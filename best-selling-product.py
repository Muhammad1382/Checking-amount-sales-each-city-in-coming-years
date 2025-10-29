import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df =  pd.read_csv ("Sales data.csv")

product_counts = df['Product'].value_counts()


plt.figure(figsize=(15,6))
ax = sns.barplot(x=product_counts.index, y=product_counts.values)
ax.bar_label(container=ax.containers[0],label_type='edge')



plt.xticks(rotation=45, ha='right')  # برچسب‌ها خواناتر باشن
plt.ylabel("Number of Sales")
plt.xlabel("Product")
plt.title("Products Sold")
plt.tight_layout()

plt.show()
