# EchoSense AI

EchoSense AI is a voice-enabled restaurant finder application that helps users find restaurants based on their location, dietary preferences, and party size through natural voice interactions.

## Features

- Voice-based interaction using Twilio
- Natural language processing for understanding user preferences
- Multi-stage conversation flow for gathering restaurant requirements
- Real-time restaurant recommendations based on user input

## Project Structure

```
app/
├── controllers/     # API endpoints and route handlers
├── services/        # Business logic and service implementations
├── models/          # Data models and schemas
├── utils/           # Utility functions and helpers
├── dspy_integration/# DSPy integration components
└── main.py          # Application entry point
```

## Prerequisites

- Python 3.8+
- Twilio account with Voice capabilities
- ngrok or similar tunneling service for local development

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd <project-directory>
```

2. Create and activate a virtual environment:

```bash
python -m venv vascoenv
source vascoenv/bin/activate  # On Windows: vascoenv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up environment variables:
   Create a `.env` file with the following variables:

```
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=your_twilio_phone_number
```

## Usage

1. Start the application:

```bash
python app/main.py
```

2. Start ngrok to expose your local server:

```bash
ngrok http 8000
```

3. Update your Twilio webhook URL to point to your ngrok URL:

```
https://your-ngrok-url/voice/answer_call
```

4. Call your Twilio phone number to interact with the restaurant finder.

## API Endpoints

- `/voice/answer_call` - Initial call handling
- `/voice/process_location` - Process user's location input
- `/voice/process_dietary` - Process dietary preferences
- `/voice/process_people` - Process number of people
- `/voice/make_call` - Initiate outbound calls

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Twilio for voice capabilities
- FastAPI for the web framework
- DSPy for language model integration
