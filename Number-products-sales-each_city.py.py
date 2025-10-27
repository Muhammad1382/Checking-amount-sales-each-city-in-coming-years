import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker



df = pd.read_csv(r"C:\Users\Ertebat\Desktop\Sales Data.csv")


City_sales = df.groupby('City')['Sales'].sum().sort_values(ascending=True)

fig, ax = plt.subplots(figsize=(12, 6))
plt.subplots_adjust(bottom=0.2)



ax= sns.barplot(x=City_sales.index, y=City_sales.values, ax=ax)
plt.xticks(rotation=45, ha='right')


ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'{x:,.0f}'))


for container in ax.containers:
    ax.bar_label(container, fmt=lambda x: f'{x:,.0f}', label_type='edge', padding=2)


plt.show()
