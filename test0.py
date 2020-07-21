# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 01:24:32 2020

@author: gcapote
"""


import pandas as pd 



url = "https://raw.githubusercontent.com/selva86/datasets/master/BostonHousing.csv"
df = pd.read_csv(url)


print(df.head())
