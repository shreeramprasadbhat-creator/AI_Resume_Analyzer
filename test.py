import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

key = os.getenv("GEMINI_API_KEY")

print("Key found:", key is not None)
print("Key length:", len(key) if key else 0)

genai.configure(api_key=key)

model = genai.GenerativeModel("gemini-2.5-flash")

try:
    response = model.generate_content("Say hello.")
    print(response.text)
except Exception as e:
    print("ERROR:", e)