import telebot
from requests import *
from json import *
from config import *
import json
import time
from datetime import datetime
from fernet import *
import smtplib
import psycopg2
from telebot import types
from keyboards import *
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import *
from psycopg2.pool import ThreadedConnectionPool
from psycopg2.pool import *
    
bot = telebot.TeleBot(TOKEN)



def get_elgur_by_token(token, message_id, req, tcp_cursor):
    if check_date(message_id, req) >= 2:
        token = change_token(message_id, req, tcp_cursor)
        tcp_cursor.execute(f"UPDATE data SET (day, month, year) = ({datetime.now().date().day}, {datetime.now().date().month},{datetime.now().date().year} ) WHERE user_id = {message_id}")
    r2 = get('https://api.eljur.ru/api/getmarks', params={
        'auth_token': token,
        'vendor': '2007',
        'out_format': 'json',
        'devkey': '9235e26e80ac2c509c48fe62db23642c',
        'days': start_period + '-' + end_period
    }, headers={'Accept': 'application/xml; charset=utf-8','User-Agent':'foo'})
    student_code = list(r2.json()['response']['result']['students'].keys())[0]
    lst_marks = r2.json()['response']['result']['students'][student_code]['lessons']
    return lst_marks

def converting(line):
    st = set()
    for i in range(len(line)):
        ln2 = len(line[i]['marks'])
        for j in range(ln2):
            if line[i]['marks'][j]['value'] not in ["Н", "н", "ОП", "оп", "Оп"]:
                ls_comm = ""
                debt_ls_comm = ""
                comm = ""
                debt_comm = ""
                tp = ""
                debt_type = ""
                if line[i]['marks'][j]['lesson_comment'] != None and line[i]['marks'][j]['lesson_comment'] != "":
                    ls_comm = f"Тип: {line[i]['marks'][j]['lesson_comment']}\n"
                    debt_ls_comm = line[i]['marks'][j]['lesson_comment']
                if line[i]['marks'][j]['comment'] != None and line[i]['marks'][j]['comment'] != "":
                    comm = f"Комментарий: {line[i]['marks'][j]['comment']}\n"
                    debt_comm = line[i]['marks'][j]['comment']
                if 'mtype' in line[i]['marks'][j] and line[i]['marks'][j]['mtype']['type'] != None and line[i]['marks'][j]['mtype']['type'] != "":
                    tp = f"Пояснение: {line[i]['marks'][j]['mtype']['type']}\n"
                    debt_type = line[i]['marks'][j]['mtype']['type']
                date = tuple(line[i]['marks'][j]['date'].split('-'))
                subject = line[i]['name']
                mark = line[i]['marks'][j]['value']
                avr = line[i]['average']
                newst = tuple([subject, mark, avr, date, ls_comm, comm, tp, debt_ls_comm, debt_comm, debt_type])
                st.add(tuple(newst))
    return st

def parsing_process(message_id):
    connection = tcp.getconn()
    tcp_cursor = connection.cursor()
    connection.autocommit = True
    tcp_cursor.execute(f"SELECT * FROM data WHERE user_id={message_id}")
    req = tcp_cursor.fetchone()
    txt = json.loads(req[4])
    prev_req = converting(txt)
    try:
        new_req = get_elgur_by_token(req[3], message_id, req, tcp_cursor)
        new_converted = converting(new_req)
        values = [message_id, str("'") + json.dumps(new_req) + str("'")]
        tcp_cursor.execute(f"UPDATE data SET last_marks = {values[1]} WHERE user_id = {values[0]}")
        if new_req != prev_req:
            stnow = new_converted - prev_req
            for elem in stnow:
                subject = f"У тебя новая оценка по предмету\"{elem[0]}\"\n"
                mark = f"Оценка: <tg-spoiler> {elem[1]} ✅</tg-spoiler>\n"
                avr = f"Новый средний балл: <tg-spoiler> {elem[2]} </tg-spoiler>\n"
                datef = f'Дата: {" ".join([elem[3][2], mon[elem[3][1]], elem[3][0]])}\n'
                ls_comm = elem[4]
                comm = elem[5]
                tp = elem[6]
                debt_ls_comm = elem[7]
                debt_comm = elem[8]
                debt_type = elem[9]
                try:
                    #bot.send_message(message_id, f"{subject}{mark}{avr}{ls_comm}{comm}{tp}{datef}", parse_mode="HTML")
                    if "2" in mark or "НПА" in mark or "А/З" in mark or "нпа" in mark or "а/з" in mark or "Д" in mark:
                        make_debt(message_id, subject, mark, debt_ls_comm, debt_comm, debt_type, datef, req, tcp_cursor)
                except:
                    #banned by the user
                    pass

    except Exception as e:
        new_txt = get_elgur_by_token(req[3], message_id, req, tcp_cursor)
        values = [message_id, str("'") + json.dumps(new_req) + str("'")]
        tcp_cursor.execute(f"UPDATE data SET last_marks = {values[1]} WHERE user_id = {values[0]}")
        print("Error")
        print(e)

    tcp.putconn(connection)


