import pymysql
import telebot
import os
import subprocess
from config import *


#--Обьявляем бота
bot = telebot.TeleBot(token)
#--
#--Обьявляем БД
db=pymysql.connect(host=host, user=user, password=password, db='stalker_db', charset='utf8mb4')
cur=db.cursor()
#--
#--Получаем список включенных каналов за исключением тестовых
cur.execute("SELECT number,name FROM itv where status='1' and name not like '%test%';")
result=cur.fetchall()
#--
#--Читаем файлы в указанной директории, отделяем расширение и пишем только id
files=os.listdir(screens)
id=[]
ch_log=''
quit_text=''
quit_OK="Все каналы работают"
count=0
for file in files:
    try:
        id.append(int(file.split('.')[0]))
    except ValueError:
        pass
#--
#--Проверяем есть ли id из БД в файлах
for channel in result:
    if not channel[0] in id:
        count+=1
        quit_text+=channel[1]+'\n'
        ch_log+=channel[1]+'\n'
quit_text+='***Не работает '+str(count)+ ' канал(ов)***'
try:
    f = open(log_path,"r")
    if count!=0:
            if not ch_log==f.read():
                f.close()
                f = open(log_path,"w+")
                f.write(ch_log)
                #пишем в телеге каналы которые лежат
                bot.send_message(chat_id,text=quit_text)
            else:
                pass
    elif count==0:
        if f.read()!=quit_OK:
            f.close()
            f = open(log_path,"w+")
            f.write(quit_OK)
            bot.send_message(chat_id,text=quit_OK)
        else:
            pass
except IOError as e:
    f = open(log_path,"w+")
    bot.send_message(chat_id,text=e)
f.close()
db.close() # Закрываем соединения с БД

subprocess.Popen('python3 '+db_file, shell=True)
