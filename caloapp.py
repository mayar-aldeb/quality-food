from flask import Flask, request, jsonify, render_template, send_from_directory, session
import pandas as pd
from flask_cors import CORS



grams_per_cup = 250
grams_per_spoon = 15

def calculate_by_grams(measure_type,calories_per_given_amount, given_amount, new_amount):
    if measure_type == 'ملاعق':
        return ((new_amount * grams_per_spoon) * calories_per_given_amount) / given_amount
    elif measure_type == 'أكواب':
        return (new_amount * calories_per_given_amount) / (given_amount / grams_per_cup)
    else:
        return (new_amount * calories_per_given_amount) / given_amount
    
def calculate_by_spoon(measure_type,calories_per_given_amount, given_amount, new_amount):
    if measure_type == 'جرام':
        return ((new_amount / grams_per_spoon) * calories_per_given_amount) / given_amount
    elif measure_type == 'أكواب':
        return ((new_amount * grams_per_cup) * calories_per_given_amount) / (given_amount * grams_per_spoon)
    else:
        return ((((grams_per_spoon * new_amount) / given_amount) * calories_per_given_amount) / (
                    given_amount * grams_per_spoon))
    
def calculate_by_piece(calories_per_given_amount, given_amount, new_amount):
    return (new_amount * calories_per_given_amount) / given_amount

def calculate_by_cup(measure_type,calories_per_given_amount, given_amount, new_amount):
    if measure_type == 'جرام':
        return (new_amount * calories_per_given_amount) / (given_amount * grams_per_cup)
    elif measure_type == "ملاعق":
        return ((new_amount * grams_per_spoon) * calories_per_given_amount) / (given_amount * grams_per_cup)
    else:
        return ((((grams_per_cup * new_amount) / given_amount) * calories_per_given_amount) / (
                    given_amount * grams_per_cup))




def calculate_calories(calories_per_given_amount, given_amount, new_amount, measure_type,quantity_type):

    if quantity_type == 'جرام' or quantity_type == 'gram':
        return calculate_by_grams(measure_type,calories_per_given_amount, given_amount, new_amount)
    elif quantity_type == 'ملعقة' or quantity_type == 'spoon' :
        return calculate_by_spoon(measure_type,calories_per_given_amount, given_amount, new_amount)
    elif quantity_type == 'قطعة' or quantity_type == 'piece':
        return calculate_by_piece(calories_per_given_amount, given_amount, new_amount)
    elif quantity_type == 'كوب' or  quantity_type == 'cup':
        return calculate_by_cup(measure_type,calories_per_given_amount, given_amount, new_amount)
    else:
        return None
    

    

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return render_template("index02.html")

@app.route('/assets/<path:filename>')
def serve_static(filename):
    return send_from_directory('templates/assets', filename)

def load_data(filename):
    return pd.read_excel(filename, engine="openpyxl").applymap(lambda x: x.strip().lower() if isinstance(x, str) else x)


meals_file = "meals cal.xlsx"
drinks_file = "drinks cal.xlsx"
items_file = "items cal.xlsx"

df = load_data(items_file)
fd = load_data(meals_file)
dd = load_data(drinks_file)





   

@app.route('/food-list/<selectedType>', methods=['GET'])
def food_list(selectedType):
    food_names = list(df['صنف'].dropna().str.strip().str.lower()) + \
            list(fd['اكلة'].dropna().str.strip().str.lower()) + \
            list(dd['مشروب'].dropna().str.strip().str.lower())
    
    if selectedType == "all":
        food_names = list(df['صنف'].dropna().str.strip().str.lower()) + \
                     list(fd['اكلة'].dropna().str.strip().str.lower()) + \
                     list(dd['مشروب'].dropna().str.strip().str.lower())
    elif selectedType == "drink":
            food_names = list(dd['مشروب'].dropna().str.strip().str.lower())
    elif selectedType == "meal":  
            food_names = list(fd['اكلة'].dropna().str.strip().str.lower())
    elif selectedType == "item":    
            food_names = list(df['صنف'].dropna().str.strip().str.lower()) 
    # Get the current language from the session (or default to 1)

    return jsonify({"foods": food_names})


@app.route('/food-measure/<food_name>', methods=['GET'])
def get_food_measure(food_name):
    food_name = food_name.strip().lower()
    dataset = None

    if food_name in df['صنف'].dropna().str.strip().str.lower().values:
        dataset = df
        name_col, type_col = 'صنف', 'نوع الكمية'
    elif food_name in fd['اكلة'].dropna().str.strip().str.lower().values:
        dataset = fd
        name_col, type_col = 'اكلة', 'نوع الكمية'
    elif food_name in dd['مشروب'].dropna().str.strip().str.lower().values:
        dataset = dd
        name_col, type_col = 'مشروب','نوع الكمية' 

    if dataset is not None:
        item_data = dataset[dataset[name_col].str.strip().str.lower() == food_name].iloc[0]
        measure_type = item_data[type_col] if type_col else "جرام"


        if measure_type == "قطعة" or measure_type == "piece"  :
            return jsonify({"measure": ["قطعة"]})  # عرض "قطعة" فقط
        else:
            return jsonify({"measure": ["جرام", "ملاعق", "أكواب"]})  # عرض باقي الخيارات بدون "قطعة"

    return jsonify({"measure": []}), 404

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    total_calories = 0
    not_found_items = [] 
    for item in data['items']:
        item_name = item['name'].strip().lower()  
        new_amount = float(item['amount'])
        measure_type = item['type']
        
        dataset = None

        if item_name in df['صنف'].dropna().str.strip().str.lower().values:
            dataset = df
            name_col, quantity_col, type_col, calorie_col = 'صنف', 'الكمية', 'نوع الكمية', 'سعرات حرارية'
        elif item_name in fd['اكلة'].dropna().str.strip().str.lower().values:
            dataset = fd
            name_col, quantity_col, type_col, calorie_col = 'اكلة', 'الكمية', 'نوع الكمية', 'سعرات حرارية'
        elif item_name in dd['مشروب'].dropna().str.strip().str.lower().values:
            dataset = dd
            name_col, quantity_col, type_col, calorie_col = 'مشروب', 'الكمية', 'نوع الكمية','سعرات حرارية'
            
        

        if dataset is not None:
            item_data = dataset[dataset[name_col].str.strip().str.lower() == item_name].iloc[0]
            given_amount = item_data[quantity_col]
            calories_per_given_amount = item_data[calorie_col]
            quantity_type=item_data[type_col]
            calories = calculate_calories(calories_per_given_amount, given_amount, new_amount, measure_type,quantity_type)
            total_calories += calories
        else:
            not_found_items.append(item_name)

    return jsonify({"total": round(total_calories, 2), "not_found": not_found_items})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)


