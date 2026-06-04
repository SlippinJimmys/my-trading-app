import streamlit as st
import yfinance as yf
from datetime import datetime
import pytz
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="My Trading App", layout="wide")
st.title("🚀 MY TRADING APP")
st.write("**$50-$100 Account** | Smart Signals + Interactive Charts")

penny_stocks = ['XOS', 'SELX', 'HUBC', 'LASE', 'WCT', 'STAK', 'SBEV', 'DBGI', 'FNGR']
big_stocks = ['NVDA', 'AAPL', 'MSFT', 'AMZN', 'GOOGL', 'TSLA', 'META', 'AVGO', 'COST', 'NFLX', 'ADBE', 'CRM', 'AMD', 'INTC', 'QCOM', 'TXN', 'MU', 'AMAT', 'LRCX', 'KLAC', 'PANW', 'CRWD']
upcoming_stocks = ['PLTR', 'ARM', 'SMCI', 'SNOW', 'DDOG', 'NET', 'MDB', 'ZS', 'OKTA', 'RBLX', 'COIN', 'HOOD', 'SOFI', 'RDDT', 'APP']
all_stocks = list(set(penny_stocks + big_stocks + upcoming_stocks))

st.sidebar.header("⚙️ Settings")
capital = st.sidebar.number_input("My Capital ($)", value=50, min_value=10)
max_risk = st.sidebar.slider("Max Risk per Trade ($)", 5, 20, 10)

