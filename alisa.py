import unittest
import sqlite3
import json
import os
import requests
import matplotlib.pyplot as plt

API_KEY = "MzA4MzEwNTV8MTY3MDM0MDc3My44MTMzMjk"
page_num = "110"
JSON_LINK = "https://api.seatgeek.com/2/events?client_id=MzA4MzEwNTV8MTY3MDM0MDc3My44MTMzMjk&per_page=110"



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
    cur.execute('CREATE TABLE IF NOT EXISTS seatgeek (id INTEGER PRIMARY KEY, type_id INTEGER, name TEXT, venue_id INTEGER, time TEXT, state_id TEXT)')
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
    for i in range(len(venues_list)):
        cur.execute("INSERT OR IGNORE INTO venues (id,type) VALUES (?,?)",(i,venues_list[i]))
        conn.commit()
       
    # 25 count limit 
    counter = cur.execute("SELECT max(id) FROM seatgeek").fetchone()[0]
    print(counter)
    if counter == None: 
        counter = 0
    for i in range(counter, counter + 25):
        if i >= 100:
            break
        # seatgeek main table info
        cur.execute('SELECT id FROM event_types WHERE type = ?',(types[i],))
        type_id = cur.fetchone()[0]
        cur.execute('SELECT id FROM venues WHERE type = ?',(venues[i],))
        venue_id = cur.fetchone()[0]
        try:
            cur.execute('SELECT id FROM states WHERE type = ?',(states[i],))
            state_id = cur.fetchone()[0]
        except:
            print("state info not found")
        try: 
            cur.execute('INSERT OR IGNORE INTO seatgeek (id, type_id, name, venue_id, time, state_id) VALUES (?,?,?,?,?,?)', (ids[i], type_id, names[i], venue_id, times[i], state_id))
        except: 
            print("exceeds 100")
        conn.commit()

def events_calculations(cur, conn):
    calc_dict = {}
    calc_list = []
    sorted_calc = []
    cur.execute("SELECT state_id FROM seatgeek")
    calc = cur.fetchall()
    for items in calc:
        # print(items)
        if items in calc_dict:
            calc_dict[items] += 1
        else:
            calc_dict[items] = 1
    # print(calc_dict)
    for k,v in calc_dict.items():
        calc_list.append((k,v))
    sorted_calc = sorted(calc_list, key = lambda x: x[1], reverse = True)
    # print(sorted_calc)
    try: 
        max_events = sorted_calc[0][0][0]
    # print(max_events)
        cur.execute('SELECT type FROM states WHERE id = ?', (max_events,))
        max_events_state = cur.fetchall()
        print(max_events_state[0][0])
        print("the state with the most events is " + max_events_state[0][0])
    except:
        print("database not fully created yet")
    return sorted_calc

    # create visualization 
    # plt.figure()
def seatgeek_visualization(cur, conn):
    plt.figure()
    x_axis = []
    y_axis = []
    values = events_calculations(cur, conn)
    print(values)
    for v in range(len(values)):
        # print(values[v][0][0])
        # print(values[v][1])
        cur.execute('SELECT type FROM states WHERE id = ?',(values[v][0][0],))
        x = cur.fetchall()
        x_axis.append(x[0][0])
        y_axis.append(values[v][1])
        # print(x[0][0])
    print(x_axis)
    print(y_axis)

    fig = plt.figure(figsize = (10,5))
    plt.bar(x_axis, y_axis, color ='purple', width = .5)
    plt.xlabel("State")
    plt.ylabel("Number of Events")
    plt.title("Number of Event per State")
    plt.show()
    


def main():
    cur, conn = setUpDatabase('TRAVEL_db')
    create_events_table(cur, conn)
    create_types_table(cur, conn)
    create_states_table(cur, conn)
    create_venues_table(cur, conn)
    events_calculations(cur, conn)
    add_events_from_json(cur, conn)
    seatgeek_visualization(cur, conn)



if __name__ == "__main__":
    main()
