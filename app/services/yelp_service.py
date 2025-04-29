# app/services/yelp_service.py
def get_reviews_insights(places: list):
    # For each restaurant in places, call Yelp Fusion API to get reviews and ratings.
    # For simplicity, we attach stubbed review data to each.
    for place in places:
        place["rating"] = 4.5
        place["review_snippet"] = "Excellent ambiance and delightful cuisine!"
    return places
