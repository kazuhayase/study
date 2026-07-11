#!/usr/bin/python
#-*- coding: utf-8 -*-
import os
import tweepy

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

#Hello, world!
api.update_status('Hello, world!')
