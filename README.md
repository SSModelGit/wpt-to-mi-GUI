# Basic GUI to MI File Converter

## Installation Steps

Installation Steps:
1. Download this repo.
2. Install Pipenv. Alternatively, setup your working Python environment according to your own preference (and risk tolerance).
3. `pip install` requirements. You can either use the provided `Pipfile` or the `requirements.txt` file (the latter is generated from the `Pipfile`).
4. Installed!

## Usage
It's pretty basic, because I'm running this entirely through Folium, but without Javascript. There's a few restrictions and steps, but it should be fairly straightforward.

Steps to run the GUI: Run the `draw_waypoints.py` file. If you're using Pipenv, remember to use `pipenv run draw_waypoints.py` or similar.
1. This will start a Flask application. Open your browser to `127.0.0.1/5000` to access the map GUI.
2. Drag and zoom around the map as you please, to reach the place of interest. Currently, it defaults to opening centered around Buzzards Bay.
3. Add *waypoints* by dropping markers - you can do so with the tab on the left-hand side of the map.
    1. There should be an icon looking like an inverted triangle with a rounded top - click this icon.
    2. Next, click the point on the map where you wish to add a waypoint.
    3. If you don't like where you placed it, there is a trash can symbol which will let you click the marker you dropped to delete.
4. Repeat step c until you've dropped all the waypoints of interest.
5. On the right-hand side, click *Export*. This will let you download a GeoJSON file of all the waypoints. Save this as anything you want - currently, it defaults to `my_plan.geojson`.
    1. Make sure the file ends in `.geojson`!

Steps to generate the .mi file:
1. Run the python file `geoparse.py`. Use Pipenv or another method to run the command `python geoparse.py`, according to your setup.
    1. If it is in the same folder as your waypoints file named `my_plan.geojson`, you can directly run it.
    2. If not, pass in the waypoint file path with the argument `-i`, like `python geoparse.py -i my_plan.geojson`.
3. This will output to terminal the .mi file contents. Copy-paste this to your .mi file.
