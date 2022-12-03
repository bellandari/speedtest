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
                       
while True:
    
    connect = sqlite3.connect("speedtest.db")
    cursor = connect.cursor()
   
    runtest()