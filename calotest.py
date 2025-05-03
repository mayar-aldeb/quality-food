from flask import Flask, request, jsonify, render_template
import pandas as pd

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("test.html")

grams_per_cup = 250
grams_per_spoon = 15

# حساب السعرات بناءً على نوع القياس
def calculate_by_grams(calories_per_given_amount, given_amount, new_amount, measure_type):
    if measure_type == 'spoons': 
        return ((new_amount * grams_per_spoon) * calories_per_given_amount) / given_amount
    elif measure_type == 'cups':
        return (new_amount * calories_per_given_amount) / (given_amount / grams_per_cup)
    else:
        return (new_amount * calories_per_given_amount) / given_amount

def calculate_by_spoon(calories_per_given_amount, given_amount, new_amount, measure_type):
    if measure_type == 'grams':
        return ((new_amount / grams_per_spoon) * calories_per_given_amount) / given_amount
    elif measure_type == 'cups':
        return ((new_amount * grams_per_cup) * calories_per_given_amount) / (given_amount * grams_per_spoon)
    else:
        return ((((grams_per_spoon * new_amount) / given_amount) * calories_per_given_amount) / (given_amount * grams_per_spoon))

def calculate_by_piece(calories_per_given_amount, given_amount, new_amount):
    return (new_amount * calories_per_given_amount) / given_amount

def calculate_by_cup(calories_per_given_amount, given_amount, new_amount, measure_type):
    if measure_type == 'grams':
        return (new_amount * calories_per_given_amount) / (given_amount * grams_per_cup)
    elif measure_type == 'spoons':
        return ((new_amount * grams_per_spoon) * calories_per_given_amount) / (given_amount * grams_per_cup)
    else:
        return ((((grams_per_cup * new_amount) / given_amount) * calories_per_given_amount) / (given_amount * grams_per_cup))
    
def get_calories(df, item_col, quantity_col, type_col, calories_col, item_name, new_amount, measure_type=None):
    row = df[df[item_col] == item_name].iloc[0]
    given_amount = row[quantity_col]
    calories_per_given_amount = row[calories_col]
    quantity_type = row[type_col]

    if quantity_type == "جرام":
        return calculate_by_grams(calories_per_given_amount, given_amount, new_amount, measure_type)
    elif quantity_type == "ملعقة":
        return calculate_by_spoon(calories_per_given_amount, given_amount, new_amount, measure_type)
    elif quantity_type == "كوب":
        return calculate_by_cup(calories_per_given_amount, given_amount, new_amount, measure_type)
    elif quantity_type == "قطعة":
        return calculate_by_piece(calories_per_given_amount, given_amount, new_amount)
    else:
        return None

@app.route('/get_all_items', methods=['GET'])
def get_all_items():
    df = pd.read_excel('items cal.xlsx')
    fd = pd.read_excel('meals cal.xlsx')
    dd = pd.read_excel('drinks cal.xlsx')

    items = list(df['صنف'].dropna().unique()) + list(fd['اكلة'].dropna().unique()) + list(dd['مشروب'].dropna().unique())

    return jsonify({'items': items})


# استرجاع نوع الكمية للعناصر
@app.route('/get_quantity_type', methods=['POST'])
def get_quantity_type():
    data = request.json
    item_name = data.get('item_name')
    
    df = pd.read_excel('items cal.xlsx')
    fd = pd.read_excel('meals cal.xlsx')
    dd = pd.read_excel('drinks cal.xlsx')
    
    quantity_type = None
    
    if item_name in df['صنف'].values:
        quantity_type = df[df['صنف'] == item_name].iloc[0]['نوع الكمية']
    elif item_name in fd['اكلة'].values:
        quantity_type = fd[fd['اكلة'] == item_name].iloc[0]['نوع الكمية']
    elif item_name in dd['مشروب'].values:
        quantity_type = dd[dd['مشروب'] == item_name].iloc[0]['نوع الكمية']
    
    if quantity_type:
        return jsonify({'quantity_type': quantity_type})
    else:
        return jsonify({'error': "Item not found"}), 404

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    item_name = data.get('item_name')
    new_amount = float(data.get('new_amount'))
    measure_type = data.get('measure_type', None)

    df = pd.read_excel('items cal.xlsx')
    fd = pd.read_excel('meals cal.xlsx')
    dd = pd.read_excel('drinks cal.xlsx')

    quantity_type = None
    calories = None

    if item_name in df['صنف'].values:
        quantity_type = df[df['صنف'] == item_name].iloc[0]['نوع الكمية']
    elif item_name in fd['اكلة'].values:
        quantity_type = fd[fd['اكلة'] == item_name].iloc[0]['نوع الكمية']
    elif item_name in dd['مشروب'].values:
        quantity_type = dd[dd['مشروب'] == item_name].iloc[0]['نوع الكمية']

    if quantity_type:
        if quantity_type == "قطعة":
            if item_name in df['صنف'].values:
                calories = get_calories(df, 'صنف', 'الكمية', 'نوع الكمية', 'سعرات حرارية', item_name, new_amount)
            elif item_name in fd['اكلة'].values:
                calories = get_calories(fd, 'اكلة', 'الكمية', 'نوع الكمية', 'سعرات حرارية', item_name, new_amount)
            elif item_name in dd['مشروب'].values:
                calories = get_calories(dd, 'مشروب', 'الكمية', 'نوع الكمية', 'سعرات حرارية', item_name, new_amount)
        else:
            if item_name in df['صنف'].values:
                calories = get_calories(df, 'صنف', 'الكمية', 'نوع الكمية', 'سعرات حرارية', item_name, new_amount, measure_type)
            elif item_name in fd['اكلة'].values:
                calories = get_calories(fd, 'اكلة', 'الكمية', 'نوع الكمية', 'سعرات حرارية', item_name, new_amount, measure_type)
            elif item_name in dd['مشروب'].values:
                calories = get_calories(dd, 'مشروب', 'الكمية', 'نوع الكمية', 'سعرات حرارية', item_name, new_amount, measure_type)

    if calories is None:
        return jsonify({'error': f"The item '{item_name}' was not found."}), 404

    return jsonify({'calories': round(calories, 2)})

if __name__ == '__main__':
    app.run(debug=True, port=5050)
