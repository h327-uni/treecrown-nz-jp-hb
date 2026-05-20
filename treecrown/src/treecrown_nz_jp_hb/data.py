import requests
import geopandas as gpd
from io import BytesIO
from shapely.geometry import box

BASE_URL = "https://gis.wcc.govt.nz/arcgis/rest/services/Parks/TreeCover/MapServer/57/query"

def load_canopy(bbox):
    """
    Fetches tree canopy polygons from Wellington City Council ArcGIS API.
    """
    params = {
        "where": "1=1",
        "geometry": f"{bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]}",
        "geometryType": "esriGeometryEnvelope",
        "spatialRel": "esriSpatialRelIntersects",
        "inSR": "4326",      
        "outSR": "4326",       
        "outFields": "*",
        "f": "geojson",
    }

    response = requests.get(BASE_URL, params=params, timeout=60)
    response.raise_for_status()

    gdf = gpd.read_file(BytesIO(response.content))
    print(f"Received {len(gdf)} canopy polygons.")
    return gdf


def canopy_coverage(canopy_gdf, bbox):
    """
    Returns the percentage of a bbox area covered by tree canopy.
    bbox: (min_lon, min_lat, max_lon, max_lat)
    """
    # Create the study zone as a polygon
    zone = gpd.GeoDataFrame(geometry=[box(*bbox)], crs="EPSG:4326")

    # Reproject both to a metre-based CRS for accurate area calculation
    # NZTM2000 is appropriate for NZ
    canopy_proj = canopy_gdf.to_crs("EPSG:2193")
    zone_proj = zone.to_crs("EPSG:2193")
    print(zone_proj.total_bounds) 

    # Clip canopy to the zone boundary
    canopy_clipped = gpd.clip(canopy_proj, zone_proj)

    # Calculate areas
    zone_area = zone_proj.geometry.area.sum()
    canopy_area = canopy_clipped.geometry.area.sum()
    print('Canopy area:', canopy_area)
    print('Zone area:', zone_area)
    coverage = (canopy_area / zone_area) * 100
    return round(coverage, 2)


def make_bbox(lon, lat, size_km=0.8):
    """Creates a bbox of approximately size_km × size_km around a point."""
    deg_per_km_lat = 1 / 111.0
    deg_per_km_lon = 1 / (111.0 * 0.64)  
    
    half = size_km / 2
    return (
        lon - half * deg_per_km_lon,
        lat - half * deg_per_km_lat,
        lon + half * deg_per_km_lon,
        lat + half * deg_per_km_lat,
    )


wellington_cbd = (174.7761582968129, -41.29426265278214)
crofton_downs = (174.7651729230385, -41.255317366554046)
johnsonville = (174.80541921449307, -41.219763666942136)

bbox = make_bbox(*wellington_cbd)
canopy = load_canopy(bbox)

print(f"CBD Canopy coverage: {canopy_coverage(canopy, bbox)}%")
