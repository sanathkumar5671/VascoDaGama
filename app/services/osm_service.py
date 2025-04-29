# app/services/osm_service.py
def get_location_details(location: str):
    # Call Nominatim API to get latitude/longitude for the location.
    # Then, optionally, use Overpass API to fetch points-of-interest.
    # For now, we return a stubbed response.
    return {
        "address": location,
        "latitude": 40.7128,
        "longitude": -74.0060,
        "bounding_box": [40.70, -74.02, 40.72, -73.99]
    }
