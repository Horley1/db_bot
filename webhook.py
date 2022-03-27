import os
import psycopg2
from flask import Flask, request
from config import *
import telebot
from telebot import types
from random import randint
from requests import post, get
from json import loads, dumps
from datetime import datetime
from fernet import *
import json
from keyboards import *

bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)
conn = psycopg2.connect(dbname=db_name, user=db_user, password=db_pass, host=db_host)
cursor = conn.cursor()
conn.autocommit = True


@bot.message_handler(commands=['start'])
def start_message(message):
    # На данный момент я умею: отправлять новые оценки
    # Тебе нужно всего лишь зарегистрироваться: напиши /reg
    bot.send_message(message.chat.id, 'Привет!', reply_markup=keyboard3)
    bot.send_message(message.chat.id, 'Я бот, который будет работать вместе с твоим Элжуром.', reply_markup=keyboard4)


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, "Напиши: /start", reply_markup=keyboard3)


@bot.message_handler(commands=['reg'])
def reg(message):
    if not check_bd(message):
        bot.send_message(message.chat.id, "Напиши мне свой логин:")
        bot.register_next_step_handler(message, get_login)
    else:
        bot.send_message(message.chat.id, "Эййй, ты уже в базе! Если что-то появиться, я тебя обязательно оповещу.")


def check_bd(message):
    cursor.execute(f"SELECT * FROM data WHERE user_id={message.chat.id}")
    if cursor.fetchone():
        return True
    else:
        return False


def get_login(message):
    global login
    login = message.text
    bot.send_message(message.from_user.id, 'ОК. Теперь напиши мне свой пароль. ')
    bot.send_message(message.from_user.id,
                     'Пароль шифруется внутренней функцией Python, поэтому никто кроме него пароль не узнает!')
    bot.delete_message(message.chat.id, message.message_id)
    bot.register_next_step_handler(message, get_pass)


def get_pass(message):
    global password
    password = message.text
    bot.send_message(message.from_user.id, 'Ща, не рыпайся. Отправлю запросик и закинем тебя в базу.')
    bot.delete_message(message.chat.id, message.message_id)
    reg_to_bd(message)


def get_elgur(login, password, message):
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
        'days': '20220110-20220530'
    })
    student_code = list(r2.json()['response']['result']['students'].keys())[0]
    lst_marks = r2.json()['response']['result']['students'][student_code]['lessons']
    return (token, lst_marks)


def encode(data):
    file = open('key.txt', 'rb')
    cipher_key = file.readline()
    cipher = Fernet(cipher_key)
    encrypted_text = cipher.encrypt(data)
    string = bytes.decode(encrypted_text, encoding='utf-8')
    return string


def reg_to_bd(message):
    if get_elgur(login, password, message) == None:
        bot.send_message(message.from_user.id, 'Кхмм... Пароль неверный! Введи нормально.')
        reg(message)
        return
    token, lst_marks = get_elgur(login, password, message)
    values = [message.chat.id, str("'") + encode(login) + str("'"), str("'") + encode(password) + str("'"),
              str("'") + token + str("'"), str("'") + dumps(lst_marks) + str("'"), datetime.now().date().day,
              datetime.now().date().month, datetime.now().date().year]
    cursor.execute(
        f"INSERT INTO data(user_id, login, pass, token, last_marks, day, month, year) VALUES({values[0]}, {values[1]}, {values[2]}, {values[3]}, {values[4]}, {values[5]}, {values[6]}, {values[7]});")
    res = bot.send_message(message.from_user.id, 'Ага, в базу тебя добавил... А теперь время получать оценки, салага!')
    bot.send_sticker(message.from_user.id, 'CAACAgIAAxkBAAEDz7hh_nZwsCfI-0F0RDJAccjHRFO2IgACYgADmS9LCloe14FkpNDVIwQ',
                     res.id)


def get_debt(message):
    bot.send_message(message.chat.id, "ОК бро, теперь буду напоминать так!", keyboard3)


