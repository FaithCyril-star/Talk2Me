import os
import openai
from flask import Flask,request
import nltk
from myChat import Chat
nltk.download('punkt')

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")



chat = Chat()

@app.route("/", methods=["GET","POST"])
def conversation():
    if request.method == "GET":
        chat.clear_chat()

        response = "New conversation initiated"
    else:
        message_text = request.json['info']
        chat.add_message({"role":"user","content":message_text})
        
         if chat.token_size > 3075:
            chat.clear_chat()
            return {"response":"chat limit is reached, conversation re-initiated"}


        completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=chat.conversation
        )

        response = completion.choices[0].message.content
        chat.add_message({"role":"assistant","content":response})

    return {"response": response}



    
