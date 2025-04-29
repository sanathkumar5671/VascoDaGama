# app/services/foursquare_service.py
def get_trending_places(location_data: dict):
    # Use Foursquare Places API with location_data (latitude, longitude, bounding box)
    # Return a list of trending restaurant candidates.
    return [
        {"name": "The Trendy Spoon", "venue_id": "123", "category": "Restaurant"},
        {"name": "Hip Eatery", "venue_id": "456", "category": "Restaurant"},
        {"name": "Modern Bites", "venue_id": "789", "category": "Restaurant"},
    ]
