#!/usr/bin/env python
# coding: utf-8

import base64, hashlib, hmac

login = 'webmonster'
secret = 'sha256'
# substr_replace
obs_login = login[:len(login)/2] + secret + login[len(login)/2:]
# hash_hmac w/ sha256
hmac64 = hmac.new(secret, base64.b64encode(obs_login), hashlib.sha256)
print hmac64.hexdigest()
