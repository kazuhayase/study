#!/usr/bin/python
#-*- coding: utf-8 -*-

import config
cfg = config.Config('./wimb.cfg')

# WhatIsMyBrowser -- Version Numbers API
# https://developers.whatismybrowser.com/api/docs/v3/integration-guide/common-elements/authentication/

import requests
import json
headers = {
    'X-API-KEY': cfg['api_key'],
}
result, version_data = requests.get(cfg['api_url'], headers=headers)
print (version_data)

