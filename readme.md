# Hollowlake SpeedTest

## Application Details

### Synopsis
This is an internet speedtest program with a few added features just for "cool" factor. It was created with the intention of just teaching me some things about Python and using some additional APIs, modules, and the like. 

### Extra Features
At the core, this is just a speedtest program. However, to give myself more coding practice I decided to add a few additional features. 

- Database
A database was added using sqlite3 to store the information returned during the speedtest. This information can be accessed by the program to pull up old test results. 

- Folium Maps
The addition of folium allows a map to be displayed via the webbrowser library. When the database is queried, the user has the option of launching a map for a more "graphical" interface. 

## Screenshots

![image]('/screenshots/mainmenu.png')
![image]('/screenshots/testcompletion.png')
![image]('/screenshots/database.png')
![image]('/screenshots/search.png')
![image]('/screenshots/tagsearch.png')
![image]('/screenshots/map.png')

## Problems
I'm sure there are several issues in the code but at the moment there's really only one that bothers me. 

When the user runs the code and a map is generated, I have yet to figure out how to immediately display the information without first generating a file to use. My current work around is that a file is created, displayed and then immediately deleted. As long as the window remains open, the file will be displayed but once the window is closed the file is gone. I'm sure there's a way to do it, I just haven't found it yet. 

## Future Plans
I intend to keep using this project as a means to learn. I'm sure there are plenty of other ways to do things that I've implemented and ways to make the program faster, smaller, and more efficient. I'm sure I'll do some more rewrites as I learn other things and play with it. 

Eventually, I'd like to make a GUI using PyQt that will allow users to run the test, view the map and the database as well as view maps and results from previous tests at the click of a button. One thing at a time though. 

