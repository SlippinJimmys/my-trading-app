import streamlit as st
import yfinance as yf
from datetime import datetime
import time

st.set_page_config(page_title="My Trading App", layout="wide")
st.title("🚀 MY TRADING APP - Big Gains + Long-Term")
st.write("**$50-$100 Account** | Real-time Alerts | Day to 12-Month Outlook")

# Stocks
penny_stocks = ['XOS', 'SELX', 'HUBC', 'LASE', 'WCT', 'STAK', 'SBEV', 'DBGI', 'FNGR']
big_stocks = ['NVDA', 'AAPL', 'MSFT', 'AMZN', 'GOOGL', 'META', 'TSLA']

st.sidebar.header("Settings")
refresh_rate = st.sidebar.slider("Refresh Rate (seconds)", 15, 60, 30)
capital = st.sidebar.number_input("Your Capital ($)", value=50, min_value=10)

tab1, tab2, tab3, tab4, tab5 = st.tabs(["📍 DAY JUMPS", "📍 WEEK", "📍 MONTH", "📈 BIG COMPANIES (Long-Term)", "📊 MARKET TRENDS"])

def get_data(ticker):
    try:
        info = yf.Ticker(ticker).info
        return {
            'price': info.get('currentPrice', 0),
            'change': info.get('regularMarketChangePercent', 0),
            'target': info.get('targetMeanPrice', 0)
        }
    except:
        return {'price': 0, 'change': 0, 'target': 0}

placeholder = st.empty()

while True:
    with placeholder.container():
        st.write(f"**Last Updated:** {datetime.now().strftime('%H:%M:%S')}")

        # DAY JUMPS
        with tab1:
            st.subheader("📍 DAY JUMPS (Best for Quick Gains)")
            for ticker in penny_stocks:
                data = get_data(ticker)
                if data['change'] >= 15:
                    st.error(f"🔥🔥 {ticker} → ${data['price']:.3f} | +{data['change']:.1f}%")
                elif data['change'] >= 8:
                    st.warning(f"✅ {ticker} → ${data['price']:.3f} | +{data['change']:.1f}%")
                elif data['change'] > 3:
                    st.info(f"{ticker} → ${data['price']:.3f} | +{data['change']:.1f}%")

        # WEEK & MONTH (shortened)
        with tab2:
            st.subheader("📍 WEEK JUMPS")
            for ticker in penny_stocks:
                data = get_data(ticker)
                if data['change'] > 4:
                    st.success(f"📈 {ticker} → ${data['price']:.3f} | +{data['change']:.1f}%")

        with tab3:
            st.subheader("📍 MONTH JUMPS")
            for ticker in penny_stocks:
                data = get_data(ticker)
                if data['price'] < 10:
                    st.write(f"🏦 {ticker} → ${data['price']:.3f}")

        # NEW LONG-TERM TAB
        with tab4:
            st.subheader("📈 BIG COMPANIES - Long Term Outlook")
            st.write("**More Stable Companies** | Analyst & Trend Based Predictions (June 2026)")

            for ticker in big_stocks:
                data = get_data(ticker)
                target = data['target']
                upside = ((target / data['price']) - 1) * 100 if data['price'] > 0 else 0
                
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.write(f"**{ticker}**")
                    st.write(f"Current: **${data['price']:.2f}**")
                with col2:
                    if upside > 15:
                        st.success(f"1M: Bullish | 3M: Strong | 6M: Very Strong | 12M: **+{upside:.1f}%** Upside")
                    elif upside > 8:
                        st.info(f"1M: Neutral+ | 3M: Positive | 6M: Good | 12M: **+{upside:.1f}%** Upside")
                    else:
                        st.warning(f"1M: Cautious | 3M: Neutral | 6M: Moderate | 12M: **+{upside:.1f}%** Upside")

        # MARKET TRENDS
        with tab5:
            st.subheader("📊 CURRENT MARKET TRENDS")
            st.info("**Positive:** Strong AI momentum continuing")
            st.warning("**Risks:** High valuations, inflation, energy prices")
            st.write("Overall: Good for big tech long-term but volatile short-term.")

        st.caption(f"Risk Reminder: With ${capital}, only risk $5-$10 max per trade.")

    time.sleep(refresh_rate)
