import streamlit as st
import yfinance as yf
import pandas as pd
import ta
import plotly.graph_objects as go

# Configurăm titlul
st.title("Trading Bot Dashboard")

# Sidebar pentru configurare
st.sidebar.header("Configurare Strategie")
stock = st.sidebar.text_input("Introduceți simbolul acțiunii", "TSLA")
rsi_period = st.sidebar.slider("Perioada RSI", 7, 21, 14)
ema_short = st.sidebar.slider("EMA Scurtă", 10, 50, 20)
ema_long = st.sidebar.slider("EMA Lungă", 50, 200, 100)

# Descărcăm datele
@st.cache_data
def get_stock_data(stock):
    data = yf.download(stock, period="6mo", interval="1d")
    return data

data = get_stock_data(stock)

# Calculăm indicatorii
def calculate_indicators(data):
    data['RSI'] = ta.momentum.RSIIndicator(data['Close'], window=rsi_period).rsi()
    data['EMA_Short'] = ta.trend.ema_indicator(data['Close'], window=ema_short)
    data['EMA_Long'] = ta.trend.ema_indicator(data['Close'], window=ema_long)
    return data

if not data.empty:
    data = calculate_indicators(data)

    # Generăm semnale
    def generate_signals(data):
        if not data.empty and data['RSI'].iloc[-1] < 30 and data['EMA_Short'].iloc[-1] > data['EMA_Long'].iloc[-1]:
            return "Cumpărare"
        elif not data.empty and data['RSI'].iloc[-1] > 70:
            return "Vânzare"
        else:
            return "Ține"

    signal = generate_signals(data)
    st.subheader(f"Analiza pentru {stock}")
    st.write(f"Ultimul Semnal: **{signal}**")

    # Afisăm graficul
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], name="Preț"))
    fig.add_trace(go.Scatter(x=data.index, y=data['EMA_Short'], name=f"EMA {ema_short}"))
    fig.add_trace(go.Scatter(x=data.index, y=data['EMA_Long'], name=f"EMA {ema_long}"))
    st.plotly_chart(fig)
else:
    st.write("Nu s-au putut descărca datele. Verificați simbolul acțiunii.")
