import streamlit as st
import yfinance as yf
from datetime import datetime
import time

st.set_page_config(page_title="My Trading App", layout="wide")
st.title("🚀 MY TRADING APP - Easy Buy Recommendations")
st.write("**$50-$100 Account** | Clear Signals | Updated June 2026")

penny_stocks = ['XOS', 'SELX', 'HUBC', 'LASE', 'WCT', 'STAK', 'SBEV', 'DBGI', 'FNGR']
big_stocks = ['NVDA', 'AAPL', 'MSFT', 'AMZN', 'GOOGL', 'TSLA', 'META']

st.sidebar.header("My Settings")
refresh_rate = st.sidebar.slider("Refresh every (seconds)", 15, 60, 30)
capital = st.sidebar.number_input("My Capital ($)", value=50, min_value=10)

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🔥 TODAY'S BUYS", 
    "📅 1 WEEK BUYS", 
    "📆 1 MONTH BUYS", 
    "📈 BIG COMPANIES", 
    "📊 MARKET TRENDS"
])

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

        # TODAY'S BUYS
        with tab1:
            st.subheader("🔥 TODAY'S BEST BUYS (Strong Momentum)")
            for ticker in penny_stocks:
                data = get_data(ticker)
                if data['change'] >= 10:
                    st.success(f"🟢 **STRONG BUY** {ticker} → ${data['price']:.3f} | **+{data['change']:.1f}%**")
                    st.write(f"   → Risk $5-$10 | Target: +20-40% today")
                elif data['change'] >= 5:
                    st.info(f"🟡 **CONSIDER** {ticker} → ${data['price']:.3f} | +{data['change']:.1f}%")

        # 1 WEEK BUYS
        with tab2:
            st.subheader("📅 1 WEEK BUYS")
            for ticker in penny_stocks:
                data = get_data(ticker)
                if data['change'] > 3:
                    st.success(f"📈 **BUY** {ticker} → ${data['price']:.3f} | +{data['change']:.1f}%")

        # 1 MONTH BUYS
        with tab3:
            st.subheader("📆 1 MONTH BUYS")
            for ticker in penny_stocks:
                data = get_data(ticker)
                if data['price'] < 8 and data['change'] > 2:
                    st.success(f"🏦 **BUY** {ticker} → ${data['price']:.3f} | +{data['change']:.1f}%")

        # BIG COMPANIES - SEPARATED BY TIMEFRAME
        with tab4:
            st.subheader("📈 BIG COMPANIES - Long Term Outlook")
            
            for ticker in big_stocks:
                data = get_data(ticker)
                upside = ((data['target'] / data['price']) - 1) * 100 if data['price'] > 0 else 0
                
                st.write(f"**{ticker}** → Current: ${data['price']:.2f}")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    if upside > 8:
                        st.success(f"**1 Month:** Bullish")
                    else:
                        st.info(f"**1 Month:** Neutral")
                
                with col2:
                    if upside > 10:
                        st.success(f"**3 Month:** Positive")
                    else:
                        st.info(f"**3 Month:** Neutral")
                
                with col3:
                    if upside > 12:
                        st.success(f"**6 Month:** Strong")
                    else:
                        st.info(f"**6 Month:** Moderate")
                
                with col4:
                    if upside > 15:
                        st.success(f"**12 Month:** **+{upside:.1f}%**")
                    elif upside > 8:
                        st.info(f"**12 Month:** +{upside:.1f}%")
                    else:
                        st.warning(f"**12 Month:** +{upside:.1f}%")

        # MARKET TRENDS
        with tab5:
            st.subheader("📊 MARKET TRENDS")
            st.info("**Positive:** AI momentum still strong, good earnings")
            st.warning("**Risks:** High valuations, inflation, energy prices")
            st.write("**Overall:** Good for momentum plays but use small size.")

        st.caption(f"**Risk Rule:** With ${capital}, max $5-$10 per trade. Sell fast on +20-40% or cut at -10%.")

    time.sleep(refresh_rate)
