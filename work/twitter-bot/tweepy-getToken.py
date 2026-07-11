#!/usr/bin/python
#-*- coding: utf-8 -*-
#http://kivantium.hateblo.jp/entry/2015/01/03/000225

import os
import tweepy

# SECURITY: credentials were hardcoded here and committed to git history.
# Rotate these Twitter/X API keys immediately; do not reuse the old values.
consumer_key = os.environ["TWITTER_CONSUMER_KEY"]
consumer_secret = os.environ["TWITTER_CONSUMER_SECRET"]
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
print "Access:", auth.get_authorization_url()
verifier = raw_input('Verifier:')
auth.get_access_token(verifier)
print "Access Token:", auth.access_token
print "Access Token Secret:", auth.access_token_secret
