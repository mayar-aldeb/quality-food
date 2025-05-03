from PIL import Image
import pandas as pd


file_path = "recipes english.xlsx"

df = pd.read_excel(file_path, engine="openpyxl")

def suggest_recipes_all(ingredients, df):
    """Find recipes that contain all entered ingredients and return full columns."""
    matching_recipes_all = []
    meal_all=[]
    image_all=[]


    # Split user input into a list of ingredients
    ingredient_list = [ing.strip().lower() for ing in ingredients.split(",")]

    # Iterate through each recipe (column) in the DataFrame
    for recipe in df.columns:
        recipe_ingredients = df[recipe].dropna().astype(str).str.lower().tolist()

        # Check if all entered ingredients exist in the recipe
        if all(ing in " ".join(recipe_ingredients) for ing in ingredient_list):
            meal_all.append(recipe)
            matching_recipes_all.append(recipe_ingredients[:-1])  # Store full ingredient list
            image_all.append(recipe_ingredients[-1])

    return meal_all,matching_recipes_all,image_all


def suggest_recipes(ingredients, df):
    matching_recipes = []
    meal = []
    image = []
    found=[]
    # Split user input into a list of ingredients
    ingredient_list = [ing.strip().lower() for ing in ingredients.split(",")]
    for recipe in df.columns:
        recipe_ingredients = df[recipe].dropna().astype(str).str.lower().tolist()

        found_ingredients = [ing for ing in ingredient_list if ing in " ".join(recipe_ingredients)]
        if found_ingredients and len(found_ingredients) < len(ingredient_list):
            found.append(found_ingredients)
            meal.append(recipe)
            matching_recipes.append(recipe_ingredients[:-1])  # Store full ingredient list except last one
            image.append(recipe_ingredients[-1])  # Print which ingredients matched
    return meal,matching_recipes,image,found

ingredient_input = input("Enter your Ingredients: ")
meal,matching_recipes,image=suggest_recipes_all(ingredient_input,df)
for i in range(len(meal)):
    print("Meal:", meal[i])
    print("Ingredients:")

    # Print each ingredient on a new line
    for ingredient in matching_recipes[i]:
        print(f" - {ingredient}")
    prefix = "اكلات\\"  # The string to add before
    image_path = prefix + image[i] + ".jpg"  # Add prefix and ".jpg"
    img = Image.open(image_path)  # Open image with PIL
    img.show()  # Display image

    print("\n" + "-" * 40)  # Add a separator for better readability
meal, matching_recipes, image,ing = suggest_recipes(ingredient_input, df)
for i in range(len(meal)):
    print("Meal just have: ", ing[i])
    print("Meal:", meal[i])
    print("Ingredients:")
    # Print each ingredient on a new line
    for ingredient in matching_recipes[i]:
        print(f" - {ingredient}")
    prefix = "اكلات\\"  # The string to add before
    image_path = prefix + image[i] + ".jpg"  # Add prefix and ".jpg"
    img = Image.open(image_path)  # Open image with PIL
    img.show()  # Display image
    print("\n" + "-" * 40)  # Add a separator for better readability


    # ///////////////////////////////////////////////////////////////////

#     from PIL import Image
# import pandas as pd

# healthy = input("Enter 1 for healthy meals or 2 for unhealthy: ")
# arab_eng=input("Enter 3 for arabic meals or 4 for english: ")
# if healthy=="1":
#     if arab_eng =="3":
#         file_path = "C:\\Users\\Mahmoud\\Desktop\\recipes arabic healthy.xlsx"
#     else:
#         file_path = "C:\\Users\\Mahmoud\\Desktop\\recipes english healthy.xlsx"
# else:
#     if arab_eng =="3":
#         file_path = "C:\\Users\\Mahmoud\\Desktop\\recipes arabic.xlsx"
#     else:
#         file_path = "C:\\Users\\Mahmoud\\Desktop\\recipes english.xlsx"

# df = pd.read_excel(file_path, engine="openpyxl")

# def suggest_recipes_all(ingredients, df):
#     """Find recipes that contain all entered ingredients and return full columns."""
#     matching_recipes_all = []
#     meal_all=[]
#     image_all=[]


#     # Split user input into a list of ingredients
#     ingredient_list = [ing.strip().lower() for ing in ingredients.split(",")]

#     # Iterate through each recipe (column) in the DataFrame
#     for recipe in df.columns:
#         recipe_ingredients = df[recipe].dropna().astype(str).str.lower().tolist()

#         # Check if all entered ingredients exist in the recipe
#         if all(ing in " ".join(recipe_ingredients) for ing in ingredient_list):
#             meal_all.append(recipe)
#             matching_recipes_all.append(recipe_ingredients[:-1])  # Store full ingredient list
#             image_all.append(recipe_ingredients[-1])

#     return meal_all,matching_recipes_all,image_all


# def suggest_recipes(ingredients, df):
#     matching_recipes = []
#     meal = []
#     image = []
#     found=[]
#     # Split user input into a list of ingredients
#     ingredient_list = [ing.strip().lower() for ing in ingredients.split(",")]
#     for recipe in df.columns:
#         recipe_ingredients = df[recipe].dropna().astype(str).str.lower().tolist()

#         found_ingredients = [ing for ing in ingredient_list if ing in " ".join(recipe_ingredients)]
#         if found_ingredients and len(found_ingredients) < len(ingredient_list):
#             found.append(found_ingredients)
#             meal.append(recipe)
#             matching_recipes.append(recipe_ingredients[:-1])  # Store full ingredient list except last one
#             image.append(recipe_ingredients[-1])  # Print which ingredients matched
#     return meal,matching_recipes,image,found

# ingredient_input = input("Enter your Ingredients: ")
# meal,matching_recipes,image=suggest_recipes_all(ingredient_input,df)
# for i in range(len(meal)):
#     print("Meal:", meal[i])
#     print("Ingredients:")

#     # Print each ingredient on a new line
#     for ingredient in matching_recipes[i]:
#         print(f" - {ingredient}")
#     prefix = "اكلات\\"  # The string to add before
#     image_path = prefix + image[i] + ".jpg"  # Add prefix and ".jpg"
#     img = Image.open(image_path)  # Open image with PIL
#     img.show()  # Display image

#     print("\n" + "-" * 40)  # Add a separator for better readability
# meal, matching_recipes, image,ing = suggest_recipes(ingredient_input, df)
# for i in range(len(meal)):
#     print("Meal just have: ", ing[i])
#     print("Meal:", meal[i])
#     print("Ingredients:")
#     # Print each ingredient on a new line
#     for ingredient in matching_recipes[i]:
#         print(f" - {ingredient}")
#     prefix = "اكلات\\"  # The string to add before
#     image_path = prefix + image[i] + ".jpg"  # Add prefix and ".jpg"
#     img = Image.open(image_path)  # Open image with PIL
#     img.show()  # Display image
#     print("\n" + "-" * 40)  # Add a separator for better readability