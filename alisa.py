import json
import unittest
import os
import requests

import unittest
import sqlite3
import json
import os
import matplotlib.pyplot as plt

API_KEY = "4OYHGD36AJLqzXGiE3TyEVLeplNvAT7W"
JSON_LINK = "https://app.ticketmaster.com/discovery/v2/events.json?countryCode=US&apikey=4OYHGD36AJLqzXGiE3TyEVLeplNvAT7W"

# def get_flight_info():
#     r = requests.get("https://app.ticketmaster.com/discovery/v2/events.json?countryCode=US&apikey=4OYHGD36AJLqzXGiE3TyEVLeplNvAT7W")
#     print(r)
#     j= json.loads(r.text)
#     return j


def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def add_events_from_json(filename):
    f = open(filename)
    file_data = f.read()
    f.close()
    json_data = json.loads(file_data)
    return json_data
    

def main():
    # get_flight_info()
    setUpDatabase('events_db')
    add_events_from_json('events.json')
    pass

if __name__ == "__main__":
    main()

# def main():
#     find_flight_info(API_KEY)

# print(main)