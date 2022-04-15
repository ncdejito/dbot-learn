from scipy.spatial import KDTree
import numpy as np
import pandas as pd
from typing import List
import json
import requests
from typing import Dict

R = 6367


def get_route(
    lon1: float, lat1: float, lon2: float, lat2: float, debug: bool = False
) -> List[list]:
    "move from 1 to 2"
    request = f"http://router.project-osrm.org/route/v1/foot/{lon1},{lat1};{lon2},{lat2}?geometries=geojson"

    res = requests.get(request)
    results = json.loads(res.content)
    if debug:
        results["request"] = request
        return results

    if results["code"] == "Ok":
        route = results["routes"][0]["geometry"]["coordinates"]
    else:
        route = None

    return route


def lonlat_to_cartesian(data: pd.DataFrame) -> pd.DataFrame:
    phi = np.deg2rad(data["lat"])
    theta = np.deg2rad(data["lon"])
    data["x"] = R * np.cos(phi) * np.cos(theta)
    data["y"] = R * np.cos(phi) * np.sin(theta)
    data["z"] = R * np.sin(phi)
    return data[["x", "y", "z"]]


def find_nearest(
    lon: float,
    lat: float,
    neighbors: pd.DataFrame,
    k: int = 1,
    debug: bool = False,
) -> Dict[int, str]:
    df = pd.DataFrame({"lon": lon, "lat": lat}, index=[0])
    kd3 = KDTree(lonlat_to_cartesian(neighbors))
    distance, index = kd3.query(lonlat_to_cartesian(df), k=k)
    if debug:
        return {
            "index": index,
            "distance": distance,
            "results": neighbors.iloc[index[0], :].to_dict(),
        }

    return neighbors.iloc[index[0], :].to_dict()
