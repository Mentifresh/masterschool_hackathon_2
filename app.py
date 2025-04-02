from flask import Flask, render_template, url_for
import json

app = Flask(__name__)


def recipes_load():
    with open("rezepte.json") as f:
        return json.load(f)

recipes = recipes_load()

#[
#   {
#    "name": "Spaghetti Bolognese",
#     "bild": "bilder/essen.jpeg",
#     "text": "Gesund, bunt und super lecker – perfekt für den Alltag.",
#     "anleitung": "Gemüse schneiden, anbraten, würzen und servieren."
#     "video": "video/...",
#   },
#   {)
#]


@app.route("/")
def index():
    return render_template("index.html", all_found_recipes=recipes)

@app.route("/rezepte/<recipe_name>")
def recipe_details(recipe_name):
    user_selected_recipe = None
    for recipe in recipes:
        # wenn der ausgewählten Rezept-Namen von json gleich der ausgewählte Rezept-Namen
        if recipe["recipe_name"] == recipe_name:
            user_selected_recipe = recipe
            break
    return render_template("rezept_detail.html", user_selected_recipe)


#if __name__ == "__main__":
    #app.run(debug=True, port=5050)