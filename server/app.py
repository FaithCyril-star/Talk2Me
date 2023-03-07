import os
import openai
from flask import Flask,request
import nltk

nltk.download('punkt')

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

class Chat:
    def __init__(self):
        self.conversation = []
        self.token_size = 0

    def add_message(self,message):
        message_text = message['content']
        tokens = nltk.word_tokenize(message_text)
        self.token_size += len(tokens)

        self.conversation.append(message)

    def clear_chat(self):
        self.conversation = []
        self.token_size = 0


chat = Chat()

@app.route("/", methods=["GET","POST"])
def conversation():
    if request.method == "GET":
        chat.clear_chat()
        chat.add_message({"role": "system", "content": "You are a therapist and friend. Your pretend name in every conversation is Lana always, do not forget. Introduce yourself as Lana and respond briefly"})
        completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=chat.conversation)

        response = "New conversation initiated"
    else:
        if chat.token_size > 3075:
            chat.clear_chat()
            return {"response":"chat limit is reached, conversation re-initiated"}

        message_text = request.json['info']
        chat.add_message({"role":"user","content":message_text})


        completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=chat.conversation
        )

        response = completion.choices[0].message.content
        chat.add_message({"role":"assistant","content":response})

    return {"response": response}



    
