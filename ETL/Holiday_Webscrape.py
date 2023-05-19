# Databricks notebook source
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from datetime import date, datetime



def getHTML(year='2023'):
    """'Takes in a string url and year. Concats string and year and request a texx
    response back from the url"""
    url = f'https://www.timeanddate.com/holidays/us/{year}?hol=25'
    print(url)
    response = requests.get(url)
    return response.text

def create_holdidays_df(lst=None):
    if lst == None:
        years = ['2015','2016','2017','2018','2019','2020','2021','2022','2023']
    else:
        years = lst
    Date = []
    holiday = []
    for y in years:
        html = getHTML(y) #creates url to be scraped
        soup = bs(html, 'html.parser')
        table = soup.find('table')
        tbody = table.find('tbody')
        row = tbody.find_all('tr', class_='showrow')
    for r in row:
        holiday.append(r.find_next('a').text)
        Date.append(str(r.find_next('th').text+" "+y))
    data = [Date,holiday]
    holiday_df = pd.DataFrame(data,).T
    holiday_df.rename(columns={0:'Date',1:'Holiday'}, inplace=True)
    holiday_df['Date'] = pd.to_datetime(holiday_df.Date)
    holiday_df['year'] = holiday_df.Date.dt.year
    holiday_df['dayofyear'] = holiday_df.Date.dt.dayofyear
    df = spark.createDataFrame(holiday_df)
    df = df.repartition(1)
    df.write.mode("overwrite").csv('/mnt/weatherwatts/holidays', header=True) 


create_holdidays_df()


