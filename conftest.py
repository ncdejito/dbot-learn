import pytest
import json


@pytest.fixture
def robot_location() -> dict:
    return json.load(open("tests/fixtures/robot_location.json"))
