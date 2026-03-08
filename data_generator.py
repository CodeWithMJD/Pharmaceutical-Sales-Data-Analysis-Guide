import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# إعداد المتغيرات الأساسية
np.random.seed(42)
n_rows = 1000
start_date = datetime(2025, 1, 1)

# قائمة أدوية وهمية وفئاتها
drugs = {
    'Panadol': 'Analgesics',
    'Amoxicillin': 'Antibiotics',
    'Insulin': 'Diabetes',
    'Lipitor': 'Cholesterol',
    'Ventolin': 'Respiratory',
    'Nexium': 'Gastrointestinal'
}

# توليد البيانات العشوائية
data = {
    'Transaction_ID': range(1001, 1001 + n_rows),
    'Date': [start_date + timedelta(days=np.random.randint(0, 365)) for _ in range(n_rows)],
    'Drug_Name': np.random.choice(list(drugs.keys()), n_rows),
    'Quantity': np.random.randint(1, 10, n_rows),
    'Unit_Price': np.random.uniform(10, 150, n_rows).round(2),
}

# تحويل البيانات إلى DataFrame
df = pd.DataFrame(data)

# إضافة الفئة بناءً على اسم الدواء
df['Category'] = df['Drug_Name'].map(drugs)

# إضافة تكلفة الوحدة (لأغراض التحليل المالي)
df['Unit_Cost'] = (df['Unit_Price'] * 0.7).round(2)

# حفظ الملف
df.to_csv('pharmacy_sales.csv', index=False)
print("تم إنشاء ملف pharmacy_sales.csv بنجاح!")