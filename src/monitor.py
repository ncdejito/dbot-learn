import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import pandas as pd
import json
import time
from glob import glob
from typing import List
import sys

sys.path.append("src/")
import navigate
import dispatch

order_dir = "data/orders/routed/"
robot_dir = "data/robots/deployed/"
robot_dir_standby = "data/robots/standby/"


def get_orders():
    routed_orders = glob(f"{order_dir}*.json")
    recs = []
    for order in routed_orders:
        info = json.load(open(order, "r"))
        recs.append(info)

    return recs


def get_ends():
    orders = get_orders()
    lons, lats = [], []

    # if no orders, zoom to manila
    if len(orders) == 0:
        lons += [120.797697, 121.333127]
        lats += [14.352055, 14.812545]

    for order in orders:
        lons.append(order["pickup"]["lon"])
        lons.append(order["dropoff"]["lon"])
        lats.append(order["pickup"]["lat"])
        lats.append(order["dropoff"]["lat"])

    return pd.DataFrame(
        {
            "lon": lons,
            "lat": lats,
        }
    )


def get_routes(status):
    "status in ['pickup','dropoff']"

    orders = get_orders()

    routes = []
    for order in orders:
        pts = order[status]["route"]
        for i in range(len(pts) - 1):
            routes.append(
                {
                    "start": [pts[i][0], pts[i][1], 0],
                    "end": [pts[i + 1][0], pts[i + 1][1], 0],
                    "name": "",
                }
            )

    return routes


def get_robots():
    ICON_URL = "https://raw.githubusercontent.com/googlefonts/noto-emoji/f931bea0efd67aefdf6beae404e1f3150c90314e/svg/emoji_u1f916.svg"
    icon_data = {
        # Icon from Wikimedia, used the Creative Commons Attribution-Share Alike 3.0
        # Unported, 2.5 Generic, 2.0 Generic and 1.0 Generic licenses
        "url": ICON_URL,
        "width": 242,
        "height": 242,
        "anchorY": 242,
    }

    robot_files = glob(f"{robot_dir}*.json")
    robot_files += glob(f"{robot_dir_standby}*.json")
    recs = []
    for robot_file in robot_files:
        info = json.load(open(robot_file, "r"))
        info["lon"] = info["location"]["lon"]
        info["lat"] = info["location"]["lat"]
        recs.append(info)
    robots = pd.DataFrame(recs)
    # robots = pd.read_json("robot_location.json", orient="index").transpose()
    # robots = pd.DataFrame([(0,0)],columns=['lon', 'lat'])

    robots["icon_data"] = None
    robots["icon_data"] = np.repeat(icon_data, len(robots))
    return robots


ends = get_ends()
routes_pickup = get_routes("pickup")
routes_dropoff = get_routes("dropoff")
robots = get_robots()
ends_layer = pdk.Layer(
    "ScatterplotLayer",
    data=ends,
    get_position="[lon, lat]",
    get_color="[200, 30, 0, 160]",
    get_radius=200,
)
routes_layer_pickup = pdk.Layer(
    "LineLayer",
    routes_pickup,
    get_source_position="start",
    get_target_position="end",
    get_color=[160, 160, 160],
    get_width=5,
    highlight_color=[255, 255, 0],
    picking_radius=10,
    auto_highlight=True,
    pickable=True,
)
routes_layer_dropoff = pdk.Layer(
    "LineLayer",
    routes_dropoff,
    get_source_position="start",
    get_target_position="end",
    get_color=[95, 93, 94],
    get_width=5,
    highlight_color=[255, 255, 0],
    picking_radius=10,
    auto_highlight=True,
    pickable=True,
)
robots_layer = pdk.Layer(
    type="IconLayer",
    data=robots,
    get_icon="icon_data",
    get_size=4,
    size_scale=15,
    get_position=["lon", "lat"],
    pickable=True,
)


def get_view(ends):
    return pdk.data_utils.viewport_helpers.compute_view(
        points=ends, view_proportion=2
    )


map_settings = pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state=pdk.data_utils.viewport_helpers.compute_view(
        points=ends, view_proportion=2
    ),
    layers=[
        routes_layer_pickup,
        routes_layer_dropoff,
        ends_layer,
        robots_layer,
    ],
)

map = st.pydeck_chart(map_settings)


dispatcher = dispatch.Dispatcher(
    order_dir="data/orders/", robot_dir="data/robots/"
)
i = 0
while True:
    # backend
    i += 1
    print(i)
    print("dispatch")
    df = dispatcher.dispatch()
    # Initialize robots
    robots_ = []
    robot_files = glob(f"{robot_dir}*.json")
    for robot_file in robot_files:
        robot = navigate.Robot(robot_file)
        robots_.append(robot)

    for robot in robots_:
        print("robot move")
        robot.move()

    # frontend
    print("get map")
    ends = get_ends()
    routes_pickup = get_routes("pickup")
    routes_dropoff = get_routes("dropoff")
    robots = get_robots()
    ends_layer.data = ends
    routes_layer_pickup.data = routes_pickup
    routes_layer_dropoff.data = routes_dropoff
    robots_layer.data = robots
    map_settings.initial_view_state = get_view(ends)
    map_settings.update()
    map.pydeck_chart(map_settings)
    time.sleep(0.5)


# locs = [
#      (120.957222, 14.640070), waypoint=4
#      (120.962439, 14.644664),
#      (120.973810, 14.645061),
# ]


# while True:
#     navigate.navigate()
#     robot_loc = read_loc()
#     robot_layer.data = robot_loc
#     r.update()
#     map.pydeck_chart(r)
#     time.sleep(0.05)
