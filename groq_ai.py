import os

from dotenv import load_dotenv
from groq import Groq


# Load API key
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Create Groq client
groq_client = Groq(api_key=GROQ_API_KEY)


# Send message to AI
def send_message_to_ai(user_message):

    try:

        response = groq_client.chat.completions.create(

            messages=[

                {
                    "role": "user",
                    "content": user_message
                }

            ],

            model="openai/gpt-oss-20b"

        )

        return response.choices[0].message.content

    except Exception as error:

        print(f"Groq API error: {error}")

        return None