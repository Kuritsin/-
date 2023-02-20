import requests
import sqlite3
import json
import time


api_server = f"https://dt.miet.ru/ppo_it/api/"
global score_errors
score_errors = 0

def request_hum():
    con = sqlite3.connect('base_of_date.db')
    cur = con.cursor()
    method = api_server + 'hum/'
    for i in range(1, 7):
        response = requests.get(method + str(i))
        valuer = json.loads(response.content.decode('utf-8'))['humidity']
        ids = json.loads(response.content.decode('utf-8'))['id']
        if response.status_code == 200:
            result = cur.execute(f"""INSERT INTO hum(sensor_id, date, value) VALUES({ids}, datetime(), {valuer})""").fetchall()
        else:
            print('Error: ' + str(response.status_code))
            score_errors += 1
            break

    con.commit()
    con.close()

def request_humtemp():
    con = sqlite3.connect('base_of_date.db')
    cur = con.cursor()
    method = api_server + 'temp_hum/'

    for i in range(1, 5):
        response = requests.get(method + str(i))
        valuer = json.loads(response.content.decode('utf-8'))['humidity']
        ids = json.loads(response.content.decode('utf-8'))['id']
        tmp = json.loads(response.content.decode('utf-8'))['temperature']
        if response.status_code == 200:
            result = cur.execute(f"""INSERT INTO hum_temp(sensor_id, date, value_temp, value_hum) VALUES({ids}, datetime(), {tmp}, {valuer})""").fetchall()
        else:
            print('Error: ' + str(response.status_code))
            score_errors += 1
            break

    con.commit()
    con.close()


request_humtemp()
request_hum()

con = sqlite3.connect('base_of_date.db')
cur = con.cursor()
times = cur.execute(
    f"""SELECT time_res FROM settinges """).fetchall()
con.commit()
con.close()
timing = time.time()
times = times[0][0]
print(times)
# while True:
#     if time.time() - timing > times:
#         timing = time.time()
#         if score_errors == 0:
#             request_humtemp()
#             request_hum()
#         else:
#             break
