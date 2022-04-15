import shutil
import os
import json
from src.navigate import Robot

filepath = "tests/fixtures/robots/deployed/crazy-dandelion.json"


def _setup():

    info = json.load(
        open("tests/fixtures/robots/initial/crazy-dandelion.json", "r")
    )
    info["order_id"] = "2d3ae2dd-8648-4005-bccd-9d812bd55a80"
    json.dump(
        info, open("tests/fixtures/robots/deployed/crazy-dandelion.json", "w")
    )
    shutil.copy2(
        "tests/fixtures/2d3ae2dd-8648-4005-bccd-9d812bd55a80_routed.json",
        "tests/fixtures/orders/routed/2d3ae2dd-8648-4005-bccd-9d812bd55a80.json",
    )


def _reset():
    os.remove(
        "tests/fixtures/orders/routed/2d3ae2dd-8648-4005-bccd-9d812bd55a80.json"
    )
    os.remove("tests/fixtures/robots/deployed/crazy-dandelion.json")


def equate_2lists(list1, list2):
    list1.sort()
    list2.sort()
    for x, y in zip(list1, list2):
        assert x == y


class TestRobot:
    def test_refresh(self):
        _setup()
        robot = Robot(filepath)
        robot.refresh()
        equate_2lists(
            list(robot.__dict__.keys()),
            # expected contents
            [
                "filepath",
                "location",
                "status",
                "waypoint",
                "order_id",
                "robot_id",
                "route",
                "end_lon",
                "end_lat",
            ],
        )
        _reset()

    def test_navigate(self):
        _setup()
        robot = Robot(filepath)
        robot.refresh()
        old_lon = robot.location["lon"]
        old_lat = robot.location["lat"]
        robot.navigate()
        new_lon = robot.location["lon"]
        new_lat = robot.location["lat"]
        assert new_lon != old_lon
        assert new_lat != old_lat
        _reset()

    def test_update_status(self):
        _setup()
        robot = Robot(filepath)
        new = filepath.replace(".json", "_test.json")
        robot = Robot(new)
        robot.update_status()
        assert os.path.exists(new)
        os.remove(new)
        _reset()

    def test_move(self):
        _setup()
        robot = Robot(filepath)
        robot.refresh()
        old_lon = robot.location["lon"]
        old_lat = robot.location["lat"]
        robot.move()
        new_lon = robot.location["lon"]
        new_lat = robot.location["lat"]
        assert new_lon != old_lon
        assert new_lat != old_lat
        _reset()
