import pandas as pd
import os
import shutil

import json
from src.dispatch import Dispatcher


order_dir = "tests/fixtures/orders/"
robot_dir = "tests/fixtures/robots/"


class TestDispatcher:
    def _setup_order(self):
        shutil.copy2(
            f"{order_dir}initial/2d3ae2dd-8648-4005-bccd-9d812bd55a80.json",
            f"{order_dir}unassigned/2d3ae2dd-8648-4005-bccd-9d812bd55a80.json",
        )

    def _setup_robot(self):
        shutil.copy2(
            f"{robot_dir}initial/crazy-dandelion.json",
            f"{robot_dir}standby/crazy-dandelion.json",
        )

    def _reset_order(self):
        os.remove(
            f"{order_dir}assigned/2d3ae2dd-8648-4005-bccd-9d812bd55a80.json"
        )

    def _reset_robot(self):
        os.remove(f"{robot_dir}deployed/crazy-dandelion.json")

    def _setup(self):
        self._setup_order()
        self._setup_robot()

    def _reset(self):
        self._reset_order()
        self._reset_robot()

    def _reset2(self):
        os.remove(
            f"{order_dir}routed/2d3ae2dd-8648-4005-bccd-9d812bd55a80.json"
        )
        self._reset_robot()

    def test_load_data(self):
        dispatcher = Dispatcher()
        df = dispatcher._load_data(json_dir="tests/fixtures/robots/initial/")
        assert len(df) == 2

    def test_assign(self):

        self._setup()
        order = {
            "robot_id": "",
            "order_id": "2d3ae2dd-8648-4005-bccd-9d812bd55a80",
        }
        robot = {
            "robot_id": "crazy-dandelion",
            "order_id": "",
        }
        dispatcher = Dispatcher()
        dispatcher._assign(order, robot, order_dir, robot_dir)

        # json files moved
        order_file = f"{order_dir}assigned/{order['order_id']}.json"
        robot_file = f"{robot_dir}deployed/{robot['robot_id']}.json"
        assert os.path.exists(order_file)
        assert os.path.exists(robot_file)

        # tagged correctly
        order2 = json.load(open(order_file, "r"))
        robot2 = json.load(open(robot_file, "r"))
        assert order2["robot_id"] != ""
        assert robot2["order_id"] != ""

        self._reset()

    def test_dispatch(self):
        # working case
        self._setup()
        dispatcher = Dispatcher(order_dir, robot_dir)
        df = dispatcher.dispatch()
        self._reset2()
        assert len(df) == 1

    def test_dispatch_with_no_robots(self):
        # no robots are available, loop on standby
        self._setup_order()
        dispatcher = Dispatcher(order_dir, robot_dir)
        df = dispatcher.dispatch()
        os.remove(
            f"{order_dir}unassigned/2d3ae2dd-8648-4005-bccd-9d812bd55a80.json"
        )
        assert len(df) == 0

    def test_dispatch_with_no_orders(self):
        # no orders are available, loop on standby
        self._setup_robot()
        dispatcher = Dispatcher(order_dir, robot_dir)
        df = dispatcher.dispatch()
        os.remove(f"{robot_dir}standby/crazy-dandelion.json")
        assert len(df) == 0

    def test_route(self):
        # TODO: what if robot is too far away?
        order_id = "2d3ae2dd-8648-4005-bccd-9d812bd55a80"
        robot_id = "crazy-dandelion"
        test_dir = "tests/fixtures/"
        routed_orders = test_dir + "orders/routed/"
        assigned_orders = test_dir + "orders/assigned/"
        deployed_robots = test_dir + "robots/deployed/"
        order = json.load(
            open(test_dir + f"orders/initial/{order_id}.json", "r")
        )
        robot = json.load(
            open(test_dir + f"robots/initial/{robot_id}.json", "r")
        )
        order["robot_id"] = robot_id

        json.dump(order, open(f"{assigned_orders}{order_id}.json", "w"))
        json.dump(robot, open(f"{deployed_robots}{robot_id}.json", "w"))
        dispatcher = Dispatcher(test_dir + "orders/", test_dir + "robots/")
        dispatcher.route(order_id)

        output_file = f"{routed_orders}{order_id}.json"
        order = json.load(open(output_file, "r"))
        os.remove(output_file)
        os.remove(f"{deployed_robots}{robot_id}.json")

        assert order["pickup"]["route"] != ""
        assert order["dropoff"]["route"] != ""
