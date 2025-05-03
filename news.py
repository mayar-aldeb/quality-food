from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time

# تحميل ChromeDriver
service = Service("chromedriver.exe")  # تأكد من المسار الصحيح
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=service, options=options)

# فتح الموقع
url = "http://agriprice.gov.eg/local-prices"
driver.get(url)

# انتظار تحميل الصفحة
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "lable")))

# استخراج الفئات المطلوبة فقط
allowed_categories = [
    "الخضراوات",
    "الحبوب والبقوليات",
    "اللحوم والدواجن",
    "الألبان ومنتجاتها",
    "الأسماك",
    "الفاكهة",
    "السلع الأساسية",
]

all_data = {}  # تخزين بيانات كل فئة

categories = driver.find_elements(By.CSS_SELECTOR, "div.p-2.lable h6")

for category in categories:
    category_name = category.text.strip()

    # تخطي الفئات غير المرغوب فيها
    if category_name not in allowed_categories:
        continue

    # الضغط على الفئة
    print(f"🔍 دخول الفئة: {category_name}...")
    driver.execute_script("arguments[0].click();", category)
    time.sleep(3)  # انتظار تحميل الصفحة

    # اختيار "الكل" من عدد السلع في الصفحة
    try:
        select_box = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, "MuiTablePagination-select")))
        select_box.click()
        time.sleep(2)  # انتظار فتح القائمة المنسدلة
        
        all_option = driver.find_element(By.XPATH, "//li[text()='الكل']")
        all_option.click()
        time.sleep(5)  # انتظار تحميل جميع المنتجات
    except:
        print(f"⚠️ {category_name}: لم يتم العثور على زر اختيار عدد السلع")

    # استخراج المنتجات
    soup = BeautifulSoup(driver.page_source, "html.parser")
    products = soup.find_all("td", class_="MuiTableCell-root MuiTableCell-body text-center")

    category_data = []
    seen_products = set()  # مجموعة لتتبع المنتجات المكررة

    for product in products:
        try:
            product_name = product.find("span").text.strip()
            price_element = product.find_next("td").find("span")
            product_price = price_element.text.strip() if price_element else None

            # تخطي المنتجات التي سعرها "غير متاح" أو المكررة
            if product_price and product_price != "غير متاح" and product_name not in seen_products:
                seen_products.add(product_name)  # إضافة المنتج إلى القائمة لمنع تكراره
                category_data.append([product_name, product_price])
                print(f"📌 {category_name} - {product_name} - 💰 {product_price}")

        except AttributeError:
            continue  # تخطي أي خطأ

    if category_data:
        all_data[category_name] = category_data

# ✅ حفظ كل فئة في ملف Excel منفصل
try:
    with pd.ExcelWriter("اسعار_المنتجات.xlsx", engine="xlsxwriter") as writer:
        for category, data in all_data.items():
            df = pd.DataFrame(data, columns=["المنتج", "السعر"])
            df.to_excel(writer, sheet_name=category, index=False)
    print("✅ تم استخراج جميع البيانات بدون تكرار وحفظها في ملف Excel!")
except Exception as e:
    print(f"❌ خطأ أثناء حفظ الملف: {e}")

driver.quit()
