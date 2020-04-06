import datetime
import folium
import glob
import gpxpy
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

script_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = os.path.join(script_dir, 'data')
road_trips_dir = os.path.join(script_dir, 'road_trips')
gpx_files = glob.glob(os.path.join(data_dir, '*.gpx'))

# gpx_files = gpx_files[:10]

map = folium.Map(location=[37.518943, -122.138206], zoom_start=9)

for gpx_file in glob.glob(os.path.join(road_trips_dir, '*', '*.gpx')):
    print gpx_file
    with open(gpx_file, 'r') as f:
        gpx = gpxpy.parse(f)
        data_points = gpx.tracks[0].segments[0].points
        points = [tuple([point.latitude, point.longitude]) for point in data_points]
        folium.PolyLine(points, color="blue", weight=3.0, opacity=1).add_to(map)

        output_html_path = os.path.join(script_dir, 'road_trips.html')
        map.save(output_html_path)

newest_start_time = None
newest_hike_name = None
gpx_list = []
for idx, gpx_file in enumerate(gpx_files):
    with open(gpx_file, 'r') as f:
        gpx = gpxpy.parse(f)
        gpx_list.append(gpx)
        data_points = gpx.tracks[0].segments[0].points
        hike_name = gpx.tracks[0].name
        print("Parsed {}: {}".format(idx, hike_name))
        start_point = data_points[0]
        start_time = start_point.time
        if start_time is None:
           start_time = datetime.datetime.strptime(hike_name[-len('YYYY-MM-DD'):], '%Y-%m-%d')
        if newest_start_time is None or newest_start_time < start_time:
            newest_start_time = start_time
            newest_hike_name = hike_name
print('Newest hike:', newest_hike_name, newest_start_time)

for idx, gpx in enumerate(gpx_list):
    data_points = gpx.tracks[0].segments[0].points
    hike_name = gpx.tracks[0].name
    print("Plotting {}: {}".format(idx, hike_name))
    if 'Estate' in hike_name:
        continue

    start_point = data_points[0]
    start_time = start_point.time
    if start_time is None:
        start_time = datetime.datetime.strptime(hike_name[-len('YYYY-MM-DD'):], '%Y-%m-%d')
    print start_time
    popup_text = '<b>{}</b><br>{}'.format(hike_name, start_time.strftime('%Y-%m-%d'))
    folium.Marker([start_point.latitude, start_point.longitude], popup=popup_text).add_to(map)

    points = [tuple([point.latitude, point.longitude]) for point in data_points]
    if hike_name == newest_hike_name:
        folium.PolyLine(points, color="red", weight=3.0, opacity=1).add_to(map)
    else:
        folium.PolyLine(points, color="blue", weight=3.0, opacity=1).add_to(map)

output_html_path = os.path.join(script_dir, 'index.html')
map.save(output_html_path)

map.get_root().html.add_child(
    folium.Element("<h1>Wuzhou's {} Hikes in Bay Area (and Beyond)</h1>".format(len(gpx_files)))
)

print('Done. Check the output html: {}'.format(output_html_path))
