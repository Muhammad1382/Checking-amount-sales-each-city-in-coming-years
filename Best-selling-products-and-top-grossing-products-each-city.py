import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df =  pd.read_csv ("Sales data.csv")

# The number of orders for each product in each city
count_grouped = df.groupby(['City', 'Product']).size().reset_index(name='Count')

# Find the product with the most sales in each city
top_count_products = count_grouped.loc[count_grouped.groupby('City')['Count'].idxmax()]

# Total sales of each product in each city
sales_grouped = df.groupby(['City', 'Product'])['Sales'].sum().reset_index()

# Find the highest grossing product in each city
top_sales_products = sales_grouped.loc[sales_grouped.groupby('City')['Sales'].idxmax()]


fig, axes = plt.subplots(1, 2, figsize=(13,6))  # 1 row, 2 columns

# Chart 1: Best selling product by number
sns.barplot(x='City', y='Count', hue='Product', data=top_count_products, dodge=False, ax=axes[0])
axes[0].set_title("Top Product by Quantity")
axes[0].tick_params(axis='x', rotation=45)

for container in axes[0].containers:
    axes[0].bar_label(container, fmt='%d', label_type='edge', padding=3)


# chart 2: the best-selling product by income
sns.barplot(x='City', y='Sales', hue='Product', data=top_sales_products, dodge=False, ax=axes[1])
axes[1].set_title("Top Product by Revenue")
axes[1].tick_params(axis='x', rotation=45)

for container in axes[1].containers:
    axes[1].bar_label(container, fmt=lambda x: f'${x:,.0f}', label_type='edge', padding=3)


plt.tight_layout()
plt.show()
