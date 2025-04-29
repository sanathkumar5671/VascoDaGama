# app/dspy_integration/dspy_optimizer.py
import openai
from app.utils.config import OPENAI_API_KEY
import requests

openai.api_key = OPENAI_API_KEY


async def generate_recommendation_output(data: dict) -> dict:
    """
    Accepts aggregated data and uses web search + ChatGPT to generate restaurant recommendations.
    """
    # First, let's search for real restaurants in the location
    search_query = f"best {data['dietary_preference']} restaurants in {data['location']['address']}"

    # Call web search to get real restaurant information
    search_results = web_search(
        search_term=search_query,
        explanation="Searching for real restaurants matching user preferences",
    )

    # Include the search results in our prompt for more accurate recommendations
    prompt = (
        f"You are a knowledgeable local restaurant expert in {data['location']['address']}. "
        "Based on the following real restaurant information and requirements:\n\n"
        f"Search Results: {search_results}\n\n"
        f"Location: {data['location']['address']}\n"
        f"Dietary Requirements: {data['dietary_preference']}\n"
        f"Number of People: {data['number_of_people']}\n\n"
        "Return ONLY a JSON response with 3 REAL restaurants from the search results that best match the criteria. Use this exact format:\n"
        "{\n"
        '  "restaurants": [\n'
        '    {"name": "REAL_RESTAURANT_NAME", "cuisine": "CUISINE_TYPE", "rating": "RATING", "reason": "SHORT_REASON"}\n'
        "  ]\n"
        "}\n\n"
        "Ensure selected restaurants are real (from search results), accommodate the dietary preferences, and suitable for the group size. "
        "Keep reasons concise and specific to each restaurant."
    )

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a restaurant recommendation expert. Use only real restaurants from the provided search results.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        response_format={"type": "json_object"},
    )

    try:
        import json

        recommendation = json.loads(response.choices[0].message.content)
        print(f"Generated recommendations: {json.dumps(recommendation, indent=2)}")
    except Exception as e:
        print(f"Error parsing GPT response: {e}")
        recommendation = {
            "message": "I apologize, but I couldn't generate specific restaurant recommendations at this time."
        }

    return recommendation
