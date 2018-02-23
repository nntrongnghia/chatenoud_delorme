from fbchat import Client
from fbchat.models import *

client = Client('hakimtsouria@gmail.com', 'kimodu06')
def send_message(message):
    if not client.isLoggedIn():
        client.login('hakimtsouria@gmail.com', 'kimodu06')
    client.send(Message(text=message), thread_id=client.uid, thread_type=ThreadType.USER)
    return None

def logout():
    client.logout()
    return None