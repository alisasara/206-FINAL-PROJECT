import unittest
import sqlite3
import json
import os
import requests
import matplotlib.pyplot as plt

JSON_LINK = "https://api.openweathermap.org/data/2.5/weather?q={}k&units={}&appid={}"
API_KEY = "ac432d87c69ca67d59caed32d101128c"
units = "imperial"
locations = ["New York City,ny", "Los Angeles,ca", "Chicago,il", "Houston,tx", "Phoenix,az", "Philadelphia,pa", "San Antonio,tx", "San Diego,ca", "Dallas,tx", "San Jose,ca", "Austin,tx", "Jacksonville,fl", "Fort Worth,tx", "Columbus,oh", "Charlotte,nc","Indianapolis,in", "San Francisco,ca", "Seattle,wa", "Denver,co","Washington,dc", "Nashville,tn", "Oklahoma City,ok", "Boston,ma", "El Paso,tx", "Portland,or", "Las Vegas,nv", "Louisville,ky", "Memphis,tn", "Detroit,mi", "Baltimore,md", "Milwaukee,wi","Albuquerque,nm", "Fresno,ca", "Tucson,az", "Sacramento,ca", "Kansas City,mo","Mesa,az", "Atlanta,ga", "Omaha,ne", "Colorado Springs,co", "Raleigh,nc", "Long Beach,ca", "Virginia Beach,va", "Miami,fl", "Oakland,ca", "Minneapolis,mn", "Tulsa,ok", "Bakersfield,ca", "Wichita,ks", "Arlington,tx", "Aurora,co", "Tampa,fl", "New Orleans,la", "Cleveland,oh", "Honolulu,hi", "Anaheim,ca", "Henderson,nv", "Lexington,ky", "Irvine,ca", "Stockton,ca", "Orlando,fl", "Corpus Christi,tx", "Newark,nj", "Riverside,ca", "St. Paul,mn", "Cincinnati,oh", "San Juan,pr", "Santa Ana,ca", "Greensboro,nc", "Pittsburgh,pa", "Jersey City,nj", "St. Louis,mo", "Lincoln,ne", "Durham,nc", "Anchorage,ak", "Plano,tx", "Chandler,az", "Chula Vista,ca", "Buffalo,ny", "Gilbert,az", "Madison,wi", "Reno,nv", "North Las Vegas,nv", "Toledo,oh", "Fort Wayne,in", "Irving,tx", "Lubbock,tx", "St. Petersburg, fl", "Laredo,tx", "Chesapeake,va", "Winston-Salem,nc", "Glendale,az", "Garland,tx", "Scottsdale,az", "Arlington,va", "Enterprise,nv", "Boise,id", "Santa Clarita,ca", "Norfolk,va"]



def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def create_weather_table(cur, conn):
    base_url  = "https://api.openweathermap.org/data/2.5/weather?q={}k&units={}&appid={}"
    for i in range(len(locations)):
        request_url = base_url.format(locations[i], units, API_KEY )
        param_dict = {'format': 'json'}
        r = requests.get(request_url, params = param_dict)
        data = r.text
        json_data = json.loads(data) # decoding JSON file
        # print(json_data)
    



def main():
    cur, conn = setUpDatabase('TRAVEL_db')
    create_weather_table(cur, conn)


if __name__ == "__main__":
    main()