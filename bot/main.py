import os
import telebot
from dotenv import load_dotenv
import requests
import time

load_dotenv()

token = os.getenv("TOKEN")
bot = telebot.TeleBot(token)
base_url = os.getenv("BASE_URL")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_message = """Heya! I'm Lana, the edututor bot.\nI am here to act as your study pal, so ask me any educational question and let's learn together! 👩🏾‍🏫. \nTo begin a new conversation, please type \n"/newchat" and hit enter."""
    bot.reply_to(message,welcome_message)


@bot.message_handler(commands=['newchat'])
def new_chat(message):
    user_id = message.from_user.id
    url = base_url + f'?user_id={user_id}'
    response = requests.get(url)
    if response.status_code == 200:
        sent_msg = bot.send_message(message.chat.id, response.json()['response'])
        bot.register_next_step_handler(sent_msg, continue_chat)
    else:
        bot.send_message(message.chat.id, "Error ocurred on server-side")
    

def continue_chat(message):
    user_id = message.from_user.id
    url = base_url + f'?user_id={user_id}'
    user_message = {"messages":message.text}
    response = requests.post(url,json= user_message)
    if response.status_code == 200:
        sent_msg = bot.send_message(message.chat.id, response.json()['response'])
        bot.register_next_step_handler(sent_msg, continue_chat)
    else:
        bot.send_message(message.chat.id, "Error ocurred on server-side")


def runbot():
    while True:
        try:
            bot.infinity_polling(none_stop=True)
        except:
            time.sleep(10)


runbot()












