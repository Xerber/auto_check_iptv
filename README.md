## Details what he does:
This chain of scripts takes screenshots of the online IPTV television stream, then checks which channels do not work, keeps statistics on which channel how long it did not work + how many times the TV channel “crashed”, sends a list of TV channels that have stopped working in Telegram.

To start, call the file generate.py, send.py and todb.py called automatically
By default, generates.py works in 8 threads, if you want to change it - change the number in
```
29 num_threads = 8
```
In the file todb.py write your data in
```
6 db=pymysql.connect(host='localhost', user='iptv', password='iptv', db='iptv', charset='utf8mb4')
```
Write your data to the config.py
Then you will need to install requirements
```
pip install -r requirements.txt
```