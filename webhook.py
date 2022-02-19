import os
import psycopg2
from flask import Flask, request
from config import *
import telebot
from random import randint

bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)
conn = psycopg2.connect(dbname='d23v4g77tn2j92', user='qzusajqercdmfq',
                        password='36da4de8c545b260b07dccc490b56cee3fcc72ee52a073e7fb40409e8ccf47c4', host='ec2-52-31-217-108.eu-west-1.compute.amazonaws.com')
cursor = conn.cursor()
conn.autocommit = True

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет! Если ты ещё не зарегался пиши: "/reg".')

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, "Напиши: /start")


@bot.message_handler(commands=['reg'])
def reg(message):
    if not check_bd(message):
      bot.send_message(message.chat.id, "Напиши мне свой логин:")
      #bot.register_next_step_handler(message, get_login)
    else:
      bot.send_message(message.chat.id, "Эййй, ты уже в базе!")

def check_bd(message):
    cursor.execute(f"SELECT * FROM data WHERE user_id={message.chat.id}")
    if cursor.fetchone():
        return True
    else:
        return False


@bot.message_handler(func=lambda message: True, content_types=['text'])
def help(message):
    res = bot.send_message(message.chat.id, phrases[randint(0, 7)])
    bot.send_sticker(message.chat.id, ids[randint(0, 14)], res.id)
    bot.send_message(message.chat.id, str(message.chat.id))

@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=URL)
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))