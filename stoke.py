"""
Stoke Finder
Author Lin Yan Ruei @ CCU PHY, Taiwan
"""
import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
    

def Stoke_KD_Value(name):
    df = yf.Ticker(f'{name}.TW').history(period='max')
    k = []
    d = []
    min_temp = []
    max_temp = []
    k_temp = 70
    d_temp = 70
    m = 0
    for i in range(len(df['High'])):
        if i < 8:
            min_temp.append(df['Low'][i])
            max_temp.append(df['High'][i])
        if i >= 8:
            min_temp.append(df['Low'][i])
            max_temp.append(df['High'][i])
            min = np.min(min_temp)
            max = np.max(max_temp)
            if max-min == 0:
                RSV = 100 * (df['Close'][i] - min) / (0.001)
            else: RSV = 100 * (df['Close'][i] - min) / (max-min)
            k_temp = 2/3 * k_temp + 1/3 * RSV
            d_temp = 2/3 * d_temp + 1/3 * k_temp
            k.append(k_temp)
            d.append(d_temp)
            min_temp.pop(0)
            max_temp.pop(0)
    if 20>k_temp and k_temp>d_temp:
        # print(f'Buy {name}, \n')
        m = 1
    if d_temp>k_temp and k_temp>80:
        # print(f'Sale {name}, \n')
        m = 2
    return m

# name= input('Input name')        
# Stoke_KD_Value(name)   #自行查找用
Buy = []
Sale = []
g= 0
with open('Good stokes.csv', newline='') as csvfile:    #Good Stokes 100
    rows = csv.reader(csvfile)
    for row in rows:
        name = row[0]
        g = Stoke_KD_Value(name)
        if g == 1:
            Buy.append(name)
        elif g == 2:
            Sale.append(name)

print('Buy: ', Buy)
print('Sale: ',Sale)      



