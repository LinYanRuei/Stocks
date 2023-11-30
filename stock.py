"""
Stock Finder
Author Lin Yan Ruei @ NTU PHY, Taiwan
"""
# To use this program, you must have good stocks.csv.
import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv


def Stock_KD_Value(name, t, nation):
    if nation == '1':
        df = yf.Ticker(f'{name}').history(period='max')
    elif nation == '0':
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
            else:
                RSV = 100 * (df['Close'][i] - min) / (max-min)
            k_temp = 2/3 * k_temp + 1/3 * RSV
            d_temp = 2/3 * d_temp + 1/3 * k_temp
            k.append(k_temp)
            d.append(d_temp)
            min_temp.pop(0)
            max_temp.pop(0)
    if t == 0:
        print('k = ', k_temp, 'd = ', d_temp)
        x = np.linspace(1,90,90)
        plt.plot(x,k[(len(k)-90):],label = 'k value')
        plt.plot(x,d[(len(k)-90):],label = 'd value')
        plt.legend(loc = 'upper right')
        plt.title(f'{name}')
        plt.show()
    if t == 1 and 30 > k_temp and k_temp > d_temp:
        # print(f'Buy {name}, \n')
        m = 1
        return m
    if t == 1 and d_temp > k_temp and k_temp > 80:
        # print(f'Sale {name}, \n')
        m = 2
        return m



nation = input('Welcome to this stocks selector. 0 for Taiwan companies, 1 for US companies ')
if nation == '1':
    print('Type "end" or 0000 to end the program.')
    name = input('Input name: ')  # e.g. TSLA for TESLA
    while name != 'end' and name != '0000':
        t = 0
        print(f"Currenly price: {yf.Ticker(f'{name}').history(period='1d')['Close'][0]:.2f}")
        Stock_KD_Value(name, t,nation)
        name = input('Input code name: ')
else:
    nation = '0'
    type = input('Input which type of searching method you want to use,\n 0 for search in yourself,\n 1 for good stocks 100. ')
    if type == '0':
        # 自行查找用
        print('Type "end" or 0000 to end the program.')
        name = input('Input name: ')  # e.g. 2330 for TSMC
        while name != 'end' and name != '0000':
            t = 0
            print(f"Currenly price: {yf.Ticker(f'{name}.TW').history(period='1d')['Close'][0]:.2f}")
            Stock_KD_Value(name, t, nation)
            name = input('Input code name: ')
    elif type == '1':
        # Good Stocks 100
        Buy = []
        Sale = []
        g = 0
        t = 1
        with open('Good stocks.csv', newline='') as csvfile:
            rows = csv.reader(csvfile)
            for row in rows:
                name = row[0]
                g = Stock_KD_Value(name, t, nation)
                if g == 1:
                    Buy.append(name)
                elif g == 2:
                    Sale.append(name)

        print('Buy:', Buy)
        print('Sale:', Sale)
    else:
        print('Wrong input')







