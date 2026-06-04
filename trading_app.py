import streamlit as st
import yfinance as yf
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="My Trading App", layout="wide")
st.title("🚀 MY TRADING APP - Clean & Easy")
st.write("**$50-$100 Account** | Clear Buy Signals + Charts")

penny_stocks = ['XOS', 'SELX', 'HUBC', 'LASE', 'WCT', 'STAK', 'SBEV', 'DBGI', 'FNGR']
big_stocks = ['NVDA', 'AAPL', 'MSFT', 'AMZN', 'GOOGL', 'TSLA', 'META']
all_stocks = list(set(penny_stocks + big_stocks))

st.sidebar.header("Settings")
capital = st.sidebar.number_input("My Capital ($)", value=50, min_value=10)

st.sidebar.markdown("---")
page = st.sidebar.radio(
    "Choose Section:",
    [
        "🔥 Today's Buys",
        "📅 1 Week Buys", 
        "📆 1 Month Buys",
        "📈 Big Companies",
        "💵 Stocks by Price",
        "📊 Charts & Analysis",
        "📊 Market Trends"
    ],
    horizontal=False
)

def get_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        return {
            'price': info.get('currentPrice', 0),
            'change': info.get('regularMarketChangePercent', 0),
            'target': info.get('targetMeanPrice', 0)
        }
    except:
        return {'price': 0, 'change': 0, 'target': 0}

if st.button("🔄 Refresh Data"):
    st.rerun()

st.write(f"**Last Updated:** {datetime.now().strftime('%H:%M:%S')}")

# TODAY'S BUYS
if page == "🔥 Today's Buys":
    st.subheader("🔥 TODAY'S BEST BUYS (Strong Momentum)")
    for ticker in penny_stocks:
        data = get_data(ticker)
        if data['change'] >= 10:
            st.success(f"🟢 **STRONG BUY** {ticker} → ${data['price']:.3f} | **+{data['change']:.1f}%**")
            st.write(f"   → Risk $5-$10 | Target: +20-40% today")
        elif data['change'] >= 5:
            st.info(f"🟡 **CONSIDER** {ticker} → ${data['price']:.3f} | +{data['change']:.1f}%")

# 1 WEEK BUYS
elif page == "📅 1 Week Buys":
    st.subheader("📅 1 WEEK BUYS")
    for ticker in penny_stocks:
        data = get_data(ticker)
        if data['change'] > 3:
            st.success(f"📈 **BUY** {ticker} → ${data['price']:.3f} | +{data['change']:.1f}%")

# 1 MONTH BUYS
elif page == "📆 1 Month Buys":
    st.subheader("📆 1 MONTH BUYS")
    for ticker in penny_stocks:
        data = get_data(ticker)
        if data['price'] < 8 and data['change'] > 2:
            st.success(f"🏦 **BUY** {ticker} → ${data['price']:.3f} | +{data['change']:.1f}%")

# BIG COMPANIES (CLEANED)
elif page == "📈 Big Companies":
    st.subheader("📈 BIG COMPANIES - Long Term Outlook")
    
    for ticker in big_stocks:
        data = get_data(ticker)
        upside = ((data['target'] / data['price']) - 1) * 100 if data['price'] > 0 else 0
        
        st.write(f"**{ticker}** → Current: ${data['price']:.2f}")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if upside > 8:
                st.success("**1 Month:** Bullish")
            else:
                st.info("**1 Month:** Neutral")
        
        with col2:
            if upside > 10:
                st.success("**3 Month:** Positive")
            else:
                st.info("**3 Month:** Neutral")
        
        with col3:
            if upside > 12:
                st.success("**6 Month:** Strong")
            else:
                st.info("**6 Month:** Moderate")
        
        with col4:
            if upside > 15:
                st.success(f"**12 Month:** +{upside:.1f}%")
            elif upside > 8:
                st.info(f"**12 Month:** +{upside:.1f}%")
            else:
                st.warning(f"**12 Month:** +{upside:.1f}%")

# STOCKS BY PRICE (CLEANED)
elif page == "💵 Stocks by Price":
    st.subheader("💵 STOCKS BY PRICE RANGE")
    
    price_range = st.selectbox(
        "Select Price Range:",
        ["$100 - $200", "$200 - $300", "$300 - $400", "$400 - $500"]
    )
    
    min_price = 100
    max_price = 200
    
    if price_range == "$100 - $200":
        min_price, max_price = 100, 200
    elif price_range == "$200 - $300":
        min_price, max_price = 200, 300
    elif price_range == "$300 - $400":
        min_price, max_price = 300, 400
    elif price_range == "$400 - $500":
        min_price, max_price = 400, 500
    
    st.write(f"**Showing stocks between ${min_price} - ${max_price}**")
    
    found = False
    for ticker in all_stocks:
        data = get_data(ticker)
        if min_price <= data['price'] < max_price:
            st.success(f"**{ticker}** → ${data['price']:.2f} | +{data['change']:.1f}%")
            found = True
    
    if not found:
        st.info(f"No stocks currently in the ${min_price}-${max_price} range.")

# CHARTS & ANALYSIS
elif page == "📊 Charts & Analysis":
    st.subheader("📊 REAL-TIME CHARTS")
    
    selected_stock = st.selectbox("Select a stock to see its chart:", all_stocks)
    
    if selected_stock:
        data = get_data(selected_stock)
        st.write(f"**{selected_stock}** → Current: **${data['price']:.2f}** | Change: **{data['change']:.1f}%**")
        
        try:
            hist = yf.Ticker(selected_stock).history(period="30d")
            if not hist.empty:
                st.line_chart(hist['Close'], use_container_width=True)
                st.write("**30-Day Price Chart**")
            else:
                st.warning("No chart data available.")
        except:
            st.warning("Could not load chart.")

# MARKET TRENDS
elif page == "📊 Market Trends":
    st.subheader("📊 MARKET TRENDS")
    st.info("**Positive:** AI momentum still strong, good earnings")
    st.warning("**Risks:** High valuations, inflation, energy prices")
    st.write("**Overall:** Good for momentum plays but use small size.")

st.caption(f"**Risk Rule:** With ${capital}, max $5-$10 per trade. Sell fast on +20-40% or cut at -10%.")
