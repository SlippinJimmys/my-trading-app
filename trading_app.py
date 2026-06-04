✅ Cleaned Up & Upgraded!
I fixed the errors (removed the unstable auto-refresh loop) and added real-time chart visualization.
Now you can:

Click "Refresh Data" button to update
Select any stock from a dropdown
See a live price chart for that stock

Final Clean Code (Replace your trading_app.py):
Pythonimport streamlit as st
import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd

st.set_page_config(page_title="My Trading App", layout="wide")
st.title("🚀 MY TRADING APP - Clean & Easy")
st.write("**$50-$100 Account** | Clear Buy Signals + Charts")

# Stocks
penny_stocks = ['XOS', 'SELX', 'HUBC', 'LASE', 'WCT', 'STAK', 'SBEV', 'DBGI', 'FNGR']
big_stocks = ['NVDA', 'AAPL', 'MSFT', 'AMZN', 'GOOGL', 'TSLA', 'META']
all_stocks = list(set(penny_stocks + big_stocks))

st.sidebar.header("Settings")
capital = st.sidebar.number_input("My Capital ($)", value=50, min_value=10)

# Vertical Navigation
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
        "📈 Market Trends"
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
            'target': info.get('targetMeanPrice', 0),
            'volume': info.get('volume', 0)
        }
    except:
        return {'price': 0, 'change': 0, 'target': 0, 'volume': 0}

def get_chart_data(ticker, days=30):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=f"{days}d")
        return hist
    except:
        return pd.DataFrame()

# Refresh Button
if st.button("🔄 Refresh Data"):
    st.rerun()

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
        with col1: st.write("**1M**" if upside > 8 else "1M")
        with col2: st.write("**3M**" if upside > 10 else "3M")
        with col3: st.write("**6M**" if upside > 12 else "6M")
        with col4: 
            if upside > 15: st.success(f"+{upside:.1f}%")
            else: st.write(f"+{upside:.1f}%")

# ========== STOCKS BY PRICE ==========
elif page == "💵 Stocks by Price":
    st.subheader("💵 STOCKS BY PRICE RANGE")
    p1, p2, p3, p4 = st.tabs(["$100-$200", "$200-$300", "$300-$400", "$400-$500"])
    
    with p1:
        for ticker in all_stocks:
            data = get_data(ticker)
            if 100 <= data['price'] < 200:
                st.success(f"**{ticker}** → ${data['price']:.2f} | +{data['change']:.1f}%")
    with p2:
        for ticker in all_stocks:
            data = get_data(ticker)
            if 200 <= data['price'] < 300:
                st.success(f"**{ticker}** → ${data['price']:.2f} | +{data['change']:.1f}%")
    with p3:
        for ticker in all_stocks:
            data = get_data(ticker)
            if 300 <= data['price'] < 400:
                st.success(f"**{ticker}** → ${data['price']:.2f} | +{data['change']:.1f}%")
    with p4:
        for ticker in all_stocks:
            data = get_data(ticker)
            if 400 <= data['price'] < 500:
                st.success(f"**{ticker}** → ${data['price']:.2f} | +{data['change']:.1f}%")

# ========== CHARTS & ANALYSIS ==========
elif page == "📊 Charts & Analysis":
    st.subheader("📊 REAL-TIME CHARTS")
    
    selected_stock = st.selectbox("Select a stock to see its chart:", all_stocks)
    
    if selected_stock:
        data = get_data(selected_stock)
        st.write(f"**{selected_stock}** → Current Price: **${data['price']:.2f}** | Change: **{data['change']:.1f}%**")
        
        # Get chart data
        chart_data = get_chart_data(selected_stock, days=30)
        
        if not chart_data.empty:
            st.line_chart(chart_data['Close'], use_container_width=True)
            st.write("**30-Day Price Chart**")
        else:
            st.warning("Could not load chart data.")

# ========== MARKET TRENDS ==========
elif page == "📊 Market Trends":
    st.subheader("📊 MARKET TRENDS")
    st.info("**Positive:** AI momentum still strong, good earnings")
    st.warning("**Risks:** High valuations, inflation, energy prices")
    st.write("**Overall:** Good for momentum plays but use small size.")

st.caption(f"**Risk Rule:** With ${capital}, max $5-$10 per trade. Sell fast on +20-40% or cut at -10%.")