@bot.message_handler(commands=['menu'])
def menu(message):
    bot.send_message(message.chat.id, "⠀⠀⠀⠀⠀⠀⠀⠀🌐Меню-панель🌐⠀⠀⠀⠀", reply_markup=keyboard5)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def txt(message):
    if message.text == "⚙Меню⚙":
        menu(message)
    else:
        res = bot.send_message(message.chat.id, phrases[randint(0, len(phrases) - 1)])
        bot.send_sticker(message.chat.id, ids[randint(0, len(ids) - 1)], res.id)


@bot.callback_query_handler(func=lambda c: c.data == 'button1')
def process_callback_button1(callback_query):
    try:
        print(callback_query)
        bot.answer_callback_query(callback_query.id)
        res = bot.send_message(callback_query.from_user.id, 'Окей!')
        bot.send_sticker(callback_query.from_user.id, agree[randint(0, len(agree) - 1)], res.id)
        cursor.execute(f"SELECT * FROM data WHERE user_id={callback_query.from_user.id}")
        db_request = cursor.fetchone()
        prev_debt = json.loads(db_request[8])
        prev_buf = json.loads(db_request[9])
        buf = prev_buf[str(callback_query.message.message_id)]
        prev_debt.append(buf)
        prev_buf.pop(str(callback_query.message.message_id))
        values = [callback_query.from_user.id, str("'") + json.dumps(prev_debt) + str("'"),
                  str("'") + json.dumps(prev_buf) + str("'")]
        cursor.execute(f"UPDATE data SET debt = {values[1]}, buffer = {values[2]} WHERE user_id = {values[0]}")
    except Exception as e:
        print("error")
        print(e)


@bot.callback_query_handler(func=lambda c: c.data == 'button2')
def process_callback_button2(callback_query):
    try:
        bot.answer_callback_query(callback_query.id)
        bot.send_message(callback_query.from_user.id, 'Красава, одной двойкой меньше!')
        cursor.execute(f"SELECT * FROM data WHERE user_id={callback_query.from_user.id}")
        db_request = cursor.fetchone()
        debt = json.loads(db_request[8])
        for i in range(len(debt)):
            if debt[i]['message'] == str(callback_query.message.message_id):
                debt.pop(i)

        values = [callback_query.from_user.id, str("'") + json.dumps(debt) + str("'")]
        cursor.execute(f"UPDATE data SET debt = {values[1]} WHERE user_id = {values[0]}")
    except Exception as e:
        print("error")
        print(e)

@bot.callback_query_handler(func=lambda c: c.data == 'button4')
def process_callback_button4(callback_query):
    bot.answer_callback_query(callback_query.id)
    cursor.execute(f"SELECT * FROM data WHERE user_id={callback_query.from_user.id}")
    data = cursor.fetchone()
    debt_button = types.InlineKeyboardButton(str(data[10]), callback_data='debt')
    keyboard = types.InlineKeyboardMarkup(row_width=3).add(button13, debt_button, button14, button5)
    bot.edit_message_reply_markup(callback_query.from_user.id, callback_query.message.message_id, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda c: c.data == 'button5')
def process_callback_button5(callback_query):
    bot.answer_callback_query(callback_query.id)
    bot.edit_message_reply_markup(callback_query.from_user.id, callback_query.message.message_id, reply_markup=keyboard5)


@bot.callback_query_handler(func=lambda c: c.data == 'debt')
def process_callback_button_debt(callback_query):
    bot.answer_callback_query(callback_query.id)


@bot.callback_query_handler(func=lambda c: c.data == 'button6')
def process_callback_button6(callback_query):
    bot.answer_callback_query(callback_query.id)
    cursor.execute(f"SELECT * FROM data WHERE user_id={callback_query.from_user.id}")
    data = json.loads(cursor.fetchone()[4])
    counter = 0
    average = 0
    for elem in data:
        average += float(elem['average'])
        counter += 1
    bot.send_message(callback_query.from_user.id, f"Твой всепредметный средний балл: {average / counter:.{2}f}💪🏻")


@bot.callback_query_handler(func=lambda c: c.data == 'button7')
def process_callback_button7(callback_query):
    bot.answer_callback_query(callback_query.id)
    bot.send_message(callback_query.from_user.id, "🧑🏼‍💻Раздел в разработке!🧑🏼‍💻")


@bot.callback_query_handler(func=lambda c: c.data == 'button8')
def process_callback_button8(callback_query):
    bot.answer_callback_query(callback_query.id)
    bot.send_message(callback_query.from_user.id, "Напиши свой вопрос или предложение для меня📡:")
    bot.register_next_step_handler(callback_query.message, suggestion)

def suggestion(message):
    bot.send_message(327830972, f'Админ, пришла новая обратная связь от:\nИмя: {message.from_user.first_name} {message.from_user.last_name}\nАккаунт: @{message.from_user.username}, {message.from_user.id}\nТекст: {message.text}')
    bot.send_message(message.from_user.id, 'Хорошо! Я обязательно передам твой вопрос или просьбу. Скоро пришлю обратную связь. Жди!')


@bot.callback_query_handler(func=lambda c: c.data == 'button9')
def process_callback_button9(callback_query):
    bot.answer_callback_query(callback_query.id)
    reg(callback_query.message)


@bot.callback_query_handler(func=lambda c: c.data == 'button10')
def process_callback_button10(callback_query):
    bot.answer_callback_query(callback_query.id)
    bot.send_message(callback_query.from_user.id, 'На данный момент доступны следуйщие функции:\n╔ 📕Отправка новых оценок📕\n╟ 2️⃣Напоминание о задолжностях2️⃣\n╟ 📚Отправка домашних заданий📚\n╚ 💯Средний предметный балл💯')


@bot.callback_query_handler(func=lambda c: c.data == 'button11')
def process_callback_button9(callback_query):
    bot.answer_callback_query(callback_query.id)
    bot.send_message(callback_query.from_user.id, 'Конфиденциальность - наш приоритет. Все личные данные хранятся строго в зашифрованном виде:')
    video = open("db-video2.mp4", 'rb')
    bot.send_video(callback_query.from_user.id, video)


@bot.callback_query_handler(func=lambda c: c.data == 'button12')
def process_callback_button9(callback_query):
    bot.answer_callback_query(callback_query.id)
    bot.send_message(callback_query.from_user.id, 'С создателем бота вы можете связаться в телеграмме:\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀☎@kalmykmaks☎')


@bot.callback_query_handler(func=lambda c: c.data == 'button13')
def process_callback_button13(callback_query):
    try:
        bot.answer_callback_query(callback_query.id)
        cursor.execute(f"SELECT * FROM data WHERE user_id={callback_query.from_user.id}")
        data = cursor.fetchone()
        if data[10] - 1 > 0:
            debt_button = types.InlineKeyboardButton(str(data[10] - 1), callback_data='debt')
            keyboard = types.InlineKeyboardMarkup(row_width=3).add(button13, debt_button, button14, button5)
            bot.edit_message_reply_markup(callback_query.from_user.id, callback_query.message.message_id, reply_markup=keyboard)
            cursor.execute(f"UPDATE data SET debt_time = {data[10] - 1} WHERE user_id = {callback_query.from_user.id}")
        else:
            bot.send_message(callback_query.from_user.id, "Ошибка! Период задолжности не может быть меньше 1. Чтобы отключить функцию нажмите кнопку 'Выключить'")
    except Exception as e:
        print(e)


@bot.callback_query_handler(func=lambda c: c.data == 'button14')
def process_callback_button14(callback_query):
    try:
        bot.answer_callback_query(callback_query.id)
        cursor.execute(f"SELECT * FROM data WHERE user_id={callback_query.from_user.id}")
        data = cursor.fetchone()
        if data[10] + 1 <= 31:
            debt_button = types.InlineKeyboardButton(str(data[10] + 1), callback_data='debt')
            keyboard = types.InlineKeyboardMarkup(row_width=3).add(button13, debt_button, button14, button5)
            bot.edit_message_reply_markup(callback_query.from_user.id, callback_query.message.message_id, reply_markup=keyboard)
            cursor.execute(f"UPDATE data SET debt_time = {data[10] + 1} WHERE user_id = {callback_query.from_user.id}")
        else:
            bot.send_message(callback_query.from_user.id, "Ошибка! Период задолжности не может быть больше 31.")
    except Exception as e:
        print(e)

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
