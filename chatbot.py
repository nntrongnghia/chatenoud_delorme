from fbchat import Client
from fbchat.models import *
from FNscraping import connection_check
from FNscraping import send_log
from datetime import datetime as dt
import time

IsLogged = False
while IsLogged == False:
    try:
        client = Client('hakimtsouria@gmail.com', 'kimodu06')
        IsLogged = True
    except:
        IsLogged = False
        send_log('No connection - fb'+ str(dt.today()))
        print('No connection - fb'+ str(dt.today()))
    time.sleep(10)


def send_message(message):
    if connection_check():
        client.send(Message(text=message), thread_id='100006887565150', thread_type=ThreadType.USER) #send message to Rachide
    else:
        send_log('No connection - fb'+ str(dt.today()))
        print('No connection - fb'+ str(dt.today()))
    return None

def logout():
    client.logout()
    return None