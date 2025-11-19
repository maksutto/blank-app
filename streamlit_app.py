import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from streamlit_autorefresh import st_autorefresh
from binance_data import binance_history


#@st.cache_data(ttl=300)
def load_data():
    url_data = "https://www.dropbox.com/scl/fi/x8igzmtfwbmgt47t6qkl9/btc_data.csv?rlkey=w3j4lhw59ei3dt383st2tqawp&dl=1"
    url_0dte = "https://www.dropbox.com/scl/fi/mcanpcslmq1zf2q7z5ls8/btc_data_Exp0.csv?rlkey=pojk0kmmamvt0y1xldljtijpd&dl=1"
    url_v = "https://www.dropbox.com/scl/fi/2wlhuv0lr46b9rv4eqf4m/btc_data_v_Exp0.csv?rlkey=qqg5czbp5d7k60hoafn756xrc&st=5dvxmvp5&dl=1"
    url_v_2 = "https://www.dropbox.com/scl/fi/k8y01j4mgyam5e4sx0oh6/btc_data_v_Exp1.csv?rlkey=6n0zui60w5q95p1abb1yrbc9u&st=e5sqjbwx&dl=1"                

    data = pd.read_csv(url_data, index_col=0)
    data["date"] = pd.to_datetime(data["date"])
    data["date"] = data["date"] - timedelta(hours=3)
    data.index = data["date"]
    data = data[~data.index.duplicated()].bfill()
    data = data[-800:]
    
    data0dte = pd.read_csv(url_0dte, index_col=0)
    data0dte["date"] = pd.to_datetime(data0dte["date"])
    data0dte["date"] = data0dte["date"] - timedelta(hours=3)
    data0dte.index = data0dte["date"]
    data0dte = data0dte[~data0dte.index.duplicated()].bfill()
    data0dte = data0dte[-800:]
    
    datav = pd.read_csv(url_v, index_col=0)
    datav["date"] = pd.to_datetime(datav["date"])
    datav.index = datav["date"]
    datav = datav[~datav.index.duplicated()].bfill()
    datav = datav[-800:]
    
    datav2 = pd.read_csv(url_v_2, index_col=0)
    datav2["date"] = pd.to_datetime(datav2["date"])
    datav2.index = datav2["date"]
    datav2 = datav2[~datav2.index.duplicated()].bfill()
    datav2 = datav2[-800:]
    
    # end_date = datetime.now()
    # start_for_btc = data0dte.index[-500] if len(data0dte) >= 400 else data0dte.index[0]
    # tick = Ticker("BTC")
    # btc_data = tick.history(start=start_for_btc, end=end_date, interval='5m')
    # btc_data = btc_data.droplevel(0)
    # btc_data.index = btc_data.index.tz_localize(None)

    # end_date = datetime.now()
    # start_for_btc = data0dte.index[-500] if len(data0dte) >= 400 else data0dte.index[0]
    # btc_data = yf.download('BTC-USD', start=start_for_btc, interval='5m', end=end_date)
    # btc_data.columns = btc_data.columns.droplevel(1)
    # btc_data.index = btc_data.index.tz_localize(None)
    end = datetime.now()
    start = end - timedelta(days=7)

    btc_data = binance_history(
        symbol='BTCUSDT',
        interval='5m',
        start_time=start,
        end_time=end
    )
    btc_data.index = btc_data['Open time'].tz_localize(None)
    data = pd.concat([data, btc_data['Close']], axis=1).ffill()
    return data, data0dte, datav, btc_data, datav2


def plot_top_chart(data, data0dte):
    fig, ax = plt.subplots(figsize=(24, 6))
    
    ax.plot(data.index, data['Close'], label='BTC Price', color='black', linewidth=1.5)
    ax.plot(data.index, data['high'], label='High', color='blue', linestyle='--', alpha=0.7)
    ax.plot(data.index, data['low'], label='Low', color='blue', linestyle='--', alpha=0.7)
    ax.plot(data.index, data['zero'], label='Zero', color='green', linestyle='-.', alpha=0.7)

    ax.plot(data0dte.index, data0dte['high'], label='0DTE High', color='blue', linestyle=':', alpha=0.8)
    ax.plot(data0dte.index, data0dte['low'], label='0DTE Low', color='blue', linestyle=':', alpha=0.8)
    ax.plot(data0dte.index, data0dte['zero'], label='0DTE Zero', color='green', linestyle=':', alpha=0.8)

    ax.grid(True, linestyle=':', alpha=0.5)
    ax.set_xticks([])
    ax.set_yticks([])
    fig.autofmt_xdate()
    return fig


def plot_bottom_chart(datav):
    fig, ax = plt.subplots(figsize=(24, 5))

    #ax.plot(datav.index, datav['puts'], label='Put', color='red', alpha=0.8)
    #ax.plot(datav.index, datav['calls'], label='Call', color='green', alpha=0.8)
    ax.plot(datav.index, (datav['calls'] + datav['puts']), label='Net', color='purple', linewidth=1)
    ax.plot(datav.index, -(datav['calls'] - datav['puts']), label='Gross', color='orange', linewidth=1, linestyle='--', alpha=1)
    ax.axhline(y=0, color='black', linestyle='-', linewidth=1)
    ax.grid(True, linestyle=':', alpha=0.5)
    ax.set_xticks([])
    ax.set_yticks([])
    fig.autofmt_xdate()
    return fig

def plot_bottom_2_chart(datav2):
    fig, ax = plt.subplots(figsize=(24, 5))

    #ax.plot(datav.index, datav['puts'], label='Put', color='red', alpha=0.8)
    #ax.plot(datav.index, datav['calls'], label='Call', color='green', alpha=0.8)
    ax.plot(datav2.index, (datav2['calls'] + datav2['puts']), label='Net', color='purple', linewidth=2)
    ax.plot(datav2.index, -(datav2['calls'] - datav2['puts']), label='Gross', color='orange', linewidth=2, linestyle='--', alpha=1)
    ax.axhline(y=0, color='black', linestyle='-', linewidth=1)
    ax.grid(True, linestyle=':', alpha=0.5)
    ax.set_xticks([])
    ax.set_yticks([])
    fig.autofmt_xdate()
    return fig
    
def main():
    st_autorefresh(interval=600000, key="datarefresh")
    with st.spinner("Загрузка данных..."):
        data, data0dte, datav, btc_data, datav2 = load_data()

    # Построение и отображение графиков
    fig1 = plot_top_chart(data, data0dte)
    st.pyplot(fig1)

    fig2 = plot_bottom_chart(datav)
    st.pyplot(fig2)

    fig3 = plot_bottom_2_chart(datav2)
    st.pyplot(fig3)
    
if __name__ == "__main__":
    main()
