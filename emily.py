import unittest
import sqlite3
import json
import os
import requests
import matplotlib.pyplot as plt

JSON_LINK = "https://api.openweathermap.org/data/2.5/weather?q={}k&units={}&appid={}"
API_KEY = "ac432d87c69ca67d59caed32d101128c"
units = "imperial"
locations = ["New York City,ny", "Los Angeles,ca", "Chicago,il", "Houston,tx", "Phoenix,az", "Philadelphia,pa", "San Antonio,tx", "San Diego,ca", "Dallas,tx", "San Jose,ca", "Austin,tx", "Jacksonville,fl", "Fort Worth,tx", "Columbus,oh", "Charlotte,nc","Indianapolis,in", "San Francisco,ca", "Seattle,wa", "Denver,co","Washington,dc", "Nashville,tn", "Oklahoma City,ok", "Boston,ma", "El Paso,tx", "Portland,or", "Las Vegas,nv", "Louisville,ky", "Memphis,tn", "Detroit,mi", "Baltimore,md", "Milwaukee,wi","Albuquerque,nm", "Fresno,ca", "Tucson,az", "Sacramento,ca", "Kansas City,mo","Mesa,az", "Atlanta,ga", "Omaha,ne", "Colorado Springs,co", "Raleigh,nc", "Long Beach,ca", "Virginia Beach,va", "Miami,fl", "Oakland,ca", "Minneapolis,mn", "Tulsa,ok", "Bakersfield,ca", "Wichita,ks", "Arlington,tx", "Aurora,co", "Tampa,fl", "New Orleans,la", "Cleveland,oh", "Honolulu,hi", "Anaheim,ca", "Henderson,nv", "Lexington,ky", "Irvine,ca", "Stockton,ca", "Orlando,fl", "Corpus Christi,tx", "Newark,nj", "Riverside,ca", "St. Paul,mn", "Cincinnati,oh", "San Juan,pr", "Santa Ana,ca", "Greensboro,nc", "Pittsburgh,pa", "Jersey City,nj", "St. Louis,mo", "Lincoln,ne", "Durham,nc", "Anchorage,ak", "Plano,tx", "Chandler,az", "Chula Vista,ca", "Buffalo,ny", "Gilbert,az", "Madison,wi", "Reno,nv", "North Las Vegas,nv", "Toledo,oh", "Fort Wayne,in", "Irving,tx", "Lubbock,tx", "St. Petersburg, fl", "Laredo,tx", "Chesapeake,va", "Winston-Salem,nc", "Glendale,az", "Garland,tx", "Scottsdale,az", "Arlington,va", "Enterprise,nv", "Boise,id", "Santa Clarita,ca", "Norfolk,va", "Detroit,mi"]



def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def create_weather_table(cur, conn):
    cur.execute('CREATE TABLE IF NOT EXISTS weather (ids INTEGER PRIMARY KEY, names TEXT, temperature INTEGER, feels_like INTEGER)')
    conn.commit()

def create_weather_info(cur, conn):
    temperature = []
    feels_like = []
    names = []
    ids = []
    nums = 1
    base_url  = "https://api.openweathermap.org/data/2.5/weather?q={}k&units={}&appid={}"
    for i in range(len(locations)):
        request_url = base_url.format(locations[i], units, API_KEY )
        param_dict = {'format': 'json'}
        r = requests.get(request_url, params = param_dict)
        data = r.text
        json_data = json.loads(data) # decoding JSON file
        # print(json_data)
        id = nums
        nums += 1 
        ids.append(id)
        temp = json_data["main"]["temp"]
        temperature.append(temp)
        feels = json_data["main"]["feels_like"]
        feels_like.append(feels)
        name = json_data["name"]
        names.append(name)
    # print(temperature)
    # print(feels_like)
    # print(names)

    counter = cur.execute("SELECT max(ids) FROM weather").fetchone()[0]
    print(counter)
    if counter == None: 
        counter = 0
    for i in range(counter, counter + 25):
        if i >= 100:
            break
        try:
            cur.execute('INSERT OR IGNORE INTO weather (ids, names, temperature, feels_like) VALUES (?,?,?,?)', (ids[i], names[i], temperature[i], feels_like[i]))
        except: 
            print("exceeds 100")
        conn.commit()
    

def weather_calculations(cur, conn):
    list_of_temp = []
    ideal_temp = input("Enter your ideal temperature: ")
    cur.execute("SELECT temperature FROM weather")
    t = cur.fetchall()
    # print(t)
    temp_diff = 1
    temp_diff_list = []
    for x in t:
        new_temp = x[0]
        list_of_temp.append(new_temp)
    # print(list_of_temp)
    for i in range(len(list_of_temp)):
        # print(int(ideal_temp)-(list_of_temp[i]))
        if abs((int(ideal_temp)-(list_of_temp[i]))) < temp_diff:
            temp_diff_list.append(list_of_temp[i])
    while True:
        if len(temp_diff_list) > 0:
            break
        if len(temp_diff_list) == 0:
            print("There are no temperatures that match this request")
            next_try = input("Enter your next ideal temperature: ")
            for i in range(len(list_of_temp)):
                if abs((int(next_try)-(list_of_temp[i]))) < temp_diff:
                    temp_diff_list.append(list_of_temp[i])
    ideal_cities = []
    print(temp_diff_list)
    for d in temp_diff_list:
        cur.execute("SELECT names FROM weather WHERE temperature = ?", (d,))
        n = cur.fetchall()
        ideal_cities.append(n[0][0])
    print(ideal_cities)

    with open('weather.txt', 'w') as f:
        f.write("Below are the cities that best match your ideal temperature of " + str(ideal_temp) + " degrees:")
        f.write("\n")
        for i in range(len(ideal_cities)):
            f.write(ideal_cities[i] + ": The temperature in " + str(ideal_cities[i]) + " is " + str(temp_diff_list[i]) + "." +"\n")









def main():
    cur, conn = setUpDatabase('TRAVEL_db')
    create_weather_table(cur, conn)
    create_weather_info(cur, conn)
    weather_calculations(cur, conn)
  


if __name__ == "__main__":
    main()