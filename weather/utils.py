"""
utils.py
"""
import requests
import pandas as pd

from datetime import datetime
from django.db import IntegrityError
from io import StringIO
from .models import WeatherData as wd

COUNTRIES = ['UK', 'England', 'Wales', 'Scotland']
READING_TYPES = ['Tmin', 'Tmax', 'Tmean', 'Rainfall', 'Sunshine']
columns = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC', 'WIN', 'SPR', 'SUM', 'AUT', 'ANN']

base_url = 'https://www.metoffice.gov.uk/pub/data/weather/uk/climate/datasets/%s/date/%s.txt'
now = datetime.now()

def create_entry(country, year, month_or_season, reading_type, reading, entry):
    if(type(reading) != float):
        try:
            reading = float(entry[columns.index(month_or_season) + 1])
        except:
            print('except: ',type(reading),reading)
            reading = 0.0
    
    db_entry = wd(
                country = country, 
                year = year, 
                month_or_season = month_or_season, 
                reading_type = reading_type,
                reading = reading )
    try:
        db_entry.save()
    except IntegrityError as e:
        pass
    except:
        print('Some Error has occured wile creating Database record!')

def curate_data(country, year, reading_type, entry):
    for col in columns:
        month_or_season = col
        reading = entry[col]
        create_entry(country, year, month_or_season, reading_type, reading, entry)

def curate_latest_data(country, year, reading_type, entry):
    month = now.month
    for i in range(month-1):
        month_or_season = columns[i]
        reading = entry[columns[i]]
        create_entry(country, year, month_or_season, reading_type, reading, entry)

    index = i+1 
    if(month > 2):
        month_or_season = 'WIN'
        reading = entry[index + 1]
        create_entry(country, year, month_or_season, reading_type, reading, entry)
    if(month > 5):
        month_or_season = 'SPR'
        reading = entry[index + 2]
        create_entry(country, year, month_or_season, reading_type, reading, entry)
    if(month > 8):
        month_or_season = 'SUM'
        reading = entry[index + 3]
        create_entry(country, year, month_or_season, reading_type, reading, entry)    

def loadDatabase(countries = COUNTRIES, reading_types = READING_TYPES):
    for country in countries:
        for reading_type in reading_types:
            url = base_url%(reading_type, country) 
            response = StringIO(requests.get(url).text)
            
            data = pd.read_csv(response, skiprows=6, delim_whitespace=True)
            entries = data.iterrows()

            for entry in entries:
                entry = entry[1]
                year = int(entry['Year'])
                if(year == now.year):
                    curate_latest_data(country, year, reading_type, entry)
                else:
                    curate_data(country, year, reading_type, entry)
    print('Database Loaded')

def updateDatabase(countries = COUNTRIES, reading_types = READING_TYPES):
    for country in countries:
        for reading_type in reading_types:
            url = base_url%(reading_type, country) 
            response = StringIO(requests.get(url).text)
            
            data = pd.read_csv(response, skiprows=6, delim_whitespace=True)
            entries = data.iterrows()
            for entry in entries:
                pass
            entry = entry[1]
            year = int(entry['Year'])
            curate_latest_data(country, year, reading_type, entry) 
    print('Database Updated')

def present_overview(reading_type='Tmax',year=2017):
    print(reading_type)
    uk = wd.objects.filter(year=year, reading_type=reading_type, country='UK')
    eng = wd.objects.filter(year=year, reading_type=reading_type, country='England')
    scot = wd.objects.filter(year=year, reading_type=reading_type, country='Scotland')
    wal = wd.objects.filter(year=year, reading_type=reading_type, country='Wales')
    queries = [uk, eng, scot, wal]
    data = []
    for i in range(12):
        if(now.year == year and i == now.month-1):
            break
        data.append([i])
    for query in queries:
        for each in query:
            index = columns.index(each.month_or_season)
            if(index < 12):
                t = [each.reading]
                data[index] += t
    return data