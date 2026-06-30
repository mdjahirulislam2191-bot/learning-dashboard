# Day 33: Prophet
## Facebook Prophet

### Prophet কি?
Prophet হল Facebook (Meta) দ্বারা তৈরি একটি টাইম সিরিজ ফোরকাস্টিং টুল যা দৈনিক পর্যবেক্ষণ সহ শক্তিশালী ঋতুগত প্রভাব এবং একাধিক সিজনালিটি হ্যান্ডল করতে পারে। এটি মিসিং ডেটা এবং আউটলায়ারদের প্রতি রোবাস্ট।

### Prophet এর বৈশিষ্ট্য
- **অটোমেটিক সিজনালিটি**: দৈনিক, সাপ্তাহিক, বার্ষিক
- **হলিডে ইফেক্ট**: বিশেষ দিনের প্রভাব মডেল করা
- **চেঞ্জপয়েন্ট ডিটেকশন**: ট্রেন্ড পরিবর্তন শনাক্ত
- **আউটলায়ার রোবাস্ট**: মিসিং ডেটা হ্যান্ডল

### ফাইন্যান্স উদাহরণ: বিক্রয় পূর্বাভাস
```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly
from sklearn.metrics import mean_squared_error, mean_absolute_error
import warnings
warnings.filterwarnings('ignore')

# ফাইন্যান্সিয়াল টাইম সিরিজ তৈরি
np.random.seed(42)
n = 730  # 2 years
dates = pd.date_range('2022-01-01', periods=n, freq='D')

# ট্রেন্ড + সাপ্তাহিক + বার্ষিক + নয়েজ
t = np.arange(n)
trend = 100 + t * 0.05
weekly = 5 * np.sin(2 * np.pi * t / 7)
yearly = 15 * np.sin(2 * np.pi * t / 365.25)
noise = np.random.randn(n) * 3

# বিশেষ ইভেন্ট (ব্ল্যাক ফ্রাইডে, ক্রিসমাস ইত্যাদি)
holiday_effect = np.zeros(n)
for i, date in enumerate(dates):
    if date.month == 12 and date.day == 25:  # Christmas
        holiday_effect[i] = 30
    if date.month == 11 and date.day >= 25 and date.day <= 30:  # Black Friday
        holiday_effect[i] = 20
    if date.month == 1 and date.day == 1:  # New Year
        holiday_effect[i] = -10

sales = trend + weekly + yearly + holiday_effect + noise
sales = np.maximum(sales, 0)  # No negative sales

df = pd.DataFrame({
    'ds': dates,
    'y': sales
})

print(f"Date range: {df['ds'].min()} to {df['ds'].max()}")
print(f"Sales range: {df['y'].min():.2f} to {df['y'].max():.2f}")
print(f"Mean sales: {df['y'].mean():.2f}")
```

### 1. বেসিক Prophet মডেল
```python
# Prophet মডেল তৈরি
model = Prophet(
    yearly_seasonality=True,
    weekly_seasonality=True,
    daily_seasonality=False,
    seasonality_mode='multiplicative',  # বা 'additive'
    changepoint_prior_scale=0.05,
    seasonality_prior_scale=10.0
)

model.fit(df)

print("✅ Prophet model trained")
print("\nModel parameters:")
print(f"  Seasonality mode: multiplicative")
print(f"  Changepoint prior scale: 0.05")
print(f"  Seasonality prior scale: 10.0")
```

### 2. ফোরকাস্টিং
```python
# ভবিষ্যতের 90 দিনের ফোরকাস্ট
future = model.make_future_dataframe(periods=90)
forecast = model.predict(future)

print(f"Forecast shape: {forecast.shape}")
print("\nForecast columns:")
print(forecast.columns.tolist())
print(f"\nForecast range: {forecast['ds'].min()} to {forecast['ds'].max()}")
```

### 3. Prophet প্লট
```python
# ফোরকাস্ট প্লট
fig1 = model.plot(forecast)
plt.title('Prophet Forecast - Daily Sales')
plt.xlabel('Date')
plt.ylabel('Sales ($)')
plt.grid(True, alpha=0.3)

# কম্পোনেন্ট প্লট
fig2 = model.plot_components(forecast)
plt.tight_layout()
plt.show()
```

### 4. ইভালুয়েশন (ট্রেন/টেস্ট স্প্লিট)
```python
# ট্রেন/টেস্ট স্প্লিট
train = df.iloc[:int(n * 0.8)]
test = df.iloc[int(n * 0.8):]

# Prophet মডেল
model_cv = Prophet(yearly_seasonality=True, weekly_seasonality=True)
model_cv.fit(train)

# ফোরকাস্ট
future_cv = model_cv.make_future_dataframe(periods=len(test))
forecast_cv = model_cv.predict(future_cv)

# টেস্ট সেটের সাথে মিলানো
forecast_test = forecast_cv.iloc[-len(test):]
y_pred = forecast_test['yhat'].values
y_true = test['y'].values

# ইভালুয়েশন
rmse = np.sqrt(mean_squared_error(y_true, y_pred))
mae = mean_absolute_error(y_true, y_pred)
mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100

print(f"\n📊 Prophet Forecast Performance:")
print(f"  RMSE: {rmse:.4f}")
print(f"  MAE:  {mae:.4f}")
print(f"  MAPE: {mape:.2f}%")

# প্রেডিকশন ইন্টারভাল
lower = forecast_test['yhat_lower'].values
upper = forecast_test['yhat_upper'].values
coverage = np.mean((y_true >= lower) & (y_true <= upper))
print(f"  Prediction interval coverage: {coverage:.2%}")

plt.figure(figsize=(15, 6))
plt.plot(test['ds'], y_true, label='Actual', linewidth=2)
plt.plot(test['ds'], y_pred, label='Prophet Forecast', linewidth=2, linestyle='--')
plt.fill_between(test['ds'], lower, upper, alpha=0.2, label='95% Confidence Interval')
plt.title('Prophet - Test Set Forecast')
plt.xlabel('Date')
plt.ylabel('Sales ($)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
```

