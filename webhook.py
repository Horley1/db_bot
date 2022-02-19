import os

from flask import Flask, request

import telebot

TOKEN = '5199364372:AAGnaM9JbpyH2_JjTpCi1zb3EN5nWUtiwmE'
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Hello, ' + message.from_user.first_name)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.reply_to(message, message.text)


@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


# @server.route("/")
# def webhook():
#     bot.remove_webhook()
#     bot.set_webhook(url='https://eltg.herokuapp.com/' + TOKEN)
#     return "!", 200


if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url='https://elgurbot.herokuapp.com/')
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
