from fbchat import Client
from fbchat.models import *
from FNscraping import connection_check
from FNscraping import send_log
from datetime import datetime as dt


if connection_check():
    client = Client('hakimtsouria@gmail.com', 'kimodu06')
else:
    send_log('No connection fb  ' + str(dt.today()))
    print('No connection fb ' + str(dt.today()))



def send_message(message):
    if connection_check():
        if not client.isLoggedIn():
            client.login('hakimtsouria@gmail.com', 'kimodu06')
        client.send(Message(text=message), thread_id='100006887565150', thread_type=ThreadType.USER) #send message to Rachide
    else:
        send_log('No connection - fb'+ str(dt.today()))
        print('No connection - fb'+ str(dt.today()))
    return None

def logout():
    client.logout()
    return None