import os
import requests
import json
from google import genai

# GitHub Settings (Secrets) se safe tarike se keys load karne ke liye
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GREEN_API_ID = os.getenv("GREEN_API_ID")
GREEN_API_TOKEN = os.getenv("GREEN_API_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def get_gk_question_from_ai():
    """Generates a new dynamic SSC GK question using Gemini AI Studio"""
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    prompt = (
        "Generate exactly one unique, high-quality and important GK/Static GK question for the SSC exam in Hindi and English (Bilingual). "
        "Provide exactly 3 multiple-choice options. The first option must start with the 👍 emoji, the second with 🙏, and the third with ❤️. "
        "Return the output STRICTLY in JSON format with keys: 'question' and 'options' (which is a list of 3 strings). "
        "Do not include any markdown formatting like ```json or trailing text."
    )
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt
    )
    
    clean_text = response.text.strip()
    if clean_text.startswith("```json"):
        clean_text = clean_text.replace("```json", "").replace("```", "").strip()
    elif clean_text.startswith("```"):
        clean_text = clean_text.replace("```", "").strip()
        
    data = json.loads(clean_text)
    return data['question'], data['options']

def send_whatsapp_poll(question, options):
    """Sends the poll directly to your WhatsApp via Green-API"""
    url = f"https://api.green-api.com/waInstance{GREEN_API_ID}/sendPoll/{GREEN_API_TOKEN}"
    
    payload = {
        "chatId": CHAT_ID,
        "options": [{"optionName": opt} for opt in options],
        "pollName": question,
        "multipleAnswers": False
    }
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        print("Success: Poll automatically posted on WhatsApp!")
    else:
        print(f"Error sending poll via Green-API: {response.text}")

if __name__ == "__main__":
    try:
        print("Connecting to Google AI Studio...")
        question, options = get_gk_question_from_ai()
        print(f"AI Generated Question: {question}")
        
        print("Forwarding Poll to WhatsApp...")
        send_whatsapp_poll(question, options)
    except Exception as e:
        print(f"An error occurred: {e}")
