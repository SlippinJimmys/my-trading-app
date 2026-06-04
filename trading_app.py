import streamlit as st
import yfinance as yf
from datetime import datetime
import time

st.set_page_config(page_title="My Trading App", layout="wide")
st.title("🚀 MY TRADING APP - Easy Buy Recommendations")
st.write("**$50-$100 Account** | Clear Signals | Updated June 2026")

# Stocks to monitor
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

        # ========== TODAY'S BUYS ==========
        with tab1:
            st.subheader("🔥 TODAY'S BEST BUYS (Strong Momentum)")
            st.write("**Best stocks right now for quick gains**")
            
            strong_buys = []
            for ticker in penny_stocks:
                data = get_data(ticker)
                if data['change'] >= 10:
                    st.success(f"🟢 **STRONG BUY** {ticker} → ${data['price']:.3f} | **+{data['change']:.1f}%**")
                    st.write(f"   → Risk only $5-$10 | Good volume & momentum")
                    strong_buys.append(ticker)
                elif data['change'] >= 5:
                    st.info(f"🟡 **CONSIDER** {ticker} → ${data['price']:.3f} | +{data['change']:.1f}%")
            
            if not strong_buys:
                st.write("No strong momentum stocks right now. Wait for better setup.")

        # ========== 1 WEEK BUYS ==========
        with tab2:
            st.subheader("📅 1 WEEK BUYS (Good for Short-Term Hold)")
            for ticker in penny_stocks:
                data = get_data(ticker)
                if data['change'] > 3:
                    st.success(f"📈 **BUY** {ticker} → ${data['price']:.3f} | +{data['change']:.1f}%")
                    st.write(f"   → Potential for continued move this week")

        # ========== 1 MONTH BUYS ==========
        with tab3:
            st.subheader("📆 1 MONTH BUYS (Better for Holding)")
            for ticker in penny_stocks:
                data = get_data(ticker)
                if data['price'] < 8 and data['change'] > 2:
                    st.success(f"🏦 **BUY** {ticker} → ${data['price']:.3f} | +{data['change']:.1f}%")
                    st.write(f"   → Good price + momentum for 1 month hold")

        # ========== BIG COMPANIES ==========
        with tab4:
            st.subheader("📈 BIG COMPANIES - Long Term")
            for ticker in big_stocks:
                data = get_data(ticker)
                upside = ((data['target'] / data['price']) - 1) * 100 if data['price'] > 0 else 0
                
                if upside > 12:
                    st.success(f"**BUY** {ticker} → ${data['price']:.2f} | **{upside:.1f}%** Upside (12 months)")
                elif upside > 5:
                    st.info(f"{ticker} → ${data['price']:.2f} | {upside:.1f}% Upside")
                else:
                    st.write(f"{ticker} → ${data['price']:.2f} | {upside:.1f}% Upside")

        # ========== MARKET TRENDS ==========
        with tab5:
            st.subheader("📊 MARKET TRENDS")
            st.info("**Positive:** AI momentum still strong, good earnings")
            st.warning("**Risks:** High valuations, inflation, energy prices")
            st.write("**Overall:** Good for momentum plays but use small size.")

        st.caption(f"**Risk Rule:** With ${capital}, max $5-$10 per trade. Sell fast on +20-40% or cut at -10%.")

    time.sleep(refresh_rate)
