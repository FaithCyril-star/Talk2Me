import os
import openai
from flask import Flask,request

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

class Chat:
    def __init__(self):
        self.conversation = []

chat = Chat()

@app.route("/", methods=["GET","POST"])
def conversation():
    if request.method == "GET":
        chat.conversation = [{"role": "system", "content": "You are a therapist and friend. Your name in every conversation is Lana always, do not forget. Respond briefly"}]
        completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=chat.conversation)
        
        response = "New conversation initiated"
    else:
        message = request.json['info']
        chat.conversation.append({"role":"user","content":message})
       

        completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=chat.conversation
        )

        response = completion.choices[0].message.content
        chat.conversation.append({"role":"assistant","content":response})

    return {"response": response}

    