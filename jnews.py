from flask import Flask, request, jsonify, render_template, send_from_directory
import os
import json
from flask_cors import CORS

app = Flask(__name__)  # تحديد المجلد الثابت بشكل صحيح
# CORS(app)

# عرض الصفحة الرئيسية
@app.route("/")
def home():
    return render_template("me.html")

@app.route('/assets/<path:filename>')
def serve_static(filename):
    return send_from_directory('templates/assets', filename)

# دالة لتحميل البيانات من JSON
def load_json_data():
    json_path = os.path.join(os.getcwd(), "templates", "products_data.json")
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as file:
            return json.load(file)
    return {}

# تحديث البيانات يدويًا عند الطلب
@app.route('/update-data')
def update_data():
    try:
        os.system("python convert_excel_to_json.py")  # تشغيل كود التحديث
        return jsonify({"status": "success", "message": "تم تحديث البيانات!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# جلب البيانات بصيغة JSON عند طلبها
@app.route('/get_data')
def get_data():
    try:
        data = load_json_data()
        if data:
            return jsonify(data)
        else:
            return jsonify({"error": "الملف غير موجود"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