st.sidebar.markdown("---")
page = st.sidebar.radio(
    "📍 Navigation",
    [
        "🏠 Dashboard",
        "⭐ Today's Highlights",
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
            'target': info.get('targetMeanPrice', 0),
            'name': info.get('shortName', ticker),
            'volume': info.get('volume', 0)
        }
    except:
        return {'price': 0, 'change': 0, 'target': 0, 'name': ticker, 'volume': 0}

if st.button("🔄 Refresh All Data"):
    st.rerun()

pacific = pytz.timezone('US/Pacific')
current_time = datetime.now(pacific).strftime('%I:%M:%S %p PT')

# ========== DASHBOARD ==========
if page == "🏠 Dashboard":
    st.subheader("📊 Quick Dashboard")
    st.write(f"**Last Updated:** {current_time}")
    
    col1, col2, col3 = st.columns(3)
    strong_buys_today = sum(1 for t in penny_stocks if get_data(t)['change'] >= 10)
    
    with col1:
        st.metric("Strong Buys Today", strong_buys_today)
    with col2:
        st.metric("Max Risk/Trade", f"${max_risk}")
    with col3:
        st.metric("Market Bias", "Bullish (AI Strong)")
    
    st.markdown("---")
    st.subheader("🔥 Top Movers Right Now")
    movers = []
    for ticker in penny_stocks:
        data = get_data(ticker)
        if data['change'] >= 5:
            movers.append((ticker, data['name'], data['price'], data['change']))
    
    if movers:
        movers.sort(key=lambda x: x[3], reverse=True)
        for t, name, price, chg in movers[:5]:
            st.success(f"**{t} - {name}** → ${price:.3f} | **+{chg:.1f}%**")
    else:
        st.info("No strong movers right now.")

# ========== TODAY'S HIGHLIGHTS (NEW) ==========
elif page == "⭐ Today's Highlights":
    st.subheader("⭐ TOP 10 STOCKS WITH BEST POTENTIAL TODAY")
    st.write("**Strongest momentum + volume right now**")
    
    all_data = []
    for ticker in all_stocks:
        data = get_data(ticker)
        if data['change'] > 0 and data['volume'] > 100000:
            all_data.append((ticker, data['name'], data['price'], data['change'], data['volume']))
    
    all_data.sort(key=lambda x: x[3], reverse=True)
    
    for i, (ticker, name, price, chg, vol) in enumerate(all_data[:10], 1):
        st.success(f"**#{i} {ticker} - {name}** → ${price:.3f} | **+{chg:.1f}%** | Vol: {vol:,}")

# ========== TODAY'S BUYS ==========
elif page == "🔥 Today's Buys":
    st.subheader("🔥 TODAY'S BEST BUYS (Strong Momentum)")
    for ticker in penny_stocks:
        data = get_data(ticker)
        if data['change'] >= 10:
            st.success(f"🟢 **STRONG BUY** {ticker} - {data['name']} → ${data['price']:.3f} | **+{data['change']:.1f}%**")
            st.write(f"   → Risk max ${max_risk} | Target: +20-40% today")
        elif data['change'] >= 5:
            st.info(f"🟡 **CONSIDER** {ticker} - {data['name']} → ${data['price']:.3f} | +{data['change']:.1f}%")

# 1 WEEK BUYS
elif page == "📅 1 Week Buys":
    st.subheader("📅 1 WEEK BUYS")
    for ticker in penny_stocks:
        data = get_data(ticker)
        if data['change'] > 3:
            st.success(f"📈 **BUY** {ticker} - {data['name']} → ${data['price']:.3f} | +{data['change']:.1f}%")

# 1 MONTH BUYS
elif page == "📆 1 Month Buys":
    st.subheader("📆 1 MONTH BUYS")
    for ticker in penny_stocks:
        data = get_data(ticker)
        if data['price'] < 8 and data['change'] > 2:
            st.success(f"🏦 **BUY** {ticker} - {data['name']} → ${data['price']:.3f} | +{data['change']:.1f}%")

# BIG COMPANIES
elif page == "📈 Big Companies":
    st.subheader("📈 BIG COMPANIES + GROWTH STOCKS - Long Term Outlook")
    for ticker in big_stocks + upcoming_stocks:
        data = get_data(ticker)
        upside = ((data['target'] / data['price']) - 1) * 100 if data['price'] > 0 else 0
        st.write(f"**{ticker} - {data['name']}** → ${data['price']:.2f}")
        col1, col2, col3, col4 = st.columns(4)
        with col1: st.write("**1M**" if upside > 8 else "1M")
        with col2: st.write("**3M**" if upside > 10 else "3M")
        with col3: st.write("**6M**" if upside > 12 else "6M")
        with col4: 
            if upside > 15: st.success(f"+{upside:.1f}%")
            else: st.write(f"+{upside:.1f}%")

# STOCKS BY PRICE + FILTER
elif page == "💵 Stocks by Price":
    st.subheader("💵 STOCKS BY PRICE RANGE + FILTER")
    
    price_range = st.selectbox("Select Price Range:", ["$100-$200", "$200-$300", "$300-$400", "$400-$500", "$500+"])
    sort_order = st.selectbox("Sort by Price:", ["Lowest to Highest", "Highest to Lowest"])
    
    if price_range == "$100-$200": min_p, max_p = 100, 200
    elif price_range == "$200-$300": min_p, max_p = 200, 300
    elif price_range == "$300-$400": min_p, max_p = 300, 400
    elif price_range == "$400-$500": min_p, max_p = 400, 500
    else: min_p, max_p = 500, 9999
    
    filtered = []
    for ticker in all_stocks:
        data = get_data(ticker)
        if min_p <= data['price'] < max_p:
            filtered.append((ticker, data['name'], data['price'], data['change']))
    
    if sort_order == "Lowest to Highest":
        filtered.sort(key=lambda x: x[2])
    else:
        filtered.sort(key=lambda x: x[2], reverse=True)
    
    st.write(f"**Stocks between ${min_p} - ${max_p if max_p < 9999 else '500+'}** ({sort_order})")
    
    for ticker, name, price, chg in filtered:
        st.success(f"**{ticker} - {name}** → ${price:.2f} | +{chg:.1f}%")

# CHARTS & ANALYSIS
elif page == "📊 Charts & Analysis":
    st.subheader("📊 INTERACTIVE CANDLESTICK CHARTS")
    selected_stock = st.selectbox("Select a stock:", all_stocks)
    if selected_stock:
        data = get_data(selected_stock)
        st.write(f"**{selected_stock} - {data['name']}** → ${data['price']:.2f} | {data['change']:.1f}%")
        try:
            hist = yf.Ticker(selected_stock).history(period="60d")
            if not hist.empty:
                fig = go.Figure(data=[go.Candlestick(x=hist.index, open=hist['Open'], high=hist['High'], low=hist['Low'], close=hist['Close'])])
                fig.update_layout(title=f"{selected_stock} - {data['name']}", height=500, xaxis_rangeslider_visible=True, template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)
        except:
            st.warning("Could not load chart.")

# MARKET TRENDS
elif page == "📊 Market Trends":
    st.subheader("📊 MARKET TRENDS")
    st.info("**Positive:** AI momentum still strong")
    st.warning("**Risks:** High valuations + inflation pressure")
    st.write("**Overall:** Good for momentum plays. Be selective.")

st.caption(f"**Risk Rule:** Max ${max_risk} per trade. Sell fast on +20-40% or cut at -10%.")
