from fbchat import Client
from fbchat.models import *
import time

#ceci est juste une exemple de chatbot, il ne faut pas 'SPAM' facebook par login et logout trop vite.
def send_message(message):
    #remplacer <email> et <password> par un compte de facebook
    client = Client('<email>', '<password>')
    client.send(Message(text=message), thread_id=client.uid, thread_type=ThreadType.USER)
    time.sleep(1)
    client.logout()
    return None