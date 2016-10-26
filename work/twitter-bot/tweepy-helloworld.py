#!/usr/bin/python
#-*- coding: utf-8 -*-
import tweepy

#Authentication
consumer_key = "***REMOVED***"
consumer_secret = "***REMOVED***"
access_token = "***REMOVED***"
access_secret = "***REMOVED***"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

#Hello, world!
api.update_status('Hello, world!')
