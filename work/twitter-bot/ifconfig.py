#!/usr/bin/python
#-*- coding: utf-8 -*-
import socket
import tweepy

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

ip = get_ip_address()

#print (ip)

#Authentication
consumer_key = "6yH2N5Z6AeI4GF9ar8fOrKrMS"
consumer_secret = "NCD63ivS1HFiLxeW3dQvGpD5ErDP1dUj29ifHSZFKyFixUJUHU"
access_token = "725515912212676608-8GzUX1Gh2OOcxOggaaeAp4p63KUcROz"
access_secret = "uRsgsbWeoHQppBIpBXZTDuPBIy6vLee1i8CFz5snUK0jF"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

##Hello, world!
#api.update_status('Hello, world!')


#dms = api.sent_direct_messages()
#for m in dms:
#   print m

#direct message to me
to = 'kazuyoshihayase'
#to = '64309160'
msg = 'Hello!' + ip
#api.send_direct_message(user_id = to, text = msg)
api.send_direct_message(screen_name = to, text = msg)

