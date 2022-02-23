import telebot
from requests import *
from json import *
from config import *
import json
import time
from datetime import datetime
from fernet import *
import psycopg2
import smtplib
import multiprocessing
bot = telebot.TeleBot(TOKEN)
conn = psycopg2.connect(dbname=db_name, user=db_user, password=db_pass, host=db_host)
cursor = conn.cursor()
conn.autocommit = True

mail = smtplib.SMTP_SSL('smtp.mail.ru', 465)
mail.login('hor1ey@mail.ru','twzr96KmMhnVPzm8vkmg')


def get_elgur_by_token(token, message_id):
    global cursor
    if check_date(message_id) >= 2:
        token = change_token(message_id)
        cursor.execute(f"UPDATE data SET (day, month, year) = ({datetime.now().date().day}, {datetime.now().date().month},{datetime.now().date().year} ) WHERE user_id = {message_id}")

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

def parsing_process(message_id):
    global cursor
    try:
        cursor.execute(f"SELECT * FROM data WHERE user_id={message_id}")
        txt = cursor.fetchone()
        new_txt = get_elgur_by_token(txt[3], message_id)
        txt = json.loads(txt[4])
        if new_txt != txt:
            for i in range(16):
                if txt[i] != new_txt[i]:
                    ln1 = len(txt[i]['marks'])
                    ln2 = len(new_txt[i]['marks'])
                    for j in range(ln2):
                        if j > len(txt[i]['marks']) - 1 or new_txt[i]['marks'][j] != txt[i]['marks'][j]:
                            if new_txt[i]['marks'][j]['value'] not in ["Н", "н", "ОП", "оп", "Оп"]:
                                if new_txt[i]['marks'][j]['lesson_comment'] == None or new_txt[i]['marks'][j]['lesson_comment'] == "":
                                    ls_comm = ""
                                else:
                                    ls_comm = f"Тип: {new_txt[i]['marks'][j]['lesson_comment']}\n"
                                if new_txt[i]['marks'][j]['comment'] == None or new_txt[i]['marks'][j]['comment'] == "":
                                    comm = ""
                                else:
                                    comm = f"Комментарий: {new_txt[i]['marks'][j]['comment']}\n"
                                if 'mtype' not in new_txt[i]['marks'][j] or (new_txt[i]['marks'][j]['mtype']['type'] == None or new_txt[i]['marks'][j]['mtype']['type'] == ""):
                                    tp = ""
                                else:
                                    tp = f"Пояснение: {new_txt[i]['marks'][j]['mtype']['type']}\n"
                                date = new_txt[i]['marks'][j]['date'].split('-')
                                date = f'Дата: {" ".join([date[2], mon[date[1]], date[0]])}'
                                subject = f"У тебя новая оценка по {sub[new_txt[i]['name']]}\n"
                                mark = f"Оценка: <tg-spoiler> {new_txt[i]['marks'][j]['value']} ✅</tg-spoiler>\n"
                                try:
                                    bot.send_message(message_id, f"{subject}{mark}{ls_comm}{comm}{tp}{date}", parse_mode="HTML")
                                except:
                                    #banned by the user
                                    pass
                add_to_bd(message_id, new_txt)
    except Exception as e:
        add_to_bd(message_id, new_txt)
        print("Error")
        print(e)
        try:
            mail.sendmail("hor1ey@mail.ru", "ma.kalmykov23@gmail.com", str(e))
        except:
            pass


def check_date(message_id):
    global cursor
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
    global cursor
    cursor.execute(f"SELECT * FROM data WHERE user_id={message_id}")
    login = cursor.fetchone()[1]
    cursor.execute(f"SELECT * FROM data WHERE user_id={message_id}")
    password = cursor.fetchone()[2]
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

def add_to_bd(message_id, new_list):
    global cursor
    values = [message_id, str("'") + json.dumps(new_list) + str("'")]
    cursor.execute(f"UPDATE data SET last_marks = {values[1]} WHERE user_id = {values[0]}")

if __name__ == '__main__' :
    while True:
        cursor.execute("SELECT user_id FROM data")
        test = list(map(lambda x: x[0], cursor.fetchall()))
        st = datetime.now()
        with multiprocessing.Pool(5) as p:
            print(test)
            p.map(parsing_process, test)
        print(datetime.now() - st)
