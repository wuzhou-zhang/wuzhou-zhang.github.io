import folium
import glob
import gpxpy
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

script_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = os.path.join(script_dir, 'data')
gpx_files = glob.glob(os.path.join(data_dir, '*.gpx'))

# gpx_files = gpx_files[:1]

map = folium.Map(location=[37.518943, -122.138206], zoom_start=10)

for idx, gpx_file in enumerate(gpx_files):
    with open(gpx_file, 'r') as f:
        gpx = gpxpy.parse(f)
        data_points = gpx.tracks[0].segments[0].points
        hike_name = gpx.tracks[0].name
        print("{}: {}".format(idx, hike_name))

        start_point = data_points[0]
        start_time = start_point.time
        popup_text = '<b>{}</b><br>{}'.format(hike_name, start_time)
        folium.Marker([start_point.latitude, start_point.longitude], popup=popup_text).add_to(map)

        points = [tuple([point.latitude, point.longitude]) for point in data_points]
        folium.PolyLine(points, color="blue", weight=1.5, opacity=1).add_to(map)

output_html_path = os.path.join(script_dir, 'index.html')
map.save(output_html_path)

map.get_root().html.add_child(
    folium.Element("<h1>Wuzhou's {} Hikes in Bay Area (and Beyond)</h1>".format(len(gpx_files)))
)

print 'Done. Check the output html: {}'.format(output_html_path)
