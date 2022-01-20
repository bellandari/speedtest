import speedtest
import json
import time
import sqlite3
import directories
import os
import folium


def test():
    
    print("\nInitializing speedtest...")
    # Speed Test Variable for shortening
    test = speedtest.Speedtest()

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
    print("Testing Ping Time...\n\n")
    ping = test.results.ping
    
    information(intel, download, upload, ping)

def information(intel, download, upload, ping):
    
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

    
    readfile = (f'Download: {dread}\n\
    Upload: {uread}\n\
    Ping: {pread}\n\
    D: {d}\n\
    Host: {host}\n\
    Lattitude: {lat}\n\
    Longitude:{lon}\n\
    Name: {name}\n\
    Sponsor: {sponsor}')

    print(f'Download Speed: {dread}')
    print(f'Upload Speed: {uread}')
    print(f'Ping: {pread}\n\n')
    print("Sending information to database and creating map...")
        
    dbinput(intel, dread, uread, pread, d, host, lat, lon, name, sponsor, timestr)
    mapcreation(lat, lon, dread, uread, pread, timestr)
    
def dbinput(intel, dread, uread, pread, d, host, lat, lon, name, sponsor, timestr):
    
    connect = sqlite3.connect('speedtest.db')
    cursor = connect.cursor()

    # Prints formated results to console   
    insertQuery = """INSERT INTO results (download, upload, ping, d, host, lat, lon, name, sponsor, time) VALUES (?,?,?,?,?,?,?,?,?,?)"""
        
    with connect as connection:
        
        cursor.execute(insertQuery, [dread, uread, pread, d, host, lat, lon, name, sponsor, timestr])
        connection.commit()    
        
    print("DB Publish complete.")  
   
def mapcreation(lat, lon, dread, uread, pread, timestr): 
      
    completemap = os.path.join(directories.directory, timestr+'.html') 
    coordinates = (lat, lon)

    map = folium.Map(coordinates, zoom_start=15)

    # Map popup configuration, makes popup with results
    overall = (f"Download: {dread} / Upload: {uread} / Ping: {pread}")
    popup = folium.Popup(overall, max_width=400,min_width=100)
    folium.Marker(coordinates, popup = popup).add_to(map)

    # Saves map as html file in the maps folder
    map.save(completemap)
    print('Map created.')
        
test()