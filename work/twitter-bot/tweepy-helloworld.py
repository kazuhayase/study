#!/usr/bin/python
#-*- coding: utf-8 -*-
import tweepy

#Authentication
consumer_key = "6yH2N5Z6AeI4GF9ar8fOrKrMS"
consumer_secret = "NCD63ivS1HFiLxeW3dQvGpD5ErDP1dUj29ifHSZFKyFixUJUHU"
access_token = "725515912212676608-5j8xnspA9SzhubHgU0q9gaqxCs0vtix"
access_secret = "WPEy1xC3eCLQYBeDvXsEIpiCdY6pdQizgRxZfaWaMZeVF"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

#Hello, world!
api.update_status('Hello, world!')