def debt_parse(message_id):
    connection = tcp.getconn()
    tcp_cursor = connection.cursor()
    connection.autocommit = True
    tcp_cursor.execute(f"SELECT * FROM data WHERE user_id={message_id}")
    data = tcp_cursor.fetchone()
    debt = json.loads(data[8])
    if debt == []:
        return
    for elem in debt:
        prev_date = datetime.strptime(elem['upd_date'], '%Y-%m-%d').date()
        dif = (datetime.now().date() - prev_date).days
        if dif > data[10]:
            res = debt_alert(message_id, elem)
            elem['upd_date'] = datetime.now().date().strftime('%Y-%m-%d')
            elem['message'] = str(res.id)
    value = str("'") + json.dumps(debt) + str("'")
    tcp_cursor.execute(f"UPDATE data SET debt = {value} WHERE user_id = {message_id}")
    tcp.putconn(connection)


def debt_alert(message_id, debt):
    if debt['ls_comm'] != '':
        final_comm = f"Комментарий: {debt['ls_comm']}"
    elif debt['type'] != '':
        final_comm = f"Комментарий: {debt['type']}"
    else:
        final_comm = ''

    #res = bot.send_message(message_id, f"Братан! У тебя кажется задолжность по предмету \"{debt['sub']}\"😳\n{debt['date'][:-1]}🗓\n{final_comm}", reply_markup=keyboard2)
    #return res


def make_debt(message_id, sub, mark, ls_comm, comm, type, datef, req, tcp_cursor):
    res = bot.send_message(message_id, "Кажется, у тебя появилась задолжность.. Это так?🙄", reply_markup=keyboard1)
    prev = json.loads(req[9])
    prev[res.id] = {'sub': sub, 'mark': mark, 'ls_comm': ls_comm, 'comm': comm, 'type': type, 'date': datef, 'message': '', 'upd_date' : datetime.now().date().strftime('%Y-%m-%d')}
    values = [message_id, str("'") + json.dumps(prev) + str("'")]
    tcp_cursor.execute(f"UPDATE data SET buffer = {values[1]} WHERE user_id = {values[0]}")


def check_date(message_id, req):
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


def change_token(message_id, req, tcp_cursor):
    login = req[1]
    password = req[2]
    print(decode(login), decode(password))
    r = post('https://api.eljur.ru/api/auth', data={
        'login': decode(login),
        'password': decode(password),
        'vendor': '2007',
        'devkey': '9235e26e80ac2c509c48fe62db23642c',
        'out_format': 'json'
    }, headers={'Accept': 'application/xml; charset=utf-8','User-Agent':'foo'})
    token = loads(r.text)['response']['result']['token']
    value = str("'") + token + str("'")
    tcp_cursor.execute(f"UPDATE data SET token = {value} WHERE user_id = {message_id}")
    return token



tcp = ThreadedConnectionPool(minconn=1, maxconn=1000, user=db_user, password=db_pass, host=db_host,
                             database=db_name)
if __name__ == '__main__' :
    while True:
        try:
            conn = tcp.getconn()
            cursor = conn.cursor()
            conn.autocommit = True
            cursor.execute("SELECT user_id FROM data")
            test = cursor.fetchall()
            with ProcessPoolExecutor(max_workers=10) as executor:
                for elem in test:
                    executor.submit(parsing_process, elem[0])
                    executor.submit(debt_parse, elem[0])
            tcp.putconn(conn)
            # if datetime.now() - datetime.strptime(end_period, '%Y-%m-%d').date() >= 0 and next_periods != []:
            #TODO: fix periods

        except Exception as e:
            print(e)
            tcp = ThreadedConnectionPool(minconn=1, maxconn=1000, user=db_user, password=db_pass, host=db_host,
                                         database=db_name)
