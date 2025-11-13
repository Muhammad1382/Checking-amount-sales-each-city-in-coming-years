import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from sklearn.metrics import mean_absolute_error

# -----------------------------
# 1️⃣ خواندن و آماده‌سازی داده
# -----------------------------
df = pd.read_csv("Sales data.csv")

df = df.dropna(subset=['Order Date','Quantity Ordered','Price Each'])
df['Quantity Ordered'] = pd.to_numeric(df['Quantity Ordered'], errors='coerce')
df['Price Each'] = pd.to_numeric(df['Price Each'], errors='coerce')
df = df.dropna(subset=['Quantity Ordered','Price Each'])
df['Revenue'] = df['Quantity Ordered'] * df['Price Each']
df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
df = df.dropna(subset=['Order Date'])

# گروه‌بندی روزانه
daily = df.groupby(df['Order Date'].dt.date)['Revenue'].sum()
daily = daily.asfreq('D').fillna(0)

# -----------------------------
# 2️⃣ تقسیم داده‌ها به آموزش و تست
# -----------------------------
train_size = int(len(daily) * 0.85)
train, test = daily.iloc[:train_size], daily.iloc[train_size:]

# -----------------------------
# 3️⃣ ساخت مدل SARIMAX و آموزش
# -----------------------------
model = sm.tsa.statespace.SARIMAX(train, order=(1,1,1), seasonal_order=(1,1,1,7))
results = model.fit(disp=False)

# -----------------------------
# 4️⃣ پیش‌بینی
# -----------------------------
forecast = results.get_forecast(steps=len(test))
pred_mean = forecast.predicted_mean
conf_int = forecast.conf_int()

# -----------------------------
# 5️⃣ ارزیابی دقت مدل
# -----------------------------
mae = mean_absolute_error(test, pred_mean)
mape = np.mean(np.abs((test - pred_mean) / test)) * 100
print(f"MAE: {mae:.2f}")
print(f"MAPE: {mape:.2f}%")

# -----------------------------
# 6️⃣ نمودار نتایج
# -----------------------------
plt.figure(figsize=(14,6))
plt.plot(train.index, train, label='Train', color='blue')
plt.plot(test.index, test, label='Actual', color='black')
plt.plot(pred_mean.index, pred_mean, label='Forecast', color='red')
plt.fill_between(pred_mean.index, conf_int.iloc[:,0], conf_int.iloc[:,1], color='red', alpha=0.2)
plt.xlabel('Date')
plt.ylabel('Revenue ($)')
plt.title('Daily Sales Forecast (SARIMAX)')
plt.legend()
plt.tight_layout()
plt.show()
