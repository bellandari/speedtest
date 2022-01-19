import speedtest
import folium
import json
import time
import os.path
import directories

# Speed Test Variable for shortening
test = speedtest.Speedtest()

# Time Stamp used to save as file names
timestr = time.strftime("%Y%m%d-%H%M%S")

# Where and how to save json and html files
completemap = os.path.join(directories.directory, timestr+'.html')
completejson = os.path.join(directories.directoryjson, timestr+'.json')

#locates the best server
print("Finding the best server...")
best = test.get_best_server()

# Takes that information and pretty formats it for the JSON file
info = json.dumps(best, indent=4, sort_keys=True)

#Takes the dumped information and loads it so Python can pull the information for use
intel = json.loads(info)

# Pulls coordinates from the JSON file
lat = intel["lat"]
lon = intel["lon"]

# Formats those coordinates to be used as argument in folium module
coordinates = (lat, lon)

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

# Generates map with testing location
map = folium.Map(coordinates, zoom_start=15)

# Map popup configuration, makes popup with results
overall = (f"Download: {dread} / Upload: {uread} / Ping: {pread}")
popup = folium.Popup(overall, max_width=400,min_width=100)
folium.Marker(coordinates, popup = popup).add_to(map)

# Saves map as html file in the maps folder
map.save(completemap)

# Takes previous JSON and writes to JSON file
data = open(completejson, "w")
data.write(info)
data.close()

# Opens the JSON file, and adds the download, upload, and ping results to it
with open (completejson, 'r') as f:
    update = json.loads(f.read())
    
    update["Download"] = dread
    update["Upload"] = uread
    update["Ping"] = pread
    
with open (completejson, 'w') as f:
    f.write(json.dumps(update, sort_keys=True, indent=4))