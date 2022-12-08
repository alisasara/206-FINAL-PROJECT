
import unittest
import sqlite3
import json
import os
import requests
import matplotlib.pyplot as plt

API_KEY = "MzA4MzEwNTV8MTY3MDM0MDc3My44MTMzMjk"
page_num = "100"
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

def add_events_from_json(cur, conn):
    base_url  = "https://api.seatgeek.com/2/events?client_id={}&per_page={}"
    request_url = base_url.format(API_KEY, page_num )
    param_dict = {'format': 'json'}
    r = requests.get(request_url, params = param_dict)
    data = r.text
    json_data = json.loads(data) # decoding JSON file
    

    ids = []
    types = []
    states = []
    venues = []
    times = []
    names = []
    numbers = 1
    for items in json_data["events"]:
        id = numbers
        numbers += 1 
        ids.append(id)
        type = items['type']
        types.append(type)
        venue = items['venue']['name']
        venues.append(venue)
        time = items["datetime_utc"]
        times.append(time)
        state = items['venue']['state']
        states.append(state)
        name = items['performers'][0]['name']
        names.append(name)
        # add in counter variable  and then have a for loop with if statement to break if counter = 25 
        # 25 count limit 
    counter = cur.execute("SELECT max(id) FROM seatgeek").fetchone()[0]
    print(counter)
    if counter == None: 
        counter = 0
    for i in range(counter, counter + 25):
        # seatgeek main table info
        try: 
            cur.execute('INSERT OR IGNORE INTO seatgeek (id, type, name, venue, time, state) VALUES (?,?,?,?,?,?)', (ids[i], types[i], names[i], venues[i], times[i], states[i]))
        except: 
            print("exceeds 100")
    
    
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


def count_item_in_data_base(cur, conn):
    cur.execute("SELECT * FROM seatgeek")
    items = cur.fetchall()
    return len(items)
        
      
   

   

# query db- sele t count of column or sleect everything and count in python and then returns number - thne input 25 
# index events from [x:x]

def main():
    cur, conn = setUpDatabase('TRAVEL_db')
    create_events_table(cur, conn)
    create_types_table(cur, conn)
    create_states_table(cur, conn)
    create_venues_table(cur, conn)
    count_item_in_data_base(cur, conn)
    add_events_from_json(cur, conn)


if __name__ == "__main__":
    main()
