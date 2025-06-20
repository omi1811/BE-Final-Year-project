import pandas as pd
import matplotlib.pyplot as plt
from pmdarima import auto_arima
import warnings
warnings.filterwarnings("ignore")

def train_sarima(df, column):
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)
    df = df.resample('H').mean().interpolate()  # hourly and clean

    # Fit SARIMA
    model = auto_arima(df[column], seasonal=True, m=24, trace=True)
    forecast = model.predict(n_periods=24)

    # Plot
    plt.figure(figsize=(10,5))
    df[column].tail(26).plot(label='Actual')
    pd.Series(forecast, index=pd.date_range(df.index[-1], periods=24, freq='H')).plot(label='Forecast')
    plt.legend()
    plt.title(f'SARIMA Forecast for {column}')
    plt.show()

    return forecast
