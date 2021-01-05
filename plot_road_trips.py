import datetime
import folium
import glob
import gpxpy
import os
import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

last_update_time = datetime.datetime.strptime('2020-08-02', '%Y-%m-%d')

script_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = os.path.join(script_dir, 'data')
road_trips_dir = os.path.join(script_dir, 'road_trips')
gpx_files = glob.glob(os.path.join(data_dir, '*.gpx'))

# gpx_files = gpx_files[:10]

map = folium.Map(location=[37.518943, -122.138206], zoom_start=9)

for gpx_file in glob.glob(os.path.join(road_trips_dir, '*', '*.gpx')):
    print(gpx_file)
    with open(gpx_file, 'r') as f:
        gpx = gpxpy.parse(f)
        data_points = gpx.tracks[0].segments[0].points
        points = [tuple([point.latitude, point.longitude]) for point in data_points]
        folium.PolyLine(points, color="blue", weight=3.0, opacity=1).add_to(map)

        output_html_path = os.path.join(script_dir, 'road_trips.html')
        map.save(output_html_path)

        print('Done. Check the output html: {}'.format(output_html_path))