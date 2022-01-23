# Needed libraries
import speedtest
import time
import sqlite3
import folium
import os
import webbrowser

# Connects to speedtest database and establishes a cursor for SQL Queries.
connect = sqlite3.connect('speedtest.db')
cursor = connect.cursor()

# Main Menu for the application. 
# Allows user to pick from options. 
def mainmenu():

    # Clears the terminal for a cleaner look.
    os.system('cls||clear')

    print("\nWelcome to the Makubex Speedtest Program.\n")
    print("Main Menu:\n")
    print("     1. Run Test")
    print("     2. Lookup Test")
    print("     3. End Program")

    menuselect = input("\nMake a selection: ")
    
    # Clears terminal after selection is made. 
    os.system('cls||clear')

    if menuselect == '1':
        test()

    if menuselect == '2':
        lookupmenu()

    else:
        exit        

# The core speedtest function.     
def test():

    print("\nInitializing speedtest...")
    test = speedtest.Speedtest()

    print("Finding the best server...")
    print("This may take a few seconds...")
    best = test.get_best_server()

    print("Testing Download Speed...")
    download = test.download()

    print("Testing Upload Speed...")
    upload = test.upload()

    print("Testing Ping Time...\n")
    ping = test.results.ping
    
    # Converts from bits to Mbps
    dread = (f'{download / 1024 / 1024:.2f} Mbps')
    uread = (f'{upload / 1024 / 1024:.2f} Mbps')
    pread = (f'{ping:.2f}ms')
    
    # Pulls coordinates directly from server response
    coordinates = best['lat'], best['lon']

    print(f'Download Speed: {dread}')
    print(f'Upload Speed: {uread}')
    print(f'Ping: {pread}\n') 
    
    createmap(best, coordinates, dread, uread, pread)
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
       return createtag()
    
    else:
        print(f"Unique Tag: {tag}")
        dbinput(best, dread, uread, pread, tag)    
    
# Creates a map with the information pulled directly from the test() function above.       
def createmap(best, coordinates, dread, uread, pread):
    
    # Establishes the map   
    datamap = folium.Map(coordinates, zoom_start=15)

    # Popup formatting
    results = (f"<b>Download:</b> {dread}<br> \
        <b>Upload:</b> {uread}<br> \
        <b>Ping:</b> {pread}<br> \
        <b>Location:</b> {best['name']}<br>\
        <b>Sponsor:</b> {best['sponsor']}    ")
    
    # Popup configuration
    popup = folium.Popup(results, max_width=600, min_width=300)
    folium.Marker(coordinates, popup = popup).add_to(datamap)

    # Saves map as html file in the maps folder
    datamap.save('map.html')
    
    # Deploys the map
    webbrowser.get("windows-default").open('map.html')
    
    # Time delay to prevent deleting before deployment
    time.sleep(2)
    
    # Removes map from system
    os.remove('map.html')
    
    print("Results launched!")
        
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
        
    print("DB Publish complete.\n\n")

# Lookup menu for the application.
# Allows user to lookup previous tests.     
def lookupmenu():
    
    print("\nMakubex Speedtest Program.\n")
    print("Lookup Menu:\n")
    print("     1. Display Specific Date")
    print("     2. Display All")
    print("     3. Search by Tag")
    print("     4. Exit")

    menuselect = input("\nMake a selection: ")
    
    # Clears terminal after selection is made.
    os.system('cls||clear')

    if menuselect == '1':
        lookuptest()
        
    if menuselect == '2':
        displayall()

    if menuselect == '3':
        lookuptag()
        
    else:
        exit    

# Displays all previous tests for viewing. 
def displayall():
    
    # SQL Query to find requested information     
    searchcommand = "SELECT tag, download, upload, ping, date, time FROM results"
    
    with connect as connection:
        
        cursor.execute(searchcommand)
        result = cursor.fetchall()

    for x in result:
        newresult = x
        print (newresult)
        
    selection()

# Looks up a specific tag if the user knows it. 
def lookuptag():
    
    selection = input("\nEnter the 4-Character Tag: ")
    
    try:
        
        # SQL Query to find requested information     
        searchcommand = "SELECT lat, lon, download, upload, ping, name, sponsor FROM results WHERE tag is '{}'".format(selection)
        
        with connect as connection:
                
                cursor.execute(searchcommand)
                result = cursor.fetchall()

        for x in result:
           
            newresult = x
            print (newresult)
        
        lookupmap(newresult)
        
    except:
        
        print("There was an error, try again!")
        lookuptag()
        
# Looks up tests by date (monthdayyear).        
def lookuptest():
    
    dateselect = input("What date? Use numerical daymonthyear (ex: 012222): ")
    
    try:
        
        # SQL Query to find requested information     
        searchcommand = "SELECT tag, download, upload, ping, sponsor FROM results WHERE date is '{}'".format(dateselect)
        
        # Pushes the information to the database    
        with connect as connection:
            
            cursor.execute(searchcommand)
            result = cursor.fetchall()

        for x in result:
            
            newresult = x
            print (newresult)
            
        selection()
    
    except:
        
        print("There was an error, try again")
        lookuptest()
    
# Allows user to select a test via typing in the tag,
# after viewing the database via previous function.     
def selection():     
       
    question = input("\nWhich test do you want to look at? Enter the 4-Character Tag: ")
    
    try:
        
        # SQL Query to find requested information     
        searchcommand = "SELECT lat, lon, download, upload, ping, name, sponsor FROM results WHERE tag is '{}'".format(question)
        
        with connect as connection:
                
                cursor.execute(searchcommand)
                result = cursor.fetchall()

        for x in result:
            newresult = x        
            print (newresult)
        
        lookupmap(newresult)
        mainmenu()   
   
    except:
      
        print("There was an error, try again.")
        selection()    
      
# Takes the information that was looked up and deploys it as a map.        
def lookupmap(newresult):
    
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
    
    print("Results launched!")
    mainmenu()
  
# Begins the application
mainmenu()