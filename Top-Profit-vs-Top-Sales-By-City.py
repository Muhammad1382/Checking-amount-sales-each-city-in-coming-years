import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker


df = pd.read_csv("Sales data.csv")


# -----------------------------
# 1️⃣ Removing empty rows and ensuring that the columns are numeric
# -----------------------------
df = df.dropna(subset=['Sales','Quantity Ordered'])
df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce')
df['Quantity Ordered'] = pd.to_numeric(df['Quantity Ordered'], errors='coerce')
df = df.dropna(subset=['Sales','Quantity Ordered'])

# -----------------------------
# 2️⃣ The highest income of each product in each city
# -----------------------------
sales_grouped = df.groupby(['City','Product'])['Sales'].sum().reset_index()
top_by_revenue = sales_grouped.loc[sales_grouped.groupby('City')['Sales'].idxmax()]
top_by_revenue = top_by_revenue.rename(columns={'Product':'top_revenue_product','Sales':'top_revenue_value'})

# -----------------------------
# 3️⃣ The highest number of products sold in each city
# -----------------------------
count_grouped = df.groupby(['City','Product'])['Quantity Ordered'].sum().reset_index()
top_by_count = count_grouped.loc[count_grouped.groupby('City')['Quantity Ordered'].idxmax()]
top_by_count = top_by_count.rename(columns={'Product':'top_count_product','Quantity Ordered':'top_count_value'})

# -----------------------------
# 4️⃣ Combine two results for comparison
# -----------------------------
merged = pd.merge(top_by_revenue, top_by_count, on='City', how='outer')

# Extracting the income of the product that has the highest number of sales
revenue_lookup = sales_grouped.set_index(['City','Product'])['Sales']
merged['revenue_of_top_count_product'] = merged.apply(
    lambda row: revenue_lookup.loc[(row['City'], row['top_count_product'])], axis=1
)

# Income comparison
merged['which_is_higher'] = np.where(
    merged['top_revenue_value'] >= merged['revenue_of_top_count_product'],
    'Revenue Product Higher',
    'Top-by-Count Product Revenue Higher'
)

print(merged)

# -----------------------------
# 5️⃣ Prepare data for charting
# -----------------------------
long_df = pd.DataFrame({
    'City': merged['City'].tolist() * 2,
    'Revenue Type': ['Top by Revenue']*len(merged) + ['Revenue of Top-by-Count Product']*len(merged),
    'Revenue': pd.concat([merged['top_revenue_value'], merged['revenue_of_top_count_product']], ignore_index=True)
})

# -----------------------------
# 6️⃣ Draw a side by side bar chart
# -----------------------------
plt.figure(figsize=(14,6))
ax = sns.barplot(x='City', y='Revenue', hue='Revenue Type', data=long_df, dodge=True, palette='viridis')

# Rotation of city names
plt.xticks(rotation=45, ha='right')
plt.ylabel("Revenue ($)")
plt.title("Comparison of Top Revenue vs Revenue of Top-by-Count Product per City")

# Number display on the bars
for container in ax.containers:
    ax.bar_label(container, fmt=lambda x: f'${x:,.0f}', label_type='edge', padding=3)


ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'${x:,.0f}'))

plt.tight_layout()
plt.show()
