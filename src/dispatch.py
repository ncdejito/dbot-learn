from glob import glob
import json
import pandas as pd
import os
import sys

sys.path.append("src/")
import geoutils


class Dispatcher:
    def __init__(self, order_dir="data/orders/", robot_dir="data/robots/"):
        self.order_dir = order_dir
        self.robot_dir = robot_dir
        # self.orders
        # self.robots
        return None

    def _load_data(self, json_dir):
        _files = glob(json_dir + "*.json")
        recs = []
        for _file in _files:
            _dict = json.load(open(_file, "r"))
            if "location" in _dict.keys():
                _dict["lon"] = _dict["location"]["lon"]
                _dict["lat"] = _dict["location"]["lat"]
            recs.append(_dict)
        return pd.DataFrame(recs)

    def _assign(self, order, robot, order_dir, robot_dir):
        "assign robot to order"
        order["robot_id"] = robot["robot_id"]
        robot["order_id"] = order["order_id"]

        # save new
        json.dump(
            order, open(f"{order_dir}assigned/{order['order_id']}.json", "w")
        )
        json.dump(
            robot, open(f"{robot_dir}deployed/{robot['robot_id']}.json", "w")
        )

        # delete old
        os.remove(f"{order_dir}unassigned/{order['order_id']}.json")
        os.remove(f"{robot_dir}standby/{robot['robot_id']}.json")

    def dispatch(self):
        # returns list of info on assigned orders
        # TODO: optimize on proximity, not recency

        unassigned_orders = self._load_data(self.order_dir + "unassigned/")

        recs = []
        for i, row in unassigned_orders.iterrows():
            order = row.to_dict()
            lon, lat = order["pickup"]["lon"], order["pickup"]["lat"]

            # update remaining robots
            standby_robots = self._load_data(self.robot_dir + "standby/")
            if len(standby_robots) > 0:
                # find nearest robot to pickup
                nearest_robot = geoutils.find_nearest(lon, lat, standby_robots)

                self._assign(
                    order, nearest_robot, self.order_dir, self.robot_dir
                )
                self.route(order["order_id"])
                recs.append(order)

        return pd.DataFrame(recs)

    def route(
        self,
        order_id,
        assigned_orders="assigned/",
        routed_orders="routed/",
        deployed_robots="deployed/",
    ):

        input_file = f"{self.order_dir}{assigned_orders}{order_id}.json"
        output_file = f"{self.order_dir}{routed_orders}{order_id}.json"

        order = json.load(open(input_file, "r"))
        robot = json.load(
            open(f"{self.robot_dir}{deployed_robots}{order['robot_id']}.json")
        )

        pickup_route = geoutils.get_route(
            robot["location"]["lon"],
            robot["location"]["lat"],
            order["pickup"]["lon"],
            order["pickup"]["lat"],
        )
        dropoff_route = geoutils.get_route(
            order["pickup"]["lon"],
            order["pickup"]["lat"],
            order["dropoff"]["lon"],
            order["dropoff"]["lat"],
        )

        order["pickup"]["route"] = pickup_route
        order["dropoff"]["route"] = dropoff_route

        json.dump(order, open(output_file, "w"))
        os.remove(input_file)
