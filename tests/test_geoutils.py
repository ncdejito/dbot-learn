from src.geoutils import get_route, lonlat_to_cartesian, find_nearest
import pytest
import pandas as pd


@pytest.fixture
def locations(robot_location) -> pd.DataFrame:
    recs = [robot_location]
    for step in [0.001, 0.01]:
        d = robot_location.copy()
        d["lon"] = d["lon"] + step
        recs.append(d)
    return pd.DataFrame(recs)


@pytest.mark.parametrize(
    "lon1, lat1, lon2, lat2, expected",
    [
        # within land, < eta
        (120.9635254, 14.6348514, 121.0254764, 14.565466, "has route"),
        # within land, > eta
        (120.9635254, 14.6348514, 120.603512, 18.193721, "no route"),
        # within land same point
        (
            120.9635254,
            14.6348514,
            120.9635254,
            14.6348514,
            "no route",
        ),
        # from land to sea point
        (
            126.478794,
            16.155694,
            120.9635254,
            14.6348514,
            "no route",
        ),
        # points at sea but near
        (
            126.478794,
            16.155694,
            126.453182,
            16.131860,
            "no route",
        ),
    ],
)
def test_get_route(lon1, lat1, lon2, lat2, expected):
    "route must be reachable within ETA"
    eta = 1800  # in seconds
    results = get_route(lon1, lat1, lon2, lat2, debug=True)
    print(results["request"])
    if 0 < results["routes"][0]["duration"] <= eta:
        r = "has route"
    else:
        r = "no route"
    assert r == expected


def test_lonlat_to_cartesian(locations):
    df2 = lonlat_to_cartesian(locations)
    assert len({"x", "y", "z"} - set(df2.columns)) == 0


def test_find_nearest(locations):
    lon = locations.loc[0, "lon"]
    lat = locations.loc[0, "lat"]
    neighbors = locations.loc[1:, :].copy()
    d = find_nearest(lon, lat, neighbors, k=1, debug=True)
    assert d["index"] == [0]
