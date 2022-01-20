# Needed libraries
import speedtest
import json
import time
import sqlite3

# This Python scripts conducts a speedtest of the internet. 
# It takes the result and stores it in a database, prints the results to console, and makes a map.

# This function is the actual test. 
def test():

    # Starting the speedtest.   
    print("\nInitializing speedtest...")
    test = speedtest.Speedtest()

    # locating the best server.
    print("Finding the best server...")
    best = test.get_best_server()

    # The server information is in JSON format. Info takes the information, intel loads it back into python.
    info = json.dumps(best, indent=4, sort_keys=True)
    intel = json.loads(info)

    # Conducts download test.
    print("Testing Download Speed...")
    download = test.download()

    # Conducts upload test.
    print("Testing Upload Speed...")
    upload = test.upload()

    # Conducts ping test.
    print("Testing Ping Time...\n\n")
    ping = test.results.ping
    
    # Sends the relevant information to the next function.
    information(intel, download, upload, ping)

# This function stores all the information for use in other functions. 
def information(intel, download, upload, ping):
    
    # This pulls all the information into keys that can be used later
    dread = (f'{download / 1024 / 1024:.2f} Mbps')
    uread = (f'{upload / 1024 / 1024:.2f} Mbps')
    pread = (f'{ping:.2f}ms')
    d = intel['d']
    host = intel['host']
    lat = intel['lat']
    lon = intel['lon']
    name = intel['name']
    sponsor = intel['sponsor']
    timestr = time.strftime("%Y%m%d-%H%M%S")
    
    # Prints the information for the user to see in console. 
    print(f'Download Speed: {dread}')
    print(f'Upload Speed: {uread}')
    print(f'Ping: {pread}\n\n')
    print("Sending information to database and creating map...")
        
    # Sends the relevant information to the next functions.     
    dbinput(dread, uread, pread, d, host, lat, lon, name, sponsor, timestr)
    
# This function takes the passed information and uploads it to a database for future reference.     
def dbinput(dread, uread, pread, d, host, lat, lon, name, sponsor, timestr):
    
    # Connects to the database and establishes a cursor
    connect = sqlite3.connect('speedtest.db')
    cursor = connect.cursor()

    # Query to insert the information into the corresponding table   
    insertQuery = """INSERT INTO results (download, upload, ping, d, host, lat, lon, name, sponsor, time) VALUES (?,?,?,?,?,?,?,?,?,?)"""
        
    # Pushes the information to the database    
    with connect as connection:
        
        cursor.execute(insertQuery, [dread, uread, pread, d, host, lat, lon, name, sponsor, timestr])
        connection.commit()    
        
    print("DB Publish complete.")  

# Calls the first function which starts the script        
test()