### 5. কাস্টম সিজনালিটি এবং রিগ্রেসর
```python
# কাস্টম সিজনালিটি (মাসিক)
model_custom = Prophet()
model_custom.add_seasonality(name='monthly', period=30.5, fourier_order=5)

# কাস্টম রিগ্রেসর (মার্কেটিং স্পেন্ড)
df['marketing_spend'] = np.random.randn(n) * 100 + 500
model_custom.add_regressor('marketing_spend')

# হলিডে ইফেক্ট
holidays = pd.DataFrame({
    'holiday': 'black_friday',
    'ds': pd.to_datetime(['2022-11-25']),
    'lower_window': -2,
    'upper_window': 1
})

model_holidays = Prophet(holidays=holidays, yearly_seasonality=True)
model_holidays.fit(df)

print("✅ Custom Prophet model with:")
print("  - Monthly seasonality")
print("  - Marketing spend regressor")
print("  - Black Friday holiday effect")
```

### 6. ক্রস ভ্যালিডেশন
```python
from prophet.diagnostics import cross_validation, performance_metrics

# ক্রস ভ্যালিডেশন
df_cv = cross_validation(model, initial='365 days', period='30 days', horizon='90 days')
df_metrics = performance_metrics(df_cv)

print("\n📊 Cross-Validation Performance Metrics:")
print(df_metrics[['horizon', 'rmse', 'mae', 'mape']].head(10))

# ক্রস ভ্যালিডেশন প্লট
fig = plt.figure(figsize=(15, 6))
plt.plot(df_cv['ds'], df_cv['y'], label='Actual', alpha=0.7)
plt.plot(df_cv['ds'], df_cv['yhat'], label='Predicted', alpha=0.7)
plt.fill_between(df_cv['ds'], df_cv['yhat_lower'], df_cv['yhat_upper'], 
                 alpha=0.2, label='95% CI')
plt.title('Cross-Validation Results')
plt.xlabel('Date')
plt.ylabel('Sales')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
```

### 7. Prophet পারফরম্যান্স টিউনিং
```python
# হাইপারপ্যারামিটার টিউনিং
param_grid = {
    'changepoint_prior_scale': [0.01, 0.05, 0.1, 0.5],
    'seasonality_prior_scale': [0.1, 1.0, 10.0],
    'seasonality_mode': ['additive', 'multiplicative']
}

# সব কম্বিনেশন (16 মডেল)
best_params = None
best_rmse = float('inf')

print("\n🔄 Hyperparameter Tuning...")
for cp in param_grid['changepoint_prior_scale']:
    for sp in param_grid['seasonality_prior_scale']:
        for sm in param_grid['seasonality_mode']:
            try:
                m = Prophet(
                    changepoint_prior_scale=cp,
                    seasonality_prior_scale=sp,
                    seasonality_mode=sm,
                    yearly_seasonality=True,
                    weekly_seasonality=True
                )
                m.fit(train)
                future_m = m.make_future_dataframe(periods=len(test))
                forecast_m = m.predict(future_m)
                y_pred_m = forecast_m['yhat'].iloc[-len(test):].values
                rmse_m = np.sqrt(mean_squared_error(test['y'], y_pred_m))
                
                print(f"  cp={cp:.2f}, sp={sp:.1f}, mode={sm}: RMSE={rmse_m:.4f}")
                
                if rmse_m < best_rmse:
                    best_rmse = rmse_m
                    best_params = {'cp': cp, 'sp': sp, 'mode': sm}
            except:
                continue

print(f"\n✅ Best params: {best_params}")
print(f"   Best RMSE: {best_rmse:.4f}")
```

### Prophet বেস্ট প্র্যাকটিস
```python
print("""
✅ Prophet Best Practices:
1️⃣ Always visualize components (trend, weekly, yearly)
2️⃣ Use cross-validation for robust evaluation
3️⃣ Add domain-specific regressors
4️⃣ Handle outliers with 'floor' and 'cap' (logistic growth)
5️⃣ Tune changepoint_prior_scale (0.01-0.5)
6️⃣ Add holiday effects for special events
7️⃣ Check prediction intervals for uncertainty

Prophet vs ARIMA:
⚫ Prophet: Automatic seasonality, robust to missing data, interpretable
⚫ ARIMA: More traditional, better for short-term forecasts, less flexible
""")
```

### সারসংক্ষেপ
আজ আমরা Prophet ফোরকাস্টিং টুল শিখলাম:
- **Prophet মডেল**: Trend + Seasonality + Holidays
- **ফোরকাস্টিং**: সহজ মেক-ফিউচার ডেটাফ্রেম API
- **কম্পোনেন্ট**: Trend, Weekly, Yearly প্যাটার্ন
- **কাস্টমাইজেশন**: Regressors, Holidays, Custom Seasonality
- **ক্রস ভ্যালিডেশন**: Time Series CV
- **হাইপারপ্যারামিটার টিউনিং**: চেঞ্জপয়েন্ট, সিজনালিটি স্কেল

### অনুশীলনী
1. Prophet ব্যবহার করে রিয়েল স্টক ডেটা ফোরকাস্ট করুন
2. মাল্টিপল রিগ্রেসর (interest rate, volume) যোগ করে মডেল উন্নত করুন
3. বিভিন্ন চেঞ্জপয়েন্ট প্রায়োর স্কেল নিয়ে এক্সপেরিমেন্ট করুন
4. Prophet vs ARIMA এর পারফরম্যান্স তুলনা করুন