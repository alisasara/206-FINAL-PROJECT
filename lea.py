from bs4 import BeautifulSoup
import requests
import re
import csv
import os
import sqlite3
import matplotlib.pyplot as plt


#This function uses beautiful soup to pull data from the yelp TOP 100 webpage
def get_website_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content,'html.parser')
    
    restaurant_names = []
    restaurant_rankings = []
    restaurant_cities = []
    restaurant_states = []
    restaurant_cuisines = []
    
    name_tags = soup.find_all('h3')

    for title in name_tags:
        title = title.text.strip()
        name = re.findall('\.\s([\s\S]+?),',title)
        rank = re.findall('^[0-9]+', title)
        city = re.findall(',([\s\S]+),', title)
        state = re.findall('[a-zA-Z\s]+$', title)
        restaurant_names.extend(name)
        restaurant_rankings.append(rank[0])
        restaurant_cities.append(city[0].strip())
        restaurant_states.append(state[0].strip())
    

    p_tags = soup.find_all("p", class_ = "article-text__09f24__Ir3Y3 css-2sacua")

    #creating list of list of cuisines 
    orig_cuisine_list = []
    for item in p_tags:
        item = item.text.strip()
        if (re.search("^Cuisine:", item)):
            cuisine = re.findall("^Cuisine: ([\s\S]+)", item)
            indv_lst = cuisine[0].split(',')
            orig_cuisine_list.append(indv_lst)
        else:
            continue
    #making official cuisine categories for database by using first listed on website
    
    for lst in orig_cuisine_list:
        restaurant_cuisines.append(lst[0])
    
    ##returning each list to put into database restaurant table 

    return restaurant_rankings, restaurant_names, restaurant_cuisines, restaurant_cities, restaurant_states


