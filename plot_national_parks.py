import csv
import folium
import glob
import gpxpy
import os
import sys

if(sys.version_info.major>=3):
    def reload(MODULE):        
        import importlib
        importlib.reload(MODULE)
else:
    reload(sys)
    sys.setdefaultencoding('utf-8')

script_dir = os.path.dirname(os.path.realpath(__file__))
csv_file = os.path.join(script_dir, 'national_parks.csv')


class NationalPark:

    def __init__(self, name, lat, lon, location, visited, num_of_visits):
        self.name = name
        self.lat = float(lat)
        self.lon = float(lon)
        self.location = location
        self.visited = visited
        self.num_of_visits = num_of_visits


national_park_list = []
with open(csv_file) as f:
    csv_reader = csv.reader(f)
    for row in csv_reader:
        print(row)
        if row[0] == 'name':
            continue
        national_park_list.append(NationalPark(*row))


map = folium.Map(location=[45.023835, -112.037200], zoom_start=4)
for national_park in national_park_list:
    # popup_text = '<b>{}</b><br>{}'.format(hike_name, start_time.strftime('%Y-%m-%d'))
    popup_text = '<b>{}</b><br>{}'.format(national_park.name, national_park.location)

    # print national_park.lat, national_park.lon
    if national_park.visited == 'YES':
        icon = folium.Icon(color='blue', icon_color='white', icon='map-marker')
    else:
        icon = folium.Icon(color='red', icon_color='white', icon='map-marker')
    folium.Marker([national_park.lat, national_park.lon], popup=popup_text, icon=icon).add_to(map)

output_html_path = os.path.join(script_dir, 'nps.html')
map.save(output_html_path)

print('Done. Check the output html: {}'.format(output_html_path))
