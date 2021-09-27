# -*- coding: utf-8 -*-
"""
Created on Mon Sep 27 15:11:47 2021

@author: he
"""

import glassdoor_scrapper as gs 
import pandas as pd 

path = "chromedriver.exe"

df = gs.get_jobs('data scientist',1000, False, path, 15)

df.to_csv('glassdoor_jobs.csv', index = False)