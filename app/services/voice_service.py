import openai
from app.services.recommendation_service import get_restaurant_recommendations
from app.utils.config import OPENAI_API_KEY
from app.services.osm_service import get_location_details
import re

openai.api_key = OPENAI_API_KEY

# Dictionary to store conversation state
conversation_state = {}


def extract_number(text: str) -> int:
    """Extract the first number from text"""
    numbers = re.findall(r"\d+", text)
    return int(numbers[0]) if numbers else 2  # Default to 2 if no number found


async def process_speech_input(
    speech_text: str, stage: str = None, call_sid: str = None
) -> str:
    print(f"\nProcessing speech input - Stage: {stage}, CallSid: {call_sid}")
    print(f"Speech text: {speech_text}")

    # Initialize or get conversation state
    if call_sid not in conversation_state:
        conversation_state[call_sid] = {}
        print(f"Initialized new conversation state for CallSid: {call_sid}")

    state = conversation_state[call_sid]
    print(f"Current state: {state}")

    if stage == "location":
        state["location"] = get_location_details(speech_text)
        print(f"Stored location: {state['location']}")
        return None
    elif stage == "dietary":
        state["dietary_preference"] = speech_text
        print(f"Stored dietary preference: {state['dietary_preference']}")
        return None
    elif stage == "people":
        try:
            state["number_of_people"] = extract_number(speech_text)
            print(f"Stored number of people: {state['number_of_people']}")

            # Verify we have all required data
            if not all(
                k in state
                for k in ["location", "dietary_preference", "number_of_people"]
            ):
                print(f"Missing required data. Current state: {state}")
                return (
                    "I'm sorry, some information is missing. Please try calling again."
                )

            data = {
                "location": state["location"],
                "dietary_preference": state["dietary_preference"],
                "number_of_people": state["number_of_people"],
                "restaurants": [
                    {
                        "name": "Local Restaurant",
                        "category": "restaurant",
                        "rating": "4.5",
                    }
                ],
            }
            print(f"Preparing recommendation request with data: {data}")

            # Await the async recommendation function
            recommendations = await get_restaurant_recommendations(
                location=data["location"],
                dietary_preference=data["dietary_preference"],
                number_of_people=data["number_of_people"],
                restaurants=data["restaurants"],
            )

            # Clear the state after getting recommendations
            del conversation_state[call_sid]
            print(f"Generated recommendations and cleared state: {recommendations}")

            return format_recommendation_response(recommendations)
        except Exception as e:
            print(f"Error processing people stage: {str(e)}")
            return (
                "I'm sorry, I couldn't process the number of people. Please try again."
            )

    print("No matching stage found")
    return "I'm sorry, I couldn't process that request."


def format_recommendation_response(recommendations: dict) -> str:
    if "restaurants" in recommendations:
        return "; ".join(
            [
                f"{rest['name']} ({rest['cuisine']} cuisine, {rest['rating']} stars): {rest['reason']}"
                for rest in recommendations["restaurants"]
            ]
        )
    return (
        "I'm sorry, I couldn't find specific restaurant recommendations at this time."
    )
