

from flask import Flask, render_template, request, send_from_directory
import pandas as pd
import os

app = Flask(__name__)

# مسار مجلد الصور
IMAGE_FOLDER = os.path.join(os.getcwd(), "اكلات")

@app.route('/assets/<path:filename>')
def serve_static(filename):
    return send_from_directory('templates/assets', filename)

@app.route('/images/<filename>')
def get_image(filename):
    return send_from_directory(IMAGE_FOLDER, filename)
@app.route('/', methods=['GET', 'POST'])
def index():
    # متغيرات فاضية مبدئيًا علشان الصفحة تفتح بدون أخطاء في GET
    meals_all = []
    matching_recipes_all = []
    images_all = []
    meals_partial = []
    matching_recipes_partial = []
    images_partial = []
    found_ingredients_partial = []

    if request.method == 'POST':
        healthy = request.form.get('healthy')
        ingredients = request.form.get('ingredients')
        lang_value = request.form.get('language_value')  # will be '3' or '4' as string


        

        if healthy == "1":
            file_path = "recipes arabic healthy.xlsx" if lang_value == "3" else "recipes english healthy.xlsx"
        else:
            file_path = "recipes arabic.xlsx" if lang_value == "3" else "recipes english.xlsx"

        df = pd.read_excel(file_path, engine="openpyxl")

        def suggest_recipes_all(ingredients, df):
            matching_recipes_all, meal_all, image_all = [], [], []
            ingredient_list = [ing.strip().lower() for ing in ingredients.split(",")]


            for recipe in df.columns:
                recipe_ingredients = df[recipe].dropna().astype(str).str.lower().tolist()
                if all(ing in " ".join(recipe_ingredients) for ing in ingredient_list):
                    meal_all.append(recipe)
                    matching_recipes_all.append(recipe_ingredients[:-1])
                    image_all.append(recipe_ingredients[-1])
            return meal_all, matching_recipes_all, image_all

        def suggest_recipes(ingredients, df):
            matching_recipes, meal, image, found = [], [], [], []
            ingredient_list = [ing.strip().lower() for ing in ingredients.split(",")]

            for recipe in df.columns:
                recipe_ingredients = df[recipe].dropna().astype(str).str.lower().tolist()
                found_ing = [ing for ing in ingredient_list if ing in " ".join(recipe_ingredients)]
                if found_ing and len(found_ing) < len(ingredient_list):
                    found.append(found_ing)
                    meal.append(recipe)
                    matching_recipes.append(recipe_ingredients[:-1])
                    image.append(recipe_ingredients[-1])
            return meal, matching_recipes, image, found

        meals_all, matching_recipes_all, images_all = suggest_recipes_all(ingredients, df)
        meals_partial, matching_recipes_partial, images_partial, found_ingredients_partial = suggest_recipes(ingredients, df)

        def validate_images(image_list):
            valid = []
            for img in image_list:
                image_path = os.path.join(IMAGE_FOLDER, img + ".jpg")
                valid.append(img + ".jpg" if os.path.exists(image_path) else None)
            return valid

        images_all = validate_images(images_all)
        images_partial = validate_images(images_partial)

    # يرجّع الصفحة سواء POST أو GET
    return render_template(
        'foodrec.html',
        meals_all=meals_all,
        matching_recipes_all=matching_recipes_all,
        images_all=images_all,
        meals_partial=meals_partial,
        matching_recipes_partial=matching_recipes_partial,
        images_partial=images_partial,
        found_ingredients_partial=found_ingredients_partial
    )


if __name__ == '__main__':
    app.run(debug=True, port=5010)
