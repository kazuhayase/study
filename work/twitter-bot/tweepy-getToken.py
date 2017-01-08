#!/usr/bin/python
#-*- coding: utf-8 -*-
#http://kivantium.hateblo.jp/entry/2015/01/03/000225

import tweepy

consumer_key = "6yH2N5Z6AeI4GF9ar8fOrKrMS"
consumer_secret = "NCD63ivS1HFiLxeW3dQvGpD5ErDP1dUj29ifHSZFKyFixUJUHU"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
print "Access:", auth.get_authorization_url()
verifier = raw_input('Verifier:')
auth.get_access_token(verifier)
print "Access Token:", auth.access_token
print "Access Token Secret:", auth.access_token_secret
