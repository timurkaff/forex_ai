from fastapi import FastAPI
import yfinance as yf
from scipy.signal import argrelextrema
import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from pmdarima import auto_arima
from sklearn.metrics import mean_squared_error
from math import sqrt

app = FastAPI()

@app.get("/predict/{ticker}")
async def predict_ticker(ticker: str):
    # Загрузка данных
    data = yf.download(ticker, period="1mo", interval="1h")
    data = data[['Close']]
    data.reset_index(inplace=True)

    # Поиск локальных минимумов и максимумов
    local_minima_index = argrelextrema(data['Close'].values, np.less_equal, order=20)[0]
    local_maxima_index = argrelextrema(data['Close'].values, np.greater_equal, order=20)[0]
    unique_indices_set = set(local_minima_index).union(set(local_maxima_index))
    all_indices = sorted(unique_indices_set)

    filtered_data = data.loc[all_indices]

    train_size = int(len(filtered_data) * 0.8)
    train, test = filtered_data[:train_size], filtered_data[train_size:]

    train_close_prices = train['Close']

    train_array = train_close_prices.to_numpy()

    auto_model = auto_arima(train_array, seasonal=False, trace=False, error_action='ignore', suppress_warnings=True)

    model = ARIMA(train_array, order=auto_model.order)
    model_fit = model.fit()

    next_day_forecast = model_fit.forecast(steps=1)

    actual_value = test.iloc[0]['Close']

    forecasted_next_close_price = round(next_day_forecast[0], 5)
    current_close_price = round(data.iloc[-1]['Close'], 5)

    return {"Current Close Price": current_close_price, "Forecasted Next Close Price": forecasted_next_close_price}