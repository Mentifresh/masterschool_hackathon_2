import openai
from openai import OpenAI
import os
import base64
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_ingredients_from_input(image_path: str = None, zutaten_liste: list = None) -> list:
    """
    Extrahiert eine cleane, englische Zutatenliste entweder aus einem Bild (Kühlschrankfoto)
    oder aus einer gegebenen Liste (z.B. von WhatsApp-Text).
    Rückgabe: Liste von Zutaten optimiert für Spoonacular.
    """

    if not image_path and not zutaten_liste:
        raise ValueError("Bitte entweder ein Bildpfad oder eine Zutatenliste übergeben.")

    if image_path:
        # Bild analysieren und Zutaten erkennen
        with open(image_path, "rb") as img_file:
            base64_img = base64.b64encode(img_file.read()).decode("utf-8")

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "You are helping to suggest a recipe based on a fridge photo. Only list food ingredients that are suitable for cooking a proper dish. Exclude drinks, jars, sauces, and non-edible items. Focus on visible fruits, vegetables, dairy, meats, and other fresh food. Only return a short, comma-separated list in English, no explanations."
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{base64_img}"}
                        }
                    ]
                }
            ],
            max_tokens=300,
            temperature=0.3
        )
        gpt_text = response.choices[0].message.content
        return [item.strip().lower() for item in gpt_text.split(",")]

    if zutaten_liste:
        # Falls String übergeben wurde (nicht Liste), umwandeln
        if isinstance(zutaten_liste, str):
            zutaten_liste = [z.strip() for z in zutaten_liste.split(",")]

        prompt = (
            "Convert this list of food ingredients into clean, comma-separated English keywords for cooking APIs like Spoonacular:\n"
            + ", ".join(zutaten_liste)
        )
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.3
        )
        gpt_text = response.choices[0].message.content
        return [item.strip().lower() for item in gpt_text.split(",")]

    return []
