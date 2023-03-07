import os
import telebot
from dotenv import load_dotenv
import requests

load_dotenv()

token = os.getenv("TOKEN")
bot = telebot.TeleBot(token)
api = os.getenv("API")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_message = """Heya, welcome to the therapy bot Lana!\nI am here to act as your new friend so speak to me and let's form a bond 😘. \nTo begin a new conversation please type \n"/newchat" and hit enter."""
    bot.reply_to(message,welcome_message)


@bot.message_handler(commands=['newchat'])
def new_chat(message):
    response = requests.get(api)
    if response.status_code == 200:
        sent_msg = bot.send_message(message.chat.id, response.json()['response'])
        bot.register_next_step_handler(sent_msg, continue_chat)
    else:
        bot.send_message(message.chat.id, "Error ocurred on server-side")
    

def continue_chat(message):
    user_message = {"info":message.text}
    response = requests.post(api,json= user_message)
    if response.status_code == 200:
        sent_msg = bot.send_message(message.chat.id, response.json()['response'])
        bot.register_next_step_handler(sent_msg, continue_chat)
    else:
        bot.send_message(message.chat.id, "Error ocurred on server-side")



 
bot.infinity_polling()












