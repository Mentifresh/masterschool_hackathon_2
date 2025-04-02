import os
from api_gpt import extract_ingredients_from_input
from api_spoon import find_recipes_by_ingredients, get_detailed_recipes

# Eingabe: entweder Bild oder Text
image_path = None  # "Testbilder/img_2.png"
zutaten_string = "spiegelei, gras, weizen "

# Analyse: Bild oder Text verwenden
if image_path:
    if not os.path.exists(image_path):
        print(f" Bild nicht gefunden unter Pfad: {image_path}")
        zutatenliste = []
    else:
        print(" Starte Analyse des Bildes...")
        zutatenliste = extract_ingredients_from_input(image_path=image_path)
else:
    print(" Verwende Zutaten aus Text:")
    zutatenliste = extract_ingredients_from_input(zutaten_liste=zutaten_string)

if 2 <= len(zutatenliste) <= 5:
    rezepte = get_detailed_recipes(zutatenliste, number=3)
    print("\nGefundene detaillierte Rezepte:")
    for rezept in rezepte:
        print(f"{rezept['rezeptname']} (Health Score: {rezept.get('gesundheitsbewertung', 'k.A.')})")
        print(f"Link: {rezept.get('rezept_url')}")
        print(f"Video: {rezept.get('video_url')}\n")
else:
    print(f"\nNicht genug oder zu viele Zutaten für eine sinnvolle Rezeptsuche ({len(zutatenliste)} erkannt).")