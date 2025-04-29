from fastapi import APIRouter, Form, Request, Response
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Gather
from app.services.voice_service import process_speech_input
from app.utils.config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER

router = APIRouter()
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


@router.api_route("/answer_call", methods=["GET", "POST"])
async def answer_call(request: Request):
    response = VoiceResponse()
    gather = Gather(
        input="speech", action="/voice/process_location", speechTimeout="auto"
    )
    gather.say(
        "Hi! I'm your restaurant finder. Please tell me your location.",
        voice="Polly.Joanna",
        language="en-US",
    )
    response.append(gather)
    return Response(content=str(response), media_type="application/xml")


@router.api_route("/process_location", methods=["GET", "POST"])
async def process_location(SpeechResult: str = Form(None), CallSid: str = Form(None)):
    response = VoiceResponse()
    if not SpeechResult:
        response.say(
            "Sorry, I didn't catch that. Please try again.", voice="Polly.Joanna"
        )
        return Response(content=str(response), media_type="application/xml")

    print(f"Location received: {SpeechResult}, CallSid: {CallSid}")  # Debug log

    # Store location - add await here
    await process_speech_input(SpeechResult, stage="location", call_sid=CallSid)

    gather = Gather(
        input="speech", action="/voice/process_dietary", speechTimeout="auto"
    )
    gather.say(
        "Got it! What are your dietary preferences? For example, vegetarian, vegan, or no preference.",
        voice="Polly.Joanna",
        language="en-US",
    )
    response.append(gather)
    return Response(content=str(response), media_type="application/xml")


@router.api_route("/process_dietary", methods=["GET", "POST"])
async def process_dietary(SpeechResult: str = Form(None), CallSid: str = Form(None)):
    response = VoiceResponse()
    if not SpeechResult:
        response.say(
            "Sorry, I didn't catch that. Please try again.", voice="Polly.Joanna"
        )
        return Response(content=str(response), media_type="application/xml")

    print(f"Dietary preference received: {SpeechResult}, CallSid: {CallSid}")

    # Store dietary preference - add await here
    await process_speech_input(SpeechResult, stage="dietary", call_sid=CallSid)

    gather = Gather(
        input="speech", action="/voice/process_people", speechTimeout="auto"
    )
    gather.say(
        "Great! And how many people will be dining?",
        voice="Polly.Joanna",
        language="en-US",
    )
    response.append(gather)
    return Response(content=str(response), media_type="application/xml")


@router.api_route("/process_people", methods=["GET", "POST"])
async def process_people(SpeechResult: str = Form(None), CallSid: str = Form(None)):
    response = VoiceResponse()
    if not SpeechResult:
        response.say(
            "Sorry, I didn't catch that. Please try again.", voice="Polly.Joanna"
        )
        return Response(content=str(response), media_type="application/xml")

    print(f"Number of people received: {SpeechResult}, CallSid: {CallSid}")  # Debug log

    # Await the async process_speech_input
    answer = await process_speech_input(SpeechResult, stage="people", call_sid=CallSid)
    if not answer or answer == "I'm sorry, I couldn't process that request.":
        response.say(
            "I apologize, but I couldn't process your request. Please try calling again.",
            voice="Polly.Joanna",
        )
    else:
        response.say(answer, voice="Polly.Joanna", language="en-US")
    return Response(content=str(response), media_type="application/xml")


@router.get("/make_call")
def make_call():
    call = client.calls.create(
        url="https://a4d9-2401-4900-1cbc-6648-e05d-4122-fb2e-4234.ngrok-free.app/voice/answer_call",
        to="+918971754926",
        from_=TWILIO_PHONE_NUMBER,
    )
    return {"call_sid": call.sid}
