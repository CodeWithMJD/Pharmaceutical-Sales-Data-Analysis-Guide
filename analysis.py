import pandas as pd
import matplotlib.pyplot as plt

# 1. تحميل البيانات
df = pd.read_csv('pharmacy_sales.csv')

# 2. تحويل عمود التاريخ لنوع datetime (ضروري للتحليل الزمني)
df['Date'] = pd.to_datetime(df['Date'])

# 3. حسابات مالية أساسية (Feature Engineering)
# إجمالي المبيعات = الكمية * سعر الوحدة
df['Revenue'] = df['Quantity'] * df['Unit_Price']

# إجمالي التكلفة = الكمية * تكلفة الوحدة
df['Total_Cost'] = df['Quantity'] * df['Unit_Cost']

# الربح الصافي لكل عملية
df['Profit'] = df['Revenue'] - df['Total_Cost']

# 4. استخراج رؤى سريعة (Insights)
total_revenue = df['Revenue'].sum()
total_profit = df['Profit'].sum()
profit_margin = (total_profit / total_revenue) * 100

print(f"--- ملخص الأداء المالي ---")
print(f"إجمالي الإيرادات: ${total_revenue:,.2f}")
print(f"إجمالي الأرباح: ${total_profit:,.2f}")
print(f"هامش الربح الإجمالي: {profit_margin:.2f}%")
print("-" * 25)

# 5. تحليل الفئات (أيهما الأكثر مبيعاً؟)
category_performance = df.groupby('Category')['Revenue'].sum().sort_values(ascending=False)
print("\nأداء الفئات العلاجية (حسب الإيرادات):")
print(category_performance)

top_drugs = df.groupby('Drug_Name')['Quantity'].sum().nlargest(3)
print("\nأكثر 3 أدوية مبيعاً من حيث الكمية:")
print(top_drugs)

# 1. إضافة عمود للشهر (استخراج الشهر من التاريخ)
df['Month'] = df['Date'].dt.to_period('M')

# 2. حساب المبيعات والأرباح لكل شهر
monthly_sales = df.groupby('Month').agg({
    'Revenue': 'sum',
    'Profit': 'sum'
}).sort_index()

print("\n--- تحليل المبيعات الشهري ---")
print(monthly_sales)

# 3. تحديد أفضل شهر من حيث المبيعات
best_month = monthly_sales['Revenue'].idxmax()
max_revenue = monthly_sales['Revenue'].max()

print(f"\nأفضل شهر مبيعات هو {best_month} بإجمالي: ${max_revenue:,.2f}")

# رسم مخطط بياني للمبيعات الشهرية
monthly_sales['Revenue'].plot(kind='line', marker='o', color='b', figsize=(10, 5))

plt.title('Monthly Pharmaceutical Sales Trend (2025)')
plt.xlabel('Month')
plt.ylabel('Revenue ($)')
plt.grid(True)
plt.show()

# 1. إنشاء ملف إكسيل باستخدام Pandas و XlsxWriter كمحرك (Engine)
writer = pd.ExcelWriter('Pharmacy_Report_2025.xlsx', engine='xlsxwriter')

# 2. تصدير البيانات الأساسية والتحليلات لصفحات منفصلة
df.to_excel(writer, sheet_name='All_Transactions', index=False)
category_performance.to_frame().to_excel(writer, sheet_name='Category_Summary')
monthly_sales.to_excel(writer, sheet_name='Monthly_Summary')

# 3. الوصول إلى كائن xlsxwriter لتنسيق الملف
workbook  = writer.book
worksheet = writer.sheets['Monthly_Summary']

# 4. إضافة رسم بياني (Chart) داخل ملف الإكسيل مباشرة
chart = workbook.add_chart({'type': 'line'})

# تحديد البيانات للرسم البياني (من صفحة Monthly_Summary)
chart.add_series({
    'name':       'Monthly Revenue',
    'categories': ['Monthly_Summary', 1, 0, 12, 0],
    'values':     ['Monthly_Summary', 1, 1, 12, 1],
    'marker':     {'type': 'circle', 'size': 5},
})

# إضافة عناوين للرسم البياني
chart.set_title({'name': 'إجمالي المبيعات الشهرية'})
chart.set_x_axis({'name': 'الشهر'})
chart.set_y_axis({'name': 'المبيعات ($)'})

# إدراج الرسم البياني في الصفحة
worksheet.insert_chart('D2', chart)

# إغلاق وحفظ الملف
writer.close()
print("\n✅ تم استخراج التقرير الاحترافي: Pharmacy_Report_2025.xlsx")