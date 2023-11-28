from flask import Flask,request,jsonify
import os
from dotenv import load_dotenv
from utils import get_token_number,reply_request
from config import mongo_connect
load_dotenv()

app = Flask(__name__)

start_prompt=os.getenv("START_PROMPT")

collection = mongo_connect()

@app.route("/", methods=["GET","POST"])
def conversation():
    user_id = request.args.get('user_id')  

    if request.method == "GET":
        response = initialise_conversation(user_id)
    else:
        message_text = request.json['messages']
        response = continue_conversation(user_id,message_text)
        
    return jsonify({"response": response})


def initialise_conversation(user_id):
    if not collection.find_one({"_id": user_id}):
        collection.insert_one({"_id":user_id,"conversation":[{"role": "system", "content": start_prompt}],"token_count":49})
    else:
        collection.update_one({"_id":user_id},{"$set": {"conversation":[{"role": "system", "content": start_prompt}],"token_count":49}})
    
    return "Conversation initiated"


def continue_conversation(user_id,message_text):
    user_info = collection.find_one({"_id":user_id},{"_id":0})  
    conversation = user_info["conversation"]
    conversation_token_count = user_info["token_count"]

    prompt = {"role":"user","content":message_text}
    conversation.append(prompt)
    prompt_token_count = get_token_number([prompt])

    if prompt_token_count + conversation_token_count > 1000:
        conversation.clear()
        conversation.append({"role": "system", "content": start_prompt})
        conversation_token_count = 49
        return "chat limit is reached, conversation re-initiated"
    else:
        completion = reply_request(conversation)
        response = completion.choices[0].message.content
        conversation.append({"role":"assistant","content":response})
        conversation_token_count += prompt_token_count

    collection.update_one({"_id":user_id},{"$set": {"conversation":conversation,"token_count":conversation_token_count}})
    return response




