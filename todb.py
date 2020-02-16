import pymysql
from config import *


#--Обьявляем локаБД
db=pymysql.connect(host='localhost', user='iptv', password='iptv', db='iptv', charset='utf8mb4')
cur=db.cursor()
#--
#--Функция для удаления канала который заработал в текстовике todb
def file_over(channel):
  with open(todb_path) as f:
    data_db = f.readlines()
  with open(todb_path,"w") as f:
    for data in data_db:
      if data != channel:
        f.write(data)
  f.close()
#--
#--Функция для установки времени во сколько заработал канал + подсчета время "не работы" канала
def db_over(channel):
  cur.execute("update time_check set time_up=now(), time_diff=sec_to_time(timestampdiff(second,time_down,time_up)) where name=%s and time_diff is null",(channel.rstrip()))
  db.commit()
#--
def main():
  with open(todb_path) as f:
      data_db = f.readlines() #список каналов которые лежат
  with open(log_path) as f:
      data_log = f.readlines() #список каналов которые только лягли
  '''сверяем каналы которые только лягли с каналами которые в tobd.
     Если находим канал который упал но не записан в БД - записываем его'''
  for ch_log in data_log:
      ch_found=0
      for ch_db in data_db:
          if ch_log == ch_db:
              ch_found+=1
      if ch_found==0:
        if ch_log == "Все каналы работают":
          pass
        else:
          cur.execute("INSERT INTO time_check (name) VALUES (%s)",(ch_log.rstrip()))
          db.commit()
          #Занести канал в БД и поставить state=0
          f = open(todb_path,"a+")
          f.write(ch_log)
          f.close()


  '''Сверяем каналы которые в tobd с каналами которые только лягли.
     Если находим канал который заработал - удаляем его из tobd
     и ставим рабочим в бд'''
  for ch_db in data_db:
      ch_found=0
      for ch_log in data_log:
          if ch_db == ch_log:
              ch_found+=1
      if ch_found==0:
        file_over(ch_db)
        db_over(ch_db)
        #Удалить канал из БД и поставить state=1

main()
db.close()
