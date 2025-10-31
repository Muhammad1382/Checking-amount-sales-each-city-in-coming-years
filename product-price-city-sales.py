import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------
# 1️⃣ Read data
# -----------------------------
df = pd.read_csv("Sales data.csv")

# Remove empty rows and convert to a number
df = df.dropna(subset=['Price Each','Quantity Ordered'])
df['Price Each'] = pd.to_numeric(df['Price Each'], errors='coerce')
df['Quantity Ordered'] = pd.to_numeric(df['Quantity Ordered'], errors='coerce')
df = df.dropna(subset=['Price Each','Quantity Ordered'])

# -----------------------------
# 2️⃣ Create price categories
# -----------------------------
def price_category(price):
    if price < 50:
        return 'Low Price'
    elif price < 150:
        return 'Medium Price'
    else:
        return 'High Price'

df['Price Category'] = df['Price Each'].apply(price_category)

# -----------------------------
# 3️⃣ Calculate the income of each group
# -----------------------------
df['Revenue'] = df['Quantity Ordered'] * df['Price Each']
revenue_by_category = df.groupby('Price Category')['Revenue'].sum().sort_values(ascending=False)
revenue_city_category = df.groupby(['City','Price Category'])['Revenue'].sum().unstack().fillna(0)

# -----------------------------
# 4️⃣ Draw two graphs side by side
# -----------------------------
fig, axes = plt.subplots(1, 2, figsize=(16,6))

# Pie chart
axes[0].pie(revenue_by_category, labels=revenue_by_category.index, autopct='%1.1f%%', colors=["#0bd5f0",'#99ff99','#ff9999'])
axes[0].set_title("Revenue Share by Price Category")

# Stacked Bar chart
revenue_city_category.plot(kind='bar', stacked=True, ax=axes[1], colormap='viridis')
axes[1].set_ylabel("Revenue ($)")
axes[1].set_title("Stacked Revenue by Price Category per City")
axes[1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.show()
