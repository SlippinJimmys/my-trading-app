import streamlit as st
import yfinance as yf
from datetime import datetime
import time

st.set_page_config(page_title="My Trading App", layout="wide")
st.title("🚀 MY TRADING APP - Easy & Smart")
st.write("**$50-$100 Account** | Clear Buy Recommendations")

# Stocks
penny_stocks = ['XOS', 'SELX', 'HUBC', 'LASE', 'WCT', 'STAK', 'SBEV']
big_stocks = ['NVDA', 'AAPL', 'MSFT', 'AMZN', 'GOOGL', 'TSLA']

st.sidebar.header("My Settings")
refresh_rate = st.sidebar.slider("Refresh every (seconds)", 15, 60, 30)
capital = st.sidebar.number_input("My Capital ($)", value=50, min_value=10)

tab1, tab2, tab3, tab4, tab5 = st.tabs(["🔥 TODAY'S BUYS", "📍 DAY JUMPS", "📈 BIG COMPANIES", "📊 MARKET TRENDS", "💡 MY ADVICE"])

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

        # ==================== TODAY'S BUY RECOMMENDATIONS ====================
        with tab1:
            st.subheader("🔥 TODAY'S BUY RECOMMENDATIONS")
            st.write("**Best stocks right now for potential gains** (Based on momentum)")

            for ticker in penny_stocks:
                data = get_data(ticker)
                if data['change'] >= 10:
                    st.success(f"🟢 **BUY** {ticker} → ${data['price']:.3f} | +{data['change']:.1f}%  ← **High Potential**")
                    st.write(f"→ Risk $5–10 | Target: +20-40% today")
                elif data['change'] >= 5:
                    st.info(f"🟡 **Consider Buying** {ticker} → ${data['price']:.3f} | +{data['change']:.1f}%")
                else:
                    st.write(f"⚪ {ticker} → ${data['price']:.3f} | +{data['change']:.1f}%")

        # DAY JUMPS
        with tab2:
            st.subheader("📍 DAY JUMPS")
            for ticker in penny_stocks:
                data = get_data(ticker)
                if data['change'] >= 8:
                    st.warning(f"✅ {ticker} → ${data['price']:.3f} | +{data['change']:.1f}%")

        # BIG COMPANIES LONG TERM
        with tab3:
            st.subheader("📈 BIG COMPANIES - Long Term")
            for ticker in big_stocks:
                data = get_data(ticker)
                upside = ((data['target'] / data['price']) - 1) * 100 if data['price'] > 0 else 0
                if upside > 15:
                    st.success(f"**BUY** {ticker} → ${data['price']:.2f} | **{upside:.1f}%** Upside (12 months)")
                else:
                    st.write(f"{ticker} → ${data['price']:.2f} | {upside:.1f}% Upside")

        # MARKET TRENDS
        with tab4:
            st.subheader("📊 MARKET TRENDS")
            st.info("**Positive:** AI sector still strong")
            st.warning("**Risks:** High valuations and inflation pressure")
            st.write("**Overall:** Good for short-term momentum trades but be careful.")

        # MY ADVICE
        with tab5:
            st.subheader("💡 MY PERSONAL ADVICE")
            st.write(f"With **${capital}**, here’s what I recommend:")
            st.write("• Risk **maximum $5-$10** per trade")
            st.write("• Focus on strong green momentum in the first 30-60 minutes")
            st.write("• Sell quickly: Take 20-40% profit or cut loss at -10%")
            st.warning("Remember: Penny stocks are very risky. You can lose your entire amount.")

        st.caption("Tip: Refresh often and only buy when you see strong green momentum.")

    time.sleep(refresh_rate)
