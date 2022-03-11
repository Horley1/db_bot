import telebot
from requests import *
from json import *
from config import *
import json
from datetime import datetime
from fernet import *
import smtplib
import psycopg2
from telebot import types
from keyboards import *
bot = telebot.TeleBot(TOKEN)

mail = smtplib.SMTP_SSL('smtp.mail.ru', 465)
mail.login('hor1ey@mail.ru','twzr96KmMhnVPzm8vkmg')
conn = psycopg2.connect(dbname=db_name, user=db_user, password=db_pass, host=db_host)
cursor = conn.cursor()
conn.autocommit = True

def get_elgur_by_token(token, message_id):
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
                                    debt_ls_comm = ""
                                else:
                                    ls_comm = f"Тип: {new_txt[i]['marks'][j]['lesson_comment']}\n"
                                    debt_ls_comm = new_txt[i]['marks'][j]['lesson_comment']
                                if new_txt[i]['marks'][j]['comment'] == None or new_txt[i]['marks'][j]['comment'] == "":
                                    comm = ""
                                    debt_comm = ""
                                else:
                                    comm = f"Комментарий: {new_txt[i]['marks'][j]['comment']}\n"
                                    debt_comm = new_txt[i]['marks'][j]['comment']
                                if 'mtype' not in new_txt[i]['marks'][j] or (new_txt[i]['marks'][j]['mtype']['type'] == None or new_txt[i]['marks'][j]['mtype']['type'] == ""):
                                    tp = ""
                                    debt_type = ""
                                else:
                                    tp = f"Пояснение: {new_txt[i]['marks'][j]['mtype']['type']}\n"
                                    debt_type = new_txt[i]['marks'][j]['mtype']['type']
                                date = new_txt[i]['marks'][j]['date'].split('-')
                                subject = f"У тебя новая оценка по {sub[new_txt[i]['name']]}\n"
                                mark = f"Оценка: <tg-spoiler> {new_txt[i]['marks'][j]['value']} ✅</tg-spoiler>\n"
                                datef = f'Дата: {" ".join([date[2], mon[date[1]], date[0]])}\n'
                                avr = f"Новый средний балл: {new_txt[i]['average']}\n"
                                try:
                                    bot.send_message(message_id, f"{subject}{mark}{ls_comm}{comm}{tp}{datef}{avr}", parse_mode="HTML")
                                    if "2" in mark:
                                        make_debt(message_id, sub[new_txt[i]['name']], new_txt[i]['marks'][j]['value'], debt_ls_comm, debt_comm, debt_type, datef)
                                except:
                                    #banned by the user
                                    pass
                add_to_bd(message_id, new_txt)
    except Exception as e:
        new_txt = get_elgur_by_token(txt[3], message_id)
        add_to_bd(message_id, new_txt)
        print("Error")
        print(e)
        try:
            mail.sendmail("hor1ey@mail.ru", "ma.kalmykov23@gmail.com", str(e))
        except:
            pass

def debt_parse(message_id):
    cursor.execute(f"SELECT * FROM data WHERE user_id={message_id}")
    debt = json.loads(cursor.fetchone()[8])
    if debt == []:
        return
    for elem in debt:
        prev_date = datetime.strptime(elem['upd_date'], '%Y-%m-%d')
        dif = (datetime.now().date() - prev_date).days
        if dif > 5:
            debt_alert(message_id, elem)
            elem['upd_date'] = datetime.date()


def debt_alert(message_id, debt):
    if debt['ls_comm'] != '':
        final_comm = f"Комментарий: {debt['ls_comm']}"
    elif debt['type'] != '':
        final_comm = f"Комментарий: {debt['type']}"
    else:
        final_comm = ''

    bot.send_message(message_id, f"Братан! У тебя кажется задолжность по {debt['sub']}\n{debt['date']}\n{final_comm}", reply_markup=keyboard2)


def make_debt(message_id, sub, mark, ls_comm, comm, type, datef):
    res = bot.send_message(message_id, "Кажется, у тебя появилась задолжность.. Это так?🙄", reply_markup=keyboard1)
    cursor.execute(f"SELECT * FROM data WHERE user_id={message_id}")
    prev = json.loads(cursor.fetchone()[9])
    prev[res.id] = {'sub': sub, 'mark': mark, 'ls_comm': ls_comm, 'comm': comm, 'type': type, 'date': datef}
    values = [message_id, str("'") + json.dumps(prev) + str("'")]
    cursor.execute(f"UPDATE data SET buffer = {values[1]} WHERE user_id = {values[0]}")

def check_date(message_id):
    cursor.execute(f"SELECT * FROM data WHERE user_id={message_id}")
    req = cursor.fetchone()
    day = req[5]
    month = req[6]
    year = req[7]
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
    values = [message_id, str("'") + json.dumps(new_list) + str("'")]
    cursor.execute(f"UPDATE data SET last_marks = {values[1]} WHERE user_id = {values[0]}")

if __name__ == '__main__' :
    while True:
        cursor.execute("SELECT user_id FROM data")
        test = cursor.fetchall()
        for elem in test:
            parsing_process(elem[0])
            debt_parse(elem[0])