import streamlit as st
import yfinance as yf
from datetime import datetime
import time

st.set_page_config(page_title="My Trading App", layout="wide")
st.title("🚀 MY TRADING APP - Big Gains Focus")
st.write("**$50-$100 Account** | Real-time Alerts | Day/Week/Month")

stocks = ['XOS', 'SELX', 'HUBC', 'LASE', 'WCT', 'STAK', 'SBEV', 'DBGI', 'FNGR', 'NVTS']

st.sidebar.header("Settings")
refresh_rate = st.sidebar.slider("Refresh Rate (seconds)", 15, 60, 30)
capital = st.sidebar.number_input("Your Capital ($)", value=50, min_value=10)

tab1, tab2, tab3, tab4 = st.tabs(["📍 DAY JUMPS", "📍 WEEK JUMPS", "📍 MONTH JUMPS", "📊 MARKET TRENDS"])

def get_data(ticker):
    try:
        info = yf.Ticker(ticker).info
        return {
            'price': info.get('currentPrice', 0),
            'change': info.get('regularMarketChangePercent', 0),
            'volume': info.get('volume', 0)
        }
    except:
        return {'price': 0, 'change': 0, 'volume': 0}

placeholder = st.empty()

while True:
    with placeholder.container():
        st.write(f"**Last Updated:** {datetime.now().strftime('%H:%M:%S')}")

        with tab1:
            st.subheader("📍 DAY JUMPS - Best for Quick Gains")
            for ticker in stocks:
                data = get_data(ticker)
                if data['change'] >= 15:
                    st.error(f"🔥🔥 {ticker} → ${data['price']:.3f} | +{data['change']:.1f}%")
                elif data['change'] >= 8:
                    st.warning(f"✅ {ticker} → ${data['price']:.3f} | +{data['change']:.1f}%")
                elif data['change'] > 3:
                    st.info(f"{ticker} → ${data['price']:.3f} | +{data['change']:.1f}%")

        with tab2:
            st.subheader("📍 WEEK JUMPS")
            for ticker in stocks:
                data = get_data(ticker)
                if data['change'] > 4:
                    st.success(f"📈 {ticker} → ${data['price']:.3f} | +{data['change']:.1f}%")

        with tab3:
            st.subheader("📍 MONTH JUMPS")
            for ticker in stocks:
                data = get_data(ticker)
                if data['price'] < 10:
                    st.write(f"🏦 {ticker} → ${data['price']:.3f}")

        with tab4:
            st.subheader("📊 MARKET TRENDS")
            st.info("**Positive:** AI momentum still strong")
            st.warning("**Negative:** High valuations + inflation concerns")
            st.write("Overall: Volatile market — good for momentum plays")

        st.caption(f"Risk Reminder: Only use ${capital} wisely. Max $5-$10 per trade.")

    time.sleep(refresh_rate)
