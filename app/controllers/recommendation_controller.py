# app/controllers/recommendation_controller.py
from fastapi import APIRouter, Query
from app.services.recommendation_service import get_restaurant_recommendations

router = APIRouter()

@router.get("/")
async def recommend_restaurants(
    location: str = Query(..., description="User location (address or city)"),
    number_of_people: int = Query(1, description="Number of people"),
    dietary_pref: str = Query("", description="Dietary preference (e.g., vegan, gluten-free)")
):
    recommendations = get_restaurant_recommendations(location, number_of_people, dietary_pref)
    return recommendations
