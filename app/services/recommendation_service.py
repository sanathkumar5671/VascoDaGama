# app/services/recommendation_service.py
import openai
from app.dspy_integration.dspy_optimizer import generate_recommendation_output
from app.services.osm_service import get_location_details
import json


def get_hotel_recommendations(location: str) -> str:
    location_details = get_location_details(location)
    data = {
        "location": location_details,
        "dietary_preference": "N/A",
        "number_of_people": 2,
        "restaurants": [
            {"name": "Hotels Search", "category": "lodging", "rating": "N/A"}
        ],
    }

    recommendation = generate_recommendation_output(data)

    print("\n=== Hotel Recommendations ===")
    print(f"Location: {location}")
    print("Response:", json.dumps(recommendation, indent=2))
    print("===========================\n")

    if "hotels" in recommendation:
        return "; ".join(
            [
                f"{hotel['name']} ({hotel['rating']} stars): {hotel['brief_reason']}"
                for hotel in recommendation["hotels"]
            ]
        )
    return "Sorry, I couldn't find specific hotel recommendations at this time."


async def get_restaurant_recommendations(
    location: dict, dietary_preference: str, number_of_people: int, restaurants: list
) -> dict:
    """
    Get restaurant recommendations based on provided parameters.

    Args:
        location: Dict containing address, latitude, and longitude
        dietary_preference: String indicating dietary restrictions/preferences
        number_of_people: Integer number of people dining
        restaurants: List of restaurant dictionaries with their details

    Returns:
        dict: Structured recommendation response
    """
    data = {
        "location": location,
        "dietary_preference": dietary_preference,
        "number_of_people": number_of_people,
        "restaurants": restaurants,
    }

    return generate_recommendation_output(data)
