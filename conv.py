import pandas as pd
import json
import os

# تحديد مسار الملفات
EXCEL_FILE = "اسعار_المنتجات.xlsx"
JSON_FILE = os.path.join("templates", "products_data.json")

def convert_excel_to_json():
    if not os.path.exists(EXCEL_FILE):
        print(f"❌ الملف {EXCEL_FILE} غير موجود!")
        return

    # قراءة جميع الأوراق في ملف Excel
    excel_data = pd.read_excel(EXCEL_FILE, sheet_name=None)
    
    # تحويل كل ورقة (فئة) إلى JSON
    all_data = {}
    for category, df in excel_data.items():
        all_data[category] = df.to_dict(orient="records")

    # حفظ البيانات في ملف JSON داخل مجلد templates
    with open(JSON_FILE, "w", encoding="utf-8") as file:
        json.dump(all_data, file, ensure_ascii=False, indent=4)

    print(f"✅ تم تحويل {EXCEL_FILE} إلى {JSON_FILE} بنجاح!")

# تشغيل التحويل
if __name__ == "__main__":
    convert_excel_to_json()
