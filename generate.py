import pymysql
import subprocess
import queue
from threading import Thread
import time
from config import *


#--Обьявляем БД
db=pymysql.connect(host=host, user=user, password=password,
                   db='stalker_db', charset='utf8mb4')
cur=db.cursor()
#--
#--Получаем список включенных каналов за исключением тестовых
cur.execute("SELECT number,cmd FROM itv where status='1' ORDER BY number ASC;")
result=cur.fetchall()
db.close()
#--

def do_stuff(q):
  while True:
    chan=q.get()
    subprocess.Popen('rm -rf '+screens+str(chan[0])+'.png', shell=True)
    subprocess.Popen('/usr/bin/timeout --foreground 20s /usr/bin/ffmpeg -i '+chan[1]+' -hide_banner -y -f image2 -qscale 0 -t 0.001 -ss 00:00:4 -s 140*100 '+screens+str(chan[0])+'.png', shell=True)
    time.sleep(5)
    q.task_done()

q = queue.Queue()
num_threads = 8

for i in range(num_threads):
  worker = Thread(target=do_stuff, args=(q,))
  worker.setDaemon(True)
  worker.start()

for x in result:
  q.put(x)

q.join()
time.sleep(25)
subprocess.Popen('python3 '+send_file, shell=True)
