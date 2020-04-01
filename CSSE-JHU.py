#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 14:13:27 2020

@author: setup
"""

import pandas as pd
import matplotlib.pyplot as plt

export_path = '/home/setup/Documents/DevBarn/Covid-Analysis/export_graph.jpg'
countries = ['Brazil','Canada','US','Italy','Spain']

def Get_CSSEJHU_Data():
    CSSEJHU_confirmed_global = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
    CSSEJHU_deaths_global = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
    CSSEJHU_recovered_global = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')
    
    return {'confirmed' : CSSEJHU_confirmed_global, 'deaths' : CSSEJHU_deaths_global, 'recovered' : CSSEJHU_recovered_global}

def GroupBy_Sum(data,column):
    
    data_column = data.groupby(column).sum().T
    
    return data_column

def EvolutionData(data,country):
    evolution = data[country][2:]
    evolution = evolution[data[country]>0]
    evolution = evolution.reset_index()[country]
    
    return evolution
    
CSSEJHU = Get_CSSEJHU_Data()

CSSEJHU_country = {}

CSSEJHU_country.update({'confirmed' : GroupBy_Sum(CSSEJHU['confirmed'],'Country/Region')})
CSSEJHU_country.update({'deaths' : GroupBy_Sum(CSSEJHU['deaths'],'Country/Region')})
CSSEJHU_country.update({'recovered' : GroupBy_Sum(CSSEJHU['recovered'],'Country/Region')})


country_data = []
max_evolution = []
for country in countries:
    evolution_country = EvolutionData(CSSEJHU_country['confirmed'], country)
    country_data.append(evolution_country)
    max_evolution.append(max(evolution_country.index))
    
xlim = min(max_evolution)+1

for i in range(len(country_data)):
    country_data[i] = country_data[i][:xlim]


# Accuracy
for i in country_data:
    plt.plot(i)
plt.xlim(left=0, right=xlim)
plt.title('Confirmed Cases vs Day')
plt.ylabel('Confirmed Cases')
plt.xlabel('Day')
plt.legend(countries, loc='upper left')
plt.savefig(export_path, quality=100, dpi=1000)
plt.show()

