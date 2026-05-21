"""This package will show a coverage percentage for three suburbs, and a shaded walk map for one route."""

from __future__ import annotations
# import pandas as pd

__version__ = "0.1.0"


def load_canopy(bbox):
    """Fetches the Auckland Council canopy layer from LINZ for a given bounding box and returns a GeoDataFrame of canopy polygons."""
    raise NotImplementedError


def canopy_coverage(area_gdf):
    """Computes the percentage of each input polygon covered by canopy."""
    raise NotImplementedError


def route_shade(route_gdf, buffer_m):
    """Buffers each edge of a route by a given distance (in metres) and returns the canopy fraction within that buffer, a proxy for pedestrian shade."""
    raise NotImplementedError

