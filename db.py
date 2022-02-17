import sqlite3
import telebot
from requests import *
from json import *
import json
from fernet import *
import time
from datetime import datetime
from random import randint
bot = telebot.TeleBot('5199364372:AAGnaM9JbpyH2_JjTpCi1zb3EN5nWUtiwmE')
connect = sqlite3.connect('bot.db')

cursor = connect.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS data (
user_id INTEGER UNIQUE NOT NULL,
login STRING,
pass STRING,
token STRING,
last_marks STRING,
day INTEGER,
month INTEGER,
year INTEGER
);""")
connect.commit()


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
    ids = ["CAACAgIAAxkBAAED5jliB622rYVv8eZEJhSU02AfXY6HEwACCwEAAlKJkSNKMfbkP3tfNSME",
    "CAACAgIAAxkBAAED5jtiB627ZWPy4SQYjXy4mT_uxr7f5wACWwADwZxgDNjYPseA8L6OIwQ",
    "CAACAgIAAxkBAAED5j1iB62_gxfmocZbsXvbUzcQb7TPIwACOgEAAlKJkSM5H9SlIyE44CME",
    "CAACAgIAAxkBAAED5j9iB63DmQEWgUnRjDBTEEQsfkYMCAACzxEAAuEYmEsMb6jvCfEBdyME",
    "CAACAgIAAxkBAAED5kFiB63Ilk6JvzNNOIq7F7Hzxx2VuAACYgYAAhyS0gPTMsh9l1U6gyME",
    "CAACAgIAAxkBAAED5kNiB63LuHof3amiyGPSXdqGbLh4FgACYgADmS9LCloe14FkpNDVIwQ",
    "CAACAgIAAxkBAAED5kViB63csm1btKnuXSmFmPiL8hU5vgAC-Q4AAnR3SUk1h3fnp2LZciME",
    "CAACAgIAAxkBAAED5kdiB63hBeLSzwH40RBUPab2AVkBowACZwADlJzpD1nBv1K_IDCPIwQ",
    "CAACAgIAAxkBAAED5kliB63sf_Vsgctp1Tgcs-Ww-mxVIwACNhAAAkk9sEvXsNAN-3e9DCME",
    "CAACAgIAAxkBAAED5ktiB637ln0jH8tK3UCioMEoR-6r5gACKBEAAlcaSUmOXFDqGGG_MSME",
    "CAACAgIAAxkBAAED5k1iB638ecKCOss-CZYRoc0ucI-iXQACDxAAAk8CUUlrHZ307_CsCCME",
    "CAACAgIAAxkBAAED5k9iB64CzjUv_WYuVfknv5EaDrFz9QACMBUAAj_uSEniPAtGDDckRyME",
    "CAACAgIAAxkBAAED0c1h_vsDtZR 101Gk1N0fPWN8oEHmLwACBwADVnU5LboLuKwYEpiCIwQ",
    "CAACAgIAAxkBAAED0c9h_vwkMIJ-E5iXn6raMpLlLoVikAACrQMCAAFji0YM1YXYfa8fXZIjBA",
    "CAACAgIAAxkBAAED0dFh_vw6qGWW9v4pM0J8ngrT2i9gpQACbwADlJzpD_cN0109W4HOIwQ",
    "CAACAgIAAxkBAAED0dNh_vxDz0xMkR4Xh0mFH-U2PJZi3AACMxAAAhWWSUlBydiAaLsldCME"]

    phrases = ["Я не знаю такой команды(((. Для регистрации напиши: /reg",
    "Ты вообще нормальый?? Напиши /reg и не позорься!",
    "Мдааммм.... Вообще не шарит... Напиши /reg уже",
    "Блин, не трать мою оперативку и напиши /reg"
    "Слыш ты! Давай иди ругайся! Я уже устал тратить свой время!",
    "Я не понял, ты вообще адекват? Что ты пишешь?",
    "Давай иди от сюда! И чтобы я тебя больше не видел!!!",
    "Иди гуляй васек!!!!!!",
    "Мдаммммммм.. Шкет, иди гуляй!"]
    res = bot.send_message(message.chat.id, phrases[randint(0, 7)])
    bot.send_sticker(message.chat.id, ids[randint(0, 14)], res.id)
    bot.send_message(message.chat.id, str(message.chat.id))


def check_bd(message):
    connect = sqlite3.connect('bot.db')
    cursor = connect.cursor()
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
    connect = sqlite3.connect('bot.db')
    cursor = connect.cursor()
    if get_elgur(login, password) == None:
        bot.send_message(message.from_user.id, 'Кхмм... Пароль неверный! Введи нормально.')
        reg(message)
        return
    token, lst_marks = get_elgur(login, password)
    values = [message.chat.id, str("'") + encode(login) + str("'"), str("'") + encode(password) + str("'"), str("'") + token + str("'"), str("'") + json.dumps(lst_marks) + str("'"), datetime.now().date().day, datetime.now().date().month, datetime.now().date().year]
    cursor.execute(f"INSERT INTO data(user_id, login, pass, token, last_marks, day, month, year) VALUES({values[0]}, {values[1]}, {values[2]}, {values[3]}, {values[4]}, {values[5]}, {values[6]}, {values[7]});")
    connect.commit()
    res = bot.send_message(message.from_user.id, 'Ага, в базу тебя добавил... А теперь время получать оценки, салага!')
    bot.send_sticker(message.from_user.id, 'CAACAgIAAxkBAAEDz7hh_nZwsCfI-0F0RDJAccjHRFO2IgACYgADmS9LCloe14FkpNDVIwQ', res.id)

bot.polling(none_stop=True, interval=0)