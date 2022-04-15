import json
import math
from haversine import haversine, inverse_haversine


class Robot:
    def __init__(self, filepath):
        self.filepath = filepath

    def refresh(self):
        "reads json instructions from dispatcher"
        info = json.load(open(self.filepath, "r"))
        self.location = info["location"]
        self.status = info["status"]
        self.waypoint = info["waypoint"]
        self.order_id = info["order_id"]
        self.robot_id = info["robot_id"]
        order_path = self.filepath.replace(
            self.robot_id, self.order_id
        ).replace("robots/deployed", "orders/routed")
        order = json.load(open(order_path, "r"))
        self.route = ""
        if self.status in ["pickup", "dropoff"]:
            self.route = order[self.status]["route"]
            self.end_lon = order[self.status]["lon"]
            self.end_lat = order[self.status]["lat"]

        return None

    def navigate(self):
        STEP_SIZE = 0.05  # in km

        lon = self.location["lon"]
        lat = self.location["lat"]

        # which part pursued in route
        wpt = self.waypoint
        route = self.route
        goal_lon, goal_lat = tuple(route[wpt])

        # move to waypoint
        direction = math.atan2((goal_lon - lon), (goal_lat - lat))
        new_lat, new_lon = inverse_haversine((lat, lon), STEP_SIZE, direction)

        # check distance to goal
        distance_to_goal = haversine((goal_lat, goal_lon), (lat, lon))
        if distance_to_goal < STEP_SIZE:
            # if end of route
            if wpt == len(route) - 1:
                # change robot status
                stat_num = {0: "standby", 1: "pickup", 2: "dropoff"}
                stat_word = {y: x for x, y in stat_num.items()}
                current_status = stat_word[self.status]
                new_status = current_status + 1
                if new_status == 3:
                    new_status = 0
                self.status = stat_num[new_status]
                self.waypoint = 0
            else:
                self.waypoint = wpt + 1  # min(len(route) - 1, )

        self.location["lon"] = new_lon
        self.location["lat"] = new_lat

    def update_status(self):
        "overwrites json file with new status"
        json.dump(self.__dict__, open(self.filepath, "w"))

    def move(self):
        self.refresh()
        if self.status != "standby":
            self.navigate()
            self.update_status()
