
import unittest
import sqlite3
import json
import os
import matplotlib.pyplot as plt

API_KEY = "MzA4MzEwNTV8MTY3MDM0MDc3My44MTMzMjk"
JSON_LINK = "https://api.seatgeek.com/2/events?client_id=MzA4MzEwNTV8MTY3MDM0MDc3My44MTMzMjk&per_page=100"



def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def create_events_table(cur, conn):
    cur.execute('CREATE TABLE IF NOT EXISTS seatgeek (id INTEGER PRIMARY KEY, type TEXT, name TEXT, time TEXT, state TEXT)')
    conn.commit()

def add_events_from_json(filename, cur, conn):
    f = open(filename)
    file_data = f.read()
    f.close()
    json_data = json.loads(file_data)
    # print(len(json_data["events"]))

    # pick info to put in db, list and then add to dictionary 
    for items in json_data["events"]:
        id = items["id"]  #primary key bc its unique - for the insert or ignore 
        type = items['type']
        name = items['venue']['name']
        time = items["datetime_utc"]
        state = items['venue']['state']
        cur.execute('INSERT OR IGNORE INTO seatgeek (id, type, name, time, state) VALUES (?,?,?,?,?)', (id, type, name, time, state))
        conn.commit()



def main():
    # get_flight_info()
    cur, conn = setUpDatabase('EVENTS_db')
    create_events_table(cur, conn)
    add_events_from_json('events.json', cur, conn)
    pass

if __name__ == "__main__":
    main()
