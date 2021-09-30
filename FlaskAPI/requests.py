# -*- coding: utf-8 -*-
"""
Created on Thu Sep 30 10:27:12 2021

@author: he
"""

import requests.get as rq
#from requests import get
from data_input import data_in

URL = 'http://127.0.0.1:5000/predict'
headers = {"Content-Type": "application/json"}
data = {"input": data_in}

r = requests.get(URL,headers=headers, json=data) 

r.json()
