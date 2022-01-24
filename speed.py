# Needed libraries
import speedtest
import sqlite3
import folium
import os
import webbrowser
import time
from tabulate import tabulate
import sys

while True:
# Connects to speedtest database and establishes a cursor for SQL Queries.
    connect = sqlite3.connect('speedtest.db')
    cursor = connect.cursor()

    # Main Application 
    def mainmenu():

        # Clears the terminal for a cleaner look.
        os.system('cls||clear')

        print("\n     Welcome to the Makubex Speedtest Program.\n")
        print("     Main Menu:\n")
        print("          1. Run Speedtest")
        print("          2. Search Database")
        print("          3. Exit")

        menuselect = input("\n     Make a selection: ")
        
        # Clears terminal after selection is made. 
        os.system('cls||clear')

        if menuselect == '1':
            test()

        if menuselect == '2':
            search()

        else:
            exit        

    # The core speedtest function.     
    def test():

        print("\n     Initializing speedtest...")
        test = speedtest.Speedtest()

        print("     Finding the best server...")
        print("     This may take a few seconds...")
        best = test.get_best_server()

        print("     Testing Download Speed...")
        download = test.download()

        print("     Testing Upload Speed...")
        upload = test.upload()

        print("     Testing Ping Time...\n")
        ping = test.results.ping
        
        # Converts from bits to Mbps
        dread = (f'{download / 1024 / 1024:.2f} Mbps')
        uread = (f'{upload / 1024 / 1024:.2f} Mbps')
        pread = (f'{ping:.2f}ms')
        
        # Pulls coordinates directly from server response
        coordinates = best['lat'], best['lon']

        print(f'     Download Speed: {dread}')
        print(f'     Upload Speed: {uread}')
        print(f'     Ping: {pread}\n') 
        
        createtag(best, dread, uread, pread)

    # Creates a unique ID tag for each test to be used in future lookups. 
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
            print(f"     Unique Tag: {tag}")
            dbinput(best, dread, uread, pread, tag)    
    
    # Enters information from test() into the database.         
    def dbinput(best, dread, uread, pread, tag):

        
        # Defines data and time variables for database
        date = time.strftime("%m%d%y")
        timestr = time.strftime("%H%M%S")

        # Query to insert the information into the corresponding table   
        insertQuery = """INSERT INTO results (tag, download, upload, ping, d, host, lat, lon, name, sponsor, date, time) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)"""
            
        # Pushes the information to the database    
        with connect as connection:
            
            cursor.execute(insertQuery, [tag, dread, uread, pread, best['d'], best['host'], best['lat'], best['lon'], best['name'], best['sponsor'], date, timestr])
            connection.commit()    
            
        print("     Information uploaded to database, successfully!\n\n")
        createmap()
            
    # Creates a map by pulling the most recent entry from the database.        
    def createmap():
        
        print("     Pulling map information from the database...")
        
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

        print("     Map launched in browser!\n")
            
        print("\n     Options:\n")
        print("          1. Return to Main Menu")
        print("          2. Quit")

        menuselect = input("\n     Make a selection: ")
        
        # Clears terminal after selection is made. 
        os.system('cls||clear')

        if menuselect == '1':
            mainmenu()
            
        else:
            exit         
    
    # Search Menu & Options        
    def search():
        
        print("\n     Options:\n")
        print("         1. Display Complete History")
        print("         2. Display Specific Tag")
        print("         3. Display Specific Date")
        
        userinput = input("\n     Select an Option: ")

        searchbydate = "SELECT tag, download, upload, ping, sponsor FROM results WHERE date is '{}'".format(userinput)

        # Displays entire database and allows user to select a tag. 
        if userinput == '1':
            
            os.system('cls||clear')

            displayall = "SELECT tag, lat, lon, download, upload, ping, name, sponsor, date, time FROM results ORDER BY date DESC, time DESC"
                
            with connect as connection:
                        
                cursor.execute(displayall)
                result = cursor.fetchall()
                
                headers = ['Tag', 'Lat', 'Lon', 'Download', 'Upload', 'Ping', 'Name', 'Sponsor', 'Date', 'Time']
                print("\n")
                print(tabulate(result, headers=headers))
                
                tagselect()
               
                
        # Allows search by specific tag        
        if userinput == '2':
            
            os.system('cls||clear')
            tagselect()
                
        # Allows searching by date           
        if userinput == '3':  
   
            os.system('cls||clear')
            newinput = input("\n     Enter the date (ex: 103122): ")
            searchbydate = "SELECT tag, download, upload, ping, sponsor FROM results WHERE date is '{}'".format(newinput)

            with connect as connection:
                        
                cursor.execute(searchbydate)
                result = cursor.fetchall()
                
                headers = ['Tag', 'Lat', 'Lon', 'Download', 'Upload', 'Ping', 'Name', 'Sponsor', 'Date', 'Time']
                print('\n')
                print(tabulate(result, headers=headers))
                tagselect()                        
  
    
    # Allows user to select a tag and moves the selected information to lookupmap()
    def tagselect():
        
        newinput = input("\n     Enter the tag: ")
        searchbytag = "SELECT tag, lat, lon, download, upload, ping, name, sponsor, date, time FROM results WHERE tag is '{}'".format(newinput)
        os.system('cls||clear')

        with connect as connection:
                    
            cursor.execute(searchbytag)
            result = cursor.fetchall()

            headers = ['Tag', 'Lat', 'Lon', 'Download', 'Upload', 'Ping', 'Name', 'Sponsor', 'Date', 'Time']
            print('\n')
            print(tabulate(result, headers=headers))            
            
            for x in result:
                newresult = x
                
            question = input("\n     Do you want a map? Y/N: ")    
            
            if question == 'y':
                
                lookupmap(newresult)
                
            else:
                
                menuorno()     
                                    
    # Makes a printout of the results                                
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
        print(f"\n     Map & Results for Speedtest {tag} Launched. ")
        
        # Delay to prevent system deleting map before it is opened
        time.sleep(2)
        
        # Deletes map from system
        os.remove(f'results.html')

        menuorno()
    
    
    def menuorno():
        
        question2 = input("\n     Press M to return to Menu, Press Q to quit: ")     
        
        if question2 == 'm':
            mainmenu()
            
        else:
            sys.exit() 
            
    mainmenu()