# This function will set up the database
def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def create_restaurant_states_table(cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS restaurant_states (state_id INTEGER PRIMARY KEY, state TEXT)")
    conn.commit()

def create_city_table(cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS restaurants_cities (city_id INTEGER PRIMARY KEY, city TEXT)")
    conn.commit()

def create_cuisine_table(cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS cuisine_types (cuisine_id INTEGER PRIMARY KEY, cuisine TEXT)")
    conn.commit()
def create_restaurants_table(cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS restaurants (ranking INT PRIMARY KEY, name TEXT, cuisine_id TEXT, city_id TEXT, state_id TEXT)")
    conn.commit()

def set_up_table(data, cur, conn):
    
    
    main_lst = []
    states = [] #4 index in main list
    cities = [] #3 index in main list
    cuisines = [] #2 index in main list
    
    for item in data:
        main_lst.append(item)
    
    ##creating state ids 
    for state in main_lst[4]:
        if state not in states:
            states.append(state)

    for i in range(len(states)):
        cur.execute("INSERT OR IGNORE INTO restaurant_states (state_id,state) VALUES (?,?)",(i,states[i]))
        conn.commit()
    
    ##creating city ids 
    for city in main_lst[3]:
        if city not in cities:
            cities.append(city)
    for i in range(len(cities)):
        cur.execute("INSERT OR IGNORE INTO restaurants_cities (city_id,city) VALUES (?,?)",(i,cities[i]))
        conn.commit()
    
    ##creating cuisine ids 
    for cuisine in main_lst[2]:
        if cuisine not in cuisines:
            cuisines.append(cuisine)
    for i in range(len(cuisines)):
        cur.execute("INSERT OR IGNORE INTO cuisine_types (cuisine_id,cuisine) VALUES (?,?)",(i,cuisines[i]))
        conn.commit()
    

    counter = cur.execute("SELECT max(ranking) FROM restaurants").fetchone()[0]
    # print(counter)
    if counter == None: 
        counter = 0
    for i in range(counter, counter + 25):
        if i >= 100:
            break
        cur.execute('SELECT cuisine_id FROM cuisine_types WHERE cuisine = ?',(main_lst[2][i],))
        cuisine_id = cur.fetchone()[0]
        cur.execute('SELECT city_id FROM restaurants_cities WHERE city = ?',(main_lst[3][i],))
        city_id = cur.fetchone()[0]
        cur.execute('SELECT state_id FROM restaurant_states WHERE state = ?',(main_lst[4][i],))
        state_id = cur.fetchone()[0]
        
        try: 
            rank = main_lst[0][i]
            name=main_lst[1][i]
            cur.execute("INSERT OR IGNORE INTO restaurants (ranking, name, cuisine_id, city_id, state_id) VALUES (?,?,?,?,?)",(rank, name, cuisine_id,city_id,state_id))    
    
    
        except: 
            print("exceeds 100")
        conn.commit()
    

    
    pass

   
#Calculations:
  
def get_restaurant_count_state(state,cur,conn):
    
    
    cur.execute('SELECT COUNT (restaurants.state_id) FROM restaurants JOIN restaurant_states WHERE restaurants.state_id = restaurant_states.state_id  AND restaurant_states.state = ?', (state, ))
    restaurant_count = cur.fetchone()[0]
    
    if restaurant_count < 1:
        return(None)
    else:
        return(restaurant_count)
     
    
    pass

def highest_rank(state,cur,conn):
    
    count = get_restaurant_count_state(state,cur,conn)
    if count == None:
        print("There are no Yelp top ranked restaurants in " + state + ".")
        return None
    else:
        print("There are " + str(count) + " top rated restaurants in " + state +".")
        
        cur.execute('SELECT restaurants.name, restaurants.ranking  FROM restaurants JOIN restaurant_states WHERE restaurants.state_id = restaurant_states.state_id  AND restaurant_states.state = ?', (state, ))
        tups = cur.fetchall()
        print(tups)
        
    
        name_list = []
        for tup in tups:
            name_list.append(tup[0])
        names = ', '.join(name_list)
        print('These restaurants are ' + names + ".")

        max_rank = tups[0]
        for tup in tups:
            if tup[1]< max_rank[1]:
                max_rank = tup
    
        print(max_rank[0] + " is the restaurant in " + state + " with the highest ranking of " + "#" + str(max_rank[1]) +".")
    return(max_rank)
    
    pass

def restaurants_visualization_and_csv(cur, conn):
    plt.figure()
   

    state_list = []
    cur.execute("SELECT restaurant_states.state FROM restaurant_states JOIN restaurants WHERE restaurant_states.state_id = restaurants.state_id")
    states = cur.fetchall()

    for tup in states:
        state_list.append(tup[0])
    
    restaurant_count_lst = []

    
    ## using calculation functions to get count for each state
    for state in state_list:
        count = get_restaurant_count_state(state,cur,conn)
        restaurant_count_lst.append(count)


    with open("restaurants.txt", 'w') as f:
        for i in range(len(state_list)):
            if restaurant_count_lst[i] == 1:
                f.write("There is " + str(restaurant_count_lst[i]) + " Yelp top rated restaurant in " + state_list[i] + "\n")
            else:  
                f.write("There are " + str(restaurant_count_lst[i]) + " Yelp top rated restaurants in " + state_list[i] + "\n")
   

    fig = plt.figure(figsize = (20,5))
    plt.bar(state_list, restaurant_count_lst, color ='purple', width = .5)
    plt.xticks(rotation = 80)
    plt.subplots_adjust(bottom = .3)
    plt.xlabel("State")
    plt.ylabel("Number of Yelp Top 100 Restaurants")
    plt.title("Number of Top Restaurants per State")
    plt.show()
    


def main():
    url = 'https://www.yelp.com/article/yelps-top-100-us-restaurants-2022'
    data = get_website_data(url)
    

    cur, conn = setUpDatabase('TRAVEL_db')
    create_restaurants_table(cur, conn)
    create_restaurant_states_table(cur, conn)
    create_city_table(cur, conn)
    create_cuisine_table(cur, conn)
    set_up_table(data, cur, conn)

    ## state count calculation
    # choose state based on weather 

    state = input("Enter a state to view top rated restaurants: ")
    get_restaurant_count_state(state,cur,conn)

    ##highest ranking restaurant in state
    highest_rank(state,cur,conn)

    ##visualization 
    restaurants_visualization_and_csv(cur, conn)

    



if __name__ == "__main__":
    main()