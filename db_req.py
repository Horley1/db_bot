import telebot
from requests import *
from json import *
from config import *
import json
import time
from datetime import datetime
from fernet import *
import psycopg2

bot = telebot.TeleBot(TOKEN)
conn = psycopg2.connect(dbname='d23v4g77tn2j92', user='qzusajqercdmfq',
                        password='36da4de8c545b260b07dccc490b56cee3fcc72ee52a073e7fb40409e8ccf47c4', host='ec2-52-31-217-108.eu-west-1.compute.amazonaws.com')
cursor = conn.cursor()
conn.autocommit = True

def parsing_process(message_id):
    cursor.execute(f"SELECT * FROM data WHERE user_id={message_id}")
    txt = cursor.fetchone()
    new_txt = get_elgur_by_token(txt[3], message_id)
    txt = json.loads(txt[4])
    if  new_txt != txt:
        for i in range(16):
            if txt[i] != new_txt[i]:
                ln1 = len(txt[i]['marks'])
                ln2 = len(new_txt[i]['marks'])
                for j in range(ln2):
                    if j > len(txt[i]['marks']) - 1 or new_txt[i]['marks'][j] != txt[i]['marks'][j]:
                        bot.send_message(message_id, f"У тебя новая оценка по {new_txt[i]['name']}\nОценка: <tg-spoiler>{new_txt[i]['marks'][j]['value']}</tg-spoiler> ✅\nТип: {new_txt[i]['marks'][j]['lesson_comment']}\nДата: {new_txt[i]['marks'][j]['date']}", parse_mode="HTML")
        add_to_bd(message_id, new_txt)

def check_date(message_id):
    cursor.execute(f"SELECT * FROM data WHERE user_id={message_id}")
    day = cursor.fetchone()[5]
    cursor.execute(f"SELECT * FROM data WHERE user_id={message_id}")
    month = cursor.fetchone()[6]
    cursor.execute(f"SELECT * FROM data WHERE user_id={message_id}")
    year = cursor.fetchone()[7]
    prev = datetime(year, month, day).date()
    now = datetime.now().date()
    return (now - prev).days


def decode(data):
    file = open('key.txt', 'rb')
    cipher_key = file.readline()
    cipher = Fernet(cipher_key)
    decrypted_text = cipher.decrypt(str.encode(data, encoding='utf-8'))
    return str(decrypted_text)[2:-1]

def change_token(message_id):
    login = cursor.execute(f"SELECT * FROM data WHERE user_id={message_id}").fetchone()[1]
    password = cursor.execute(f"SELECT * FROM data WHERE user_id={message_id}").fetchone()[2]
    r = post('https://api.eljur.ru/api/auth', data={
        'login': decode(login),
        'password': decode(password),
        'vendor': '2007',
        'devkey': '9235e26e80ac2c509c48fe62db23642c',
        'out_format': 'json'
    })
    token = loads(r.text)['response']['result']['token']
    value = str("'") + token + str("'")
    cursor.execute(f"UPDATE data SET token = {value} WHERE user_id = {message_id}")
    return token



def get_elgur_by_token(token, message_id):
    if check_date(message_id) > 0:
        token = change_token(message_id)

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

def add_to_bd(message_id, new_list):
    values = [message_id ,str("'") + json.dumps(new_list) + str("'")]
    cursor.execute(f"UPDATE data SET last_marks = {values[1]} WHERE user_id = {values[0]}")


cursor.execute("SELECT user_id FROM data")
test = cursor.fetchall()
while True:
    for elem in test:
        try:
            parsing_process(elem[0])
        except:
            pass
    time.sleep(0.1)
    print("YES!!!")