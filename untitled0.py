# -*- coding: utf-8 -*-
"""
Created on Mon May 21 13:56:54 2018

@author: mohsheik
"""

import requests
from requests.auth import HTTPDigestAuth

session = requests.session()
session.auth = HTTPDigestAuth("admin", "admin")

response = session.get("http://localhost:8002/manage/v2/databases?format=json")

print(response.status_code)
print(response.json())