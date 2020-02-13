#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 22:31:30 2020

@author: asahay
"""

import os
import requests
import sys
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as ureq
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime


def main():
    url = "https://en.wikipedia.org/wiki/Template:2019%E2%80%9320_Wuhan_coronavirus_data/China_medical_cases"
    uClient = ureq(url)
    #print(uClient)
    page_html=uClient.read()
    uClient.close()
    #print(page_html)
    page_soup = soup(page_html,"html.parser")
    table = page_soup.find('table',attrs={'class' : 'wikitable'})
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    data = []
    for row in rows:
       cells = row.find_all('td')
       cells = [ele.text.strip() for ele in cells]
       data.append(cells)
    df = pd.DataFrame(data)
    df = df[2:-1]
    plt.style.use('seaborn')
    df.columns = ["Date","Suspects","Active Cases","DailyIncreaseInActive","ConfirmedCumulative",
                  "DailyIncreaseInConfirmedCases","Serious","Serious%",
                  "Deaths","Recovered","Deaths+Recovered",
                  "Death/RecoveryRatio","Death/Recovery(Incremental)",
                  "DeathToCulumative","RDRatio","Quarantined",
                  "ReleasedOnTheDay",
            "Released(Cumulative)","Total","Source"]
    dates=[]
    for dateValue in df.Date:
        dateValue = datetime.strptime(dateValue,'%Y-%m-%d').date()
        actualDate = datetime(dateValue.year,dateValue.month,dateValue.day)
        dates.append(actualDate)
    df['Date'] = dates
    writer = pd.ExcelWriter('coronaVirusData.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='CoronaVirus Data')
    writer.save()
if __name__ == '__main__':
    main()
    

    