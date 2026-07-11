#!/usr/bin/python
#-*- coding: utf-8 -*-
import os
import socket
import tweepy

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

ip = get_ip_address()

#print (ip)

# SECURITY: credentials were hardcoded here and committed to git history.
# Rotate these Twitter/X API keys immediately; do not reuse the old values.
#Authentication
consumer_key = os.environ["TWITTER_CONSUMER_KEY"]
consumer_secret = os.environ["TWITTER_CONSUMER_SECRET"]
access_token = os.environ["TWITTER_ACCESS_TOKEN"]
access_secret = os.environ["TWITTER_ACCESS_SECRET"]
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

