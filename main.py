from datetime import datetime
import json
import urllib
import requests
from zk import ZK, const

conn = None
zk = ZK('192.168.6.50', port=4370, timeout=5)
try:
    print('Connecting to device ...')
    conn = zk.connect()
    print(conn)
    print('Disabling device ...')
    conn.disable_device()
    attendances = conn.get_attendance()
    report = {}
    counter = 0
    # print '--- Get User ---'
    users = conn.get_users()
    for attendance in attendances:
        
        if (attendance.timestamp.day == datetime.today().day and attendance.timestamp.month == datetime.today().month and attendance.timestamp.year == datetime.today().year) or (attendance.timestamp.day == datetime.today().day - 1 and attendance.timestamp.month == datetime.today().month and attendance.timestamp.year == datetime.today().year and attendance.timestamp.hour >= 7 and attendance.timestamp.minute > 5 ):
            for user in users:
                if attendance.user_id == user.user_id:
                    counter += 1
                    month = attendance.timestamp.month
                    if int(month) < 10:
                        month = '0'+str(month)
                    else:
                        month = month
                    date = '{}/{}/{} {}:{}:{}'.format(attendance.timestamp.day,month,attendance.timestamp.year, attendance.timestamp.hour, attendance.timestamp.minute,attendance.timestamp.second)
                    reporte = [
                        date,
                        user.user_id,
                        user.name                        
                        ]
                 
                    report['key{}'.format(counter)] = reporte

    url = "https://script.google.com/macros/s/AKfycbxDL4Bmjb3-UVcfWaZu12zF5s_1_txabcVTnI-i9zlkGh4rI47f8HgvM-PGKIOUoWktLQ/exec"
    content = urllib.parse.quote(string=str(report).replace("'",'"'))
    payload='data={}'.format(content)
    print('attendance')
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Cookie': 'NID=511=V7lcouZMFEc8vmYovjIh_-mgtlp8dZgKQv-A0wtOvuC5iLHPOYrzdJck1VAOZmHIL5Bfimk5OzDTzcnTVngLnqRnlcvumIXQ_AkmuAS_mrhbXKpEdm9h8InTuMoy123dhe4_rB1qjMWuSLBbibUmbUernGHeNUwxwEuxno_0svU'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    conn.enable_device()
except Exception as e:
    print (e)
finally:
    if conn:
        conn.disconnect()