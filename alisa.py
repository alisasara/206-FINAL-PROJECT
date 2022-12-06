
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

# Creates list of types ID's and numbers
def create_types_table(cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS event_types (id INTEGER PRIMARY KEY, type TEXT)")
    conn.commit()

# Creates list of states ID's and numbers
def create_states_table(cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS states (id INTEGER PRIMARY KEY, type TEXT)")
    conn.commit()

# Creates list of venues ID's and numbers
def create_venues_table(cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS venues (id INTEGER PRIMARY KEY, type TEXT)")
    conn.commit()

def create_events_table(cur, conn):
    cur.execute('CREATE TABLE IF NOT EXISTS seatgeek (id INTEGER PRIMARY KEY, type TEXT, name TEXT, venue TEXT, time TEXT, state TEXT)')
    conn.commit()

def add_events_from_json(filename, cur, conn):
    f = open(filename)
    file_data = f.read()
    f.close()
    json_data = json.loads(file_data)

    types = []
    states = []
    venues = []
    for items in json_data["events"]:
        id = items["id"]  #primary key bc its unique - for the insert or ignore 
        type = items['type']
        types.append(type)
        venue = items['venue']['name']
        venues.append(venue)
        time = items["datetime_utc"]
        state = items['venue']['state']
        states.append(state)
        name = items['performers'][0]['name']
        
        # seatgeek main table info
        cur.execute('INSERT OR IGNORE INTO seatgeek (id, type, name, venue, time, state) VALUES (?,?,?,?,?,?)', (id, type, name, venue, time, state))
        conn.commit()
    
    # 25 count limit 
    cur.execute("SELECT * FROM seatgeek")
    counter = cur.fetchall()
    print(len(counter))

    # info for types 
    types_dict = {}
    for t in types:
        if t in types_dict:
            types_dict[t] += 1
        else:
            types_dict[t] = 1
    type_list = []
    for keys in types_dict.keys():
        type_list.append(keys)
    for i in range(len(type_list)):
        cur.execute("INSERT OR IGNORE INTO event_types (id,type) VALUES (?,?)",(i,type_list[i]))
        conn.commit()
    
    # info for states
    states_dict = {}
    for s in states:
        if s in states_dict:
            states_dict[s] += 1
        else:
            states_dict[s] = 1
    states_list = []
    for keys in states_dict.keys():
        states_list.append(keys)
    for i in range(len(states_list)):
        cur.execute("INSERT OR IGNORE INTO states (id,type) VALUES (?,?)",(i,states_list[i]))
        conn.commit()

    # info for venues 
    venues_dict = {}
    for v in venues:
        if v in venues_dict:
            venues_dict[v] += 1
        else:
            venues_dict[v] = 1
    venues_list = []
    for keys in venues_dict.keys():
        venues_list.append(keys)
    for i in range(len(states_list)):
        cur.execute("INSERT OR IGNORE INTO venues (id,type) VALUES (?,?)",(i,venues_list[i]))
        conn.commit()


# query db- sele t count of column or sleect everything and count in python and then returns number - thne input 25 
# index events from [x:x]

def main():
    cur, conn = setUpDatabase('EVENTS_db')
    create_events_table(cur, conn)
    create_types_table(cur, conn)
    create_states_table(cur, conn)
    create_venues_table(cur, conn)
    add_events_from_json('events.json', cur, conn)


if __name__ == "__main__":
    main()
