import streamlit as st
import yfinance as yf
from datetime import datetime
import time

st.set_page_config(page_title="My Trading App", layout="wide")
st.title("🚀 MY TRADING APP - Easy Buy Recommendations")
st.write("**$50-$100 Account** | Clear Signals | Updated June 2026")

penny_stocks = ['XOS', 'SELX', 'HUBC', 'LASE', 'WCT', 'STAK', 'SBEV', 'DBGI', 'FNGR']
big_stocks = ['NVDA', 'AAPL', 'MSFT', 'AMZN', 'GOOGL', 'TSLA', 'META']
all_stocks = ['NVDA', 'AAPL', 'MSFT', 'AMZN', 'GOOGL', 'TSLA', 'META', 'AVGO', 'COST', 'NFLX']

st.sidebar.header("My Settings")
refresh_rate = st.sidebar.slider("Refresh every (seconds)", 15, 60, 30)
capital = st.sidebar.number_input("My Capital ($)", value=50, min_value=10)

# VERTICAL NAVIGATION (Sidebar)
st.sidebar.markdown("---")
st.sidebar.subheader("📍 Navigation")

page = st.sidebar.radio(
    "Choose Section:",
    [
        "🔥 Today's Buys",
        "📅 1 Week Buys", 
        "📆 1 Month Buys",
        "📈 Big Companies",
        "💵 Stocks by Price Range",
        "📊 Market Trends"
    ],
    horizontal=False  # This makes it vertical
)

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
        if page == "🔥 Today's Buys":
            st.subheader("🔥 TODAY'S BEST BUYS (Strong Momentum)")
            for ticker in penny_stocks:
                data = get_data(ticker)
                if data['change'] >= 10:
                    st.success(f"🟢 **STRONG BUY** {ticker} → ${data['price']:.3f} | **+{data['change']:.1f}%**")
                    st.write(f"   → Risk $5-$10 | Target: +20-40% today")
                elif data['change'] >= 5:
                    st.info(f"🟡 **CONSIDER** {ticker} → ${data['price']:.3f} | +{data['change']:.1f}%")

        # ========== 1 WEEK BUYS ==========
        elif page == "📅 1 Week Buys":
            st.subheader("📅 1 WEEK BUYS")
            for ticker in penny_stocks:
                data = get_data(ticker)
                if data['change'] > 3:
                    st.success(f"📈 **BUY** {ticker} → ${data['price']:.3f} | +{data['change']:.1f}%")

        # ========== 1 MONTH BUYS ==========
        elif page == "📆 1 Month Buys":
            st.subheader("📆 1 MONTH BUYS")
            for ticker in penny_stocks:
                data = get_data(ticker)
                if data['price'] < 8 and data['change'] > 2:
                    st.success(f"🏦 **BUY** {ticker} → ${data['price']:.3f} | +{data['change']:.1f}%")

        # ========== BIG COMPANIES ==========
        elif page == "📈 Big Companies":
            st.subheader("📈 BIG COMPANIES - Long Term Outlook")
            for ticker in big_stocks:
                data = get_data(ticker)
                upside = ((data['target'] / data['price']) - 1) * 100 if data['price'] > 0 else 0
                st.write(f"**{ticker}** → ${data['price']:.2f}")
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.write("**1M**" if upside > 8 else "1M")
                with col2:
                    st.write("**3M**" if upside > 10 else "3M")
                with col3:
                    st.write("**6M**" if upside > 12 else "6M")
                with col4:
                    if upside > 15:
                        st.success(f"+{upside:.1f}%")
                    else:
                        st.write(f"+{upside:.1f}%")

        # ========== STOCKS BY PRICE RANGE ==========
        elif page == "💵 Stocks by Price Range":
            st.subheader("💵 STOCKS BY PRICE RANGE")
            
            price_tab1, price_tab2, price_tab3, price_tab4 = st.tabs([
                "$100-$200", "$200-$300", "$300-$400", "$400-$500"
            ])
            
            with price_tab1:
                st.write("**Stocks $100 - $200**")
                for ticker in all_stocks:
                    data = get_data(ticker)
                    if 100 <= data['price'] < 200:
                        st.success(f"**{ticker}** → ${data['price']:.2f} | +{data['change']:.1f}%")
            
            with price_tab2:
                st.write("**Stocks $200 - $300**")
                for ticker in all_stocks:
                    data = get_data(ticker)
                    if 200 <= data['price'] < 300:
                        st.success(f"**{ticker}** → ${data['price']:.2f} | +{data['change']:.1f}%")
            
            with price_tab3:
                st.write("**Stocks $300 - $400**")
                for ticker in all_stocks:
                    data = get_data(ticker)
                    if 300 <= data['price'] < 400:
                        st.success(f"**{ticker}** → ${data['price']:.2f} | +{data['change']:.1f}%")
            
            with price_tab4:
                st.write("**Stocks $400 - $500**")
                for ticker in all_stocks:
                    data = get_data(ticker)
                    if 400 <= data['price'] < 500:
                        st.success(f"**{ticker}** → ${data['price']:.2f} | +{data['change']:.1f}%")

        # ========== MARKET TRENDS ==========
        elif page == "📊 Market Trends":
            st.subheader("📊 MARKET TRENDS")
            st.info("**Positive:** AI momentum still strong, good earnings")
            st.warning("**Risks:** High valuations, inflation, energy prices")
            st.write("**Overall:** Good for momentum plays but use small size.")

        st.caption(f"**Risk Rule:** With ${capital}, max $5-$10 per trade. Sell fast on +20-40% or cut at -10%.")

    time.sleep(refresh_rate)
