import speedtest
import json
import time
import sqlite3

connect = sqlite3.connect('speedtest.db')
cursor = connect.cursor()

# Speed Test Variable for shortening
test = speedtest.Speedtest()

# Time Stamp used to save as file names
timestr = time.strftime("%Y%m%d-%H%M%S")

#locates the best server
print("Finding the best server...")
best = test.get_best_server()

# Takes that information and pretty formats it for the JSON file
info = json.dumps(best, indent=4, sort_keys=True)
intel = json.loads(info)

# Conducts download test
print("Testing Download Speed...")
download = test.download()

# Conducts upload test
print("Testing Upload Speed...")
upload = test.upload()

# Conducts ping test
print("Testing Ping Time...")
ping = test.results.ping

# Takes results and formats them for easy reading
dread = (f'{download / 1024 / 1024:.2f} Mbps')
uread = (f'{upload / 1024 / 1024:.2f} Mbps')
pread = (f'{ping:.2f}ms')

# Prints formated results to console
print(f'Download Speed: {dread}')
print(f'Upload Speed: {uread}')
print(f'Ping: {pread}')
       
d = intel['d']
host = intel['host']
lat = intel['lat']
lon = intel['lon']
name = intel['name']
sponsor = intel['sponsor']

insertQuery = """INSERT INTO results (download, upload, ping, d, host, lat, lon, name, sponsor, time) VALUES (?,?,?,?,?,?,?,?,?,?)"""
    
with connect as connection:
    
    cursor.execute(insertQuery, [dread, uread, pread, d, host, lat, lon, name, sponsor, timestr])
    connection.commit()    
    
print("DB Publish complete.")

