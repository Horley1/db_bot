import os
from flask import Flask, request
from config import *
import telebot
from requests import *
from json import *
import json
from fernet import *
from datetime import datetime
from random import randint
import psycopg2

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
        bot.register_next_step_handler(message, get_login)
    else:
        bot.send_message(message.chat.id, "Эййй, ты уже в базе!")

@bot.message_handler(content_types=['text'])
def help(message):
    res = bot.send_message(message.chat.id, phrases[randint(0, 7)])
    bot.send_sticker(message.chat.id, ids[randint(0, 14)], res.id)
    bot.send_message(message.chat.id, str(message.chat.id))


def check_bd(message):
    if cursor.execute(f"SELECT * FROM data WHERE user_id={message.chat.id}").fetchone():
        return True
    else:
        return False


def get_login(message):
    global login
    login = message.text
    bot.send_message(message.from_user.id, 'ОК. Теперь напиши мне свой пароль. ')
    bot.send_message(message.from_user.id, 'Пароль шифруется внутренней функцией Python, поэтому никто кроме него пароль не узнает!')
    bot.delete_message(message.chat.id, message.message_id)
    bot.register_next_step_handler(message, get_pass)


def get_pass(message):
    global password
    password = message.text
    bot.send_message(message.from_user.id, 'Ща, не рыпайся. Отправлю запросик и закинем тебя в базу.')
    bot.delete_message(message.chat.id, message.message_id)
    reg_to_bd(message)

def get_elgur(login, password):
    r = post('https://api.eljur.ru/api/auth', data={
        'login': login,
        'password': password,
        'vendor': '2007',
        'devkey': '9235e26e80ac2c509c48fe62db23642c',  # 19c4bfc2705023fe080ce94ace26aec9
        'out_format': 'json'
    })
    if r.status_code != 200:
        return None
    token = loads(r.text)['response']['result']['token']
    r2 = get('https://api.eljur.ru/api/getmarks', params={
        'auth_token': token,
        'vendor': '2007',
        'out_format': 'json',
        'devkey': '9235e26e80ac2c509c48fe62db23642c',
        'days': '20220110-20220320'
    })
    student_code = list(r2.json()['response']['result']['students'].keys())[0]
    lst_marks = r2.json()['response']['result']['students'][student_code]['lessons']
    return (token, lst_marks)
def get_elgur_by_token(token):
    r2 = get('https://api.eljur.ru/api/getmarks', params={
        'auth_token': token,
        'vendor': '2007',
        'out_format': 'json',
        'devkey': '9235e26e80ac2c509c48fe62db23642c',
        'days': '20220110-20220320'
    })
    student_code = list(r2.json()['response']['result']['students'].keys())[0]
    lst_marks = r2.json()['response']['result']['students'][student_code]['lessons']
    return lst_marks


def encode(data):
    file = open('key.txt', 'rb')
    cipher_key = file.readline()
    cipher = Fernet(cipher_key)
    encrypted_text = cipher.encrypt(data)
    string = bytes.decode(encrypted_text, encoding='utf-8')
    return string


def reg_to_bd(message):
    if get_elgur(login, password) == None:
        bot.send_message(message.from_user.id, 'Кхмм... Пароль неверный! Введи нормально.')
        reg(message)
        return
    token, lst_marks = get_elgur(login, password)
    values = [message.chat.id, str("'") + encode(login) + str("'"), str("'") + encode(password) + str("'"), str("'") + token + str("'"), str("'") + json.dumps(lst_marks) + str("'"), datetime.now().date().day, datetime.now().date().month, datetime.now().date().year]
    cursor.execute(f"INSERT INTO data(user_id, login, pass, token, last_marks, day, month, year) VALUES({values[0]}, {values[1]}, {values[2]}, {values[3]}, {values[4]}, {values[5]}, {values[6]}, {values[7]});")
    res = bot.send_message(message.from_user.id, 'Ага, в базу тебя добавил... А теперь время получать оценки, салага!')
    bot.send_sticker(message.from_user.id, 'CAACAgIAAxkBAAEDz7hh_nZwsCfI-0F0RDJAccjHRFO2IgACYgADmS9LCloe14FkpNDVIwQ', res.id)

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