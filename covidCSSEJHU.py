#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 10:20:50 2020

@author: setup
"""

from selenium import webdriver
import pandas as pd
import unicodedata
import datetime


url = 'https://especiais.g1.globo.com/bemestar/coronavirus/mapa-coronavirus/'
br_cities_coord_path = 'br_cities_coord.csv'
br_state = {'AC':'Acre','AL':'Alagoas','AP':'Amapa','AM':'Amazonas','BA':'Bahia','CE':'Ceara','DF':'Distrito Federal','ES':'Espirito Santo','GO':'Goias','MA':'Maranhao','MT':'Mato Grosso','MS':'Mato Grosso do Sul','MG':'Minas Gerais','PA':'Para','PB':'Paraiba','PR':'Parana','PE':'Pernambuco','PI':'Piaui','RJ':'Rio de Janeiro','RN':'Rio Grande do Norte','RS':'Rio Grande do Sul','RO':'Rondonia','RR':'Roraima','SC':'Santa Catarina','SP':'Sao Paulo','SE':'Sergipe','TO':'Tocantins'}
csv_save_path = 'time_series_covid19_confirmed_BR.csv'

#Collect data from specific website and return driver instance
def ColectData(url):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("headless")
    driver = webdriver.Chrome(options=chrome_options)
    
    driver.get(url)
    
    return driver

def ExtractInfo(driver,key,xpath):
    
    elements = driver.find_elements_by_xpath(xpath)
    data = []
    
    data.append(element.text for element in elements)
    
    elements = pd.DataFrame(data).T.rename(columns={0:key})
  
    return elements

def FindCoordinates(address):
    
    
    for name in coord_data.keys():
        coord_data[name] = bulk_data.iloc[group_data.indices[name]].set_index('name')
    
    location = address.apply((lambda arg: coord_data[arg['Province_State'].upper()].loc[arg['Admin2'].upper()]), axis=1)
    # location[['latitude', 'longitude']] = pd.DataFrame(location.apply(lambda loc: tuple(loc[0].coordinates) if loc else None).tolist(), index=df.index)
    
    return location

def CreateModelCSV():
    bulk_data = pd.read_csv(br_cities_coord_path)
    group_data = bulk_data.groupby('state')
    coord_data = group_data.groups
    
    

def main(url):
    
    driver = ColectData(url)
    
    xpath = "//div[@class='places__body']//div[@class='places__cell']"
    data = ExtractInfo(driver,'City',xpath)
    
    data['UID'] = 0
    data['iso2'] = 'BR'
    data['iso3'] = 'Brazil'
    data['code3'] = 0
    data['FIPS'] = 0
    
    new = data['City'].str.split(", ", n = 1, expand = True)
    data['Admin2'] = new[0].apply(lambda arg: unicodedata.normalize('NFKD', arg).encode('ASCII', 'ignore').decode("utf-8"))
    data['Province_State'] = new[1].replace(br_state)
    
    data['Country_Region'] = 'Brazil'
    
    data = data.dropna(subset=['Province_State'])
    
    location = FindCoordinates(pd.concat([data['Admin2'],data['Province_State']], axis=1))
    data['lat'],data['long'] = location['lat'],location['long']
    
    data['Combined_Key'] = data['Admin2']+', '+ data['Province_State']+', '+data['Country_Region']
    
    xpath = "//div[@class='places__body']//div[@class='places__cell places__cell--right']"
    current_day = datetime.datetime.now().strftime("%x")
    data = pd.concat([data,ExtractInfo(driver,current_day,xpath)], axis=1)
    
    data = data.dropna(subset=['Province_State'])
    
    return data

data = main(url)

model = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv')
    
    


