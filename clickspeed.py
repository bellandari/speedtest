# Code by: Bellandari
# GitHub: https://github.com/bellandari
# Last Update: 12/02/2022

import speedtest
import sqlite3
from tabulate import tabulate
import click
import folium
import os
import webbrowser
import time

@click.command()
@click.option("--run", type = click.Choice(['test', 'history', 'search']))
def runtest(run):

    if run == 'test':
        
        click.echo("Testing, please standby...")
        runtest = speedtest.Speedtest()
        best = runtest.get_best_server()
        download = runtest.download()
        upload = runtest.upload()
        ping = runtest.results.ping

        dread = (f'{download / 1024 / 1024:.2f} Mbps')
        uread = (f'{upload / 1024 / 1024:.2f} Mbps')
        pread = (f'{ping:.2f}ms')
        
        click.echo(f'Download: {dread}, Upload: {uread}, Ping: {pread}')
    
        table()
        createtag(best, dread, uread, pread)
    
    if run == 'history':
            
        displayall = "SELECT tag, lat, lon, download, upload, ping, name, sponsor, date, time FROM results ORDER BY date DESC, time DESC"
                
        with connect as connection:
                    
            cursor.execute(displayall)
            result = cursor.fetchall()
            
            headers = ['Tag', 'Lat', 'Lon', 'Download', 'Upload', 'Ping', 'Name', 'Sponsor', 'Date', 'Time']
            click.echo("")
            click.echo(tabulate(result, headers=headers))
    
    if run == 'search':
        newinput = input("Enter the tag: ")  
        displayall = "SELECT tag, lat, lon, download, upload, ping, name, sponsor, date, time FROM results ORDER BY date DESC, time DESC"
        searchbytag = "SELECT tag, lat, lon, download, upload, ping, name, sponsor, date, time FROM results WHERE tag is '{}'".format(newinput)

        with connect as connection:
                    
            cursor.execute(searchbytag)
            result = cursor.fetchall()
            
            headers = ['Tag', 'Lat', 'Lon', 'Download', 'Upload', 'Ping', 'Name', 'Sponsor', 'Date', 'Time']
            click.echo("")
            click.echo(tabulate(result, headers=headers))
            
            for x in result:
                newresult = x
            
            lookupmap(newresult)

def lookupmap(newresult):
    
    # Defines variables as pulled from the database 
    tag = newresult[0]     
    lat = newresult[1]
    lon = newresult[2]
    download = newresult[3]
    upload = newresult[4]
    ping = newresult[5]
    name = newresult[6]
    sponsor = newresult[7]
    date = newresult[8]
    
    coordinates = (lat, lon)      
    
    # Establishes map
    datamap = folium.Map(coordinates, zoom_start=15)

    # Formatting for Map Popup
    results = (f"\
        <b>Download:</b> {download}<br> \
        <b>Upload:</b> {upload}<br> \
        <b>Ping:</b> {ping}<br> \
        <b>Location:</b> {name}<br>\
        <b>Sponsor:</b> {sponsor}<br>\
        <b>Tag:</b> {tag}<br>\
        <b>Date:</b>{date}")
    
    # Popup configuration
    popup = folium.Popup(results, max_width=600, min_width=300)
    folium.Marker(coordinates, popup = popup).add_to(datamap)

    # Saves map as html file in the maps folder
    datamap.save('results.html')
    
    # Deploys window with map
    webbrowser.get("windows-default").open('results.html')

    click.echo("")
    click.echo(f"Map & Results for Speedtest {tag} Launched. ")
    
    # Delay to prevent system deleting map before it is opened
    time.sleep(2)
    
    # Deletes map from system
    os.remove(f'results.html')
                   
def table():
    
    with connect as connection:
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS results (tag, download, upload, ping, d, host, lat, lon, name, sponsor, date, time)''')
        connection.commit()      
        
def createtag(best, dread, uread, pread):
    
    import string
    from random import choices
    
    # Creates a random 4 digit key used to locate a specific test
    characters = string.digits + string.ascii_letters
    tag = ''.join(choices(characters, k=4))
    
    # Attempts to find the tag in the databse to prevent duplicates. 
    cursor.execute("SELECT tag FROM results")
    
    results = cursor.fetchone()
    
    # In the unlikely situation it finds a duplicate, it recalls the function to try again.    
    if results == tag:
        createtag()
    
    else:
        click.echo(f"Unique Tag: {tag}")
        dbinput(best, dread, uread, pread, tag)   
            
def dbinput(best, dread, uread, pread, tag):

        
        # Defines data and time variables for database
        date = time.strftime("%m%d%y")
        timestr = time.strftime("%H%M%S")

        # Query to insert the information into the corresponding table   
        insertQuery = """INSERT INTO results (tag, download, upload, ping, d, host, lat, lon, name, sponsor, date, time) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)"""
            
        # Pushes the information to the database    
        with connect as connection:
            
            cursor.execute('''CREATE TABLE IF NOT EXISTS results (tag, download, upload, ping, d, host, lat, lon, name, sponsor, date, time)''')
           
            cursor.execute(insertQuery, [tag, dread, uread, pread, best['d'], best['host'], best['lat'], best['lon'], best['name'], best['sponsor'], date, timestr])
            connection.commit()    
            
        click.echo("Information uploaded to database, successfully!")
        createmap()
            
def createmap():
        
    searchcommand = "SELECT lat, lon, download, upload, ping, name, sponsor FROM (SELECT * FROM results ORDER BY date DESC, time DESC) LIMIT 1"

    with connect as connection:
            
        cursor.execute(searchcommand)
        result = cursor.fetchall()        
            
    # For loop places results into a dictionary        
    for x in result:
        newresult = x
                    
    # Defines variables as pulled from the database      
    lat = newresult[0]
    lon = newresult[1]
    download = newresult[2]
    upload = newresult[3]
    ping = newresult[4]
    name = newresult[5]
    sponsor = newresult[6]
        
    coordinates = (lat, lon)      

    # Establishes map
    datamap = folium.Map(coordinates, zoom_start=15)

    # Formatting for Map Popup
    results = (f"<b>Download:</b> {download}<br> \
        <b>Upload:</b> {upload}<br> \
        <b>Ping:</b> {ping}<br> \
        <b>Location:</b> {name}<br>\
        <b>Sponsor:</b> {sponsor}")

    # Popup configuration
    popup = folium.Popup(results, max_width=600, min_width=300)
    folium.Marker(coordinates, popup = popup).add_to(datamap)

    # Saves map as html file in the maps folder
    datamap.save('map.html')

    # Deploys window with map
    webbrowser.get("windows-default").open('map.html')

    # Delay to prevent system deleting map before it is opened
    time.sleep(2)

    # Deletes map from system
    os.remove('map.html')

    click.echo("Map launched in browser!\n")     
                       
while True:
    
    connect = sqlite3.connect("speedtest.db")
    cursor = connect.cursor()
   
    runtest()