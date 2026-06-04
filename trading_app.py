import streamlit as st
import yfinance as yf
from datetime import datetime
import pytz
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="My Trading App", layout="wide")
st.title("🚀 MY TRADING APP")
st.write("**$50-$100 Account** | Smart Signals + Paper Trading + Options Education")

penny_stocks = ['XOS', 'SELX', 'HUBC', 'LASE', 'WCT', 'STAK', 'SBEV', 'DBGI', 'FNGR']
big_stocks = ['NVDA', 'AAPL', 'MSFT', 'AMZN', 'GOOGL', 'TSLA', 'META', 'AVGO', 'COST', 'NFLX', 'ADBE', 'CRM', 'AMD', 'INTC', 'QCOM', 'TXN', 'MU', 'AMAT', 'LRCX', 'KLAC', 'PANW', 'CRWD']
upcoming_stocks = ['PLTR', 'ARM', 'SMCI', 'SNOW', 'DDOG', 'NET', 'MDB', 'ZS', 'OKTA', 'RBLX', 'COIN', 'HOOD', 'SOFI', 'RDDT', 'APP']
all_stocks = list(set(penny_stocks + big_stocks + upcoming_stocks))

st.sidebar.header("⚙️ Settings")
capital = st.sidebar.number_input("My Capital ($)", value=50, min_value=10)
max_risk = st.sidebar.slider("Max Risk per Trade ($)", 5, 20, 10)

st.sidebar.markdown("---")
st.sidebar.subheader("🔍 Global Filters")
price_sort = st.sidebar.selectbox("Sort by Price", ["None", "Lowest → Highest", "Highest → Lowest"])
potential_sort = st.sidebar.selectbox("Sort by Potential", ["None", "Most Potential → Least"])

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
        "📈 Options Strategies",
        "📝 Paper Trading",
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

def apply_filters(stock_list):
    data_list = []
    for ticker in stock_list:
        data = get_data(ticker)
        upside = ((data['target'] / data['price']) - 1) * 100 if data['price'] > 0 else 0
        potential_score = data['change'] * 0.6 + upside * 0.4
        data_list.append((ticker, data['name'], data['price'], data['change'], upside, potential_score, data['volume']))
    
    if price_sort == "Lowest → Highest":
        data_list.sort(key=lambda x: x[2])
    elif price_sort == "Highest → Lowest":
        data_list.sort(key=lambda x: x[2], reverse=True)
    
    if potential_sort == "Most Potential → Least":
        data_list.sort(key=lambda x: x[5], reverse=True)
    
    return data_list

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

# ========== TODAY'S HIGHLIGHTS ==========
elif page == "⭐ Today's Highlights":
    st.subheader("⭐ TOP 10 STOCKS WITH BEST POTENTIAL TODAY")
    filtered = apply_filters(all_stocks)[:10]
    for i, (ticker, name, price, chg, upside, score, vol) in enumerate(filtered, 1):
        st.success(f"**#{i} {ticker} - {name}** → ${price:.3f} | **+{chg:.1f}%** | Upside: {upside:.1f}%")

# ========== TODAY'S BUYS ==========
elif page == "🔥 Today's Buys":
    st.subheader("🔥 TODAY'S BEST BUYS (Strong Momentum)")
    filtered = apply_filters(penny_stocks)
    for ticker, name, price, chg, upside, score, vol in filtered:
        if chg >= 10:
            st.success(f"🟢 **STRONG BUY** {ticker} - {name} → ${price:.3f} | **+{chg:.1f}%**")
            st.write(f"   → Risk max ${max_risk} | Target: +20-40% today")
        elif chg >= 5:
            st.info(f"🟡 **CONSIDER** {ticker} - {name} → ${price:.3f} | +{chg:.1f}%")

# 1 WEEK BUYS
elif page == "📅 1 Week Buys":
    st.subheader("📅 1 WEEK BUYS")
    filtered = apply_filters(penny_stocks)
    for ticker, name, price, chg, upside, score, vol in filtered:
        if chg > 3:
            st.success(f"📈 **BUY** {ticker} - {name} → ${price:.3f} | +{chg:.1f}%")

# 1 MONTH BUYS
elif page == "📆 1 Month Buys":
    st.subheader("📆 1 MONTH BUYS")
    filtered = apply_filters(penny_stocks)
    for ticker, name, price, chg, upside, score, vol in filtered:
        if price < 8 and chg > 2:
            st.success(f"🏦 **BUY** {ticker} - {name} → ${price:.3f} | +{chg:.1f}%")

# BIG COMPANIES
elif page == "📈 Big Companies":
    st.subheader("📈 BIG COMPANIES + GROWTH STOCKS - Long Term Outlook")
    filtered = apply_filters(big_stocks + upcoming_stocks)
    for ticker, name, price, chg, upside, score, vol in filtered:
        st.write(f"**{ticker} - {name}** → ${price:.2f}")
        col1, col2, col3, col4 = st.columns(4)
        with col1: st.write("**1M**" if upside > 8 else "1M")
        with col2: st.write("**3M**" if upside > 10 else "3M")
        with col3: st.write("**6M**" if upside > 12 else "6M")
        with col4: 
            if upside > 15: st.success(f"+{upside:.1f}%")
            else: st.write(f"+{upside:.1f}%")

# STOCKS BY PRICE
elif page == "💵 Stocks by Price":
    st.subheader("💵 STOCKS BY PRICE RANGE")
    price_range = st.selectbox("Select Price Range:", ["$100-$200", "$200-$300", "$300-$400", "$400-$500", "$500+"])
    
    if price_range == "$100-$200": min_p, max_p = 100, 200
    elif price_range == "$200-$300": min_p, max_p = 200, 300
    elif price_range == "$300-$400": min_p, max_p = 300, 400
    elif price_range == "$400-$500": min_p, max_p = 400, 500
    else: min_p, max_p = 500, 9999
    
    filtered = [item for item in apply_filters(all_stocks) if min_p <= item[2] < max_p]
    st.write(f"**Stocks between ${min_p} - ${max_p if max_p < 9999 else '500+'}**")
    
    for ticker, name, price, chg, upside, score, vol in filtered:
        st.success(f"**{ticker} - {name}** → ${price:.2f} | +{chg:.1f}%")

# ========== OPTIONS STRATEGIES EXPLORER (NEW) ==========
elif page == "📈 Options Strategies":
    st.subheader("📈 OPTIONS STRATEGIES EXPLORER")
    st.warning("⚠️ Options are high risk. Start with paper trading first!")
    
    strategies = {
        "Long Call": {
            "outlook": "Strongly Bullish",
            "risk": "100% of premium",
            "reward": "Very High (unlimited)",
            "best_for": "Expecting big upside move",
            "complexity": "Low"
        },
        "Bull Call Spread": {
            "outlook": "Moderately Bullish",
            "risk": "Defined & Limited",
            "reward": "Defined & Limited",
            "best_for": "Reducing cost of long call",
            "complexity": "Medium"
        },
        "Covered Call": {
            "outlook": "Mildly Bullish / Neutral",
            "risk": "Stock ownership risk",
            "reward": "Limited (premium + stock gain)",
            "best_for": "Generating income on stocks you own",
            "complexity": "Medium"
        },
        "Iron Condor": {
            "outlook": "Neutral (Range-bound)",
            "risk": "Defined & Limited",
            "reward": "Limited but high probability",
            "best_for": "Low volatility expected",
            "complexity": "High"
        },
        "Protective Put": {
            "outlook": "Bullish but want protection",
            "risk": "Cost of put (insurance)",
            "reward": "Stock upside + downside protection",
            "best_for": "Hedging long stock positions",
            "complexity": "Low"
        }
    }
    
    for name, details in strategies.items():
        with st.expander(f"📌 {name}"):
            st.write(f"**Market Outlook:** {details['outlook']}")
            st.write(f"**Max Risk:** {details['risk']}")
            st.write(f"**Max Reward:** {details['reward']}")
            st.write(f"**Best For:** {details['best_for']}")
            st.write(f"**Complexity:** {details['complexity']}")

# ========== PAPER TRADING SIMULATOR (NEW) ==========
elif page == "📝 Paper Trading":
    st.subheader("📝 PAPER TRADING SIMULATOR")
    st.info("Practice trading with **virtual money** ($10,000 starting capital)")
    
    # Initialize session state for paper trading
    if 'portfolio' not in st.session_state:
        st.session_state.portfolio = {
            'cash': 10000.0,
            'positions': {},
            'trades': []
        }
    
    port = st.session_state.portfolio
    
    # Portfolio Summary
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Cash Balance", f"${port['cash']:.2f}")
    with col2:
        total_value = port['cash']
        for t, pos in port['positions'].items():
            total_value += pos['shares'] * get_data(t)['price']
        st.metric("Total Portfolio Value", f"${total_value:.2f}")
    with col3:
        st.metric("Open Positions", len(port['positions']))
    
    st.markdown("---")
    
    # Trade Form
    st.subheader("Place a Paper Trade")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        trade_ticker = st.selectbox("Select Stock", all_stocks)
    with col2:
        action = st.selectbox("Action", ["BUY", "SELL"])
    with col3:
        shares = st.number_input("Number of Shares", min_value=1, value=10)
    
    current_price = get_data(trade_ticker)['price']
    trade_value = shares * current_price
    
    if st.button("Execute Paper Trade"):
        if action == "BUY":
            if port['cash'] >= trade_value:
                port['cash'] -= trade_value
                if trade_ticker in port['positions']:
                    port['positions'][trade_ticker]['shares'] += shares
                    port['positions'][trade_ticker]['avg_price'] = (
                        (port['positions'][trade_ticker]['avg_price'] * (port['positions'][trade_ticker]['shares'] - shares) + current_price * shares) / 
                        port['positions'][trade_ticker]['shares']
                    )
                else:
                    port['positions'][trade_ticker] = {'shares': shares, 'avg_price': current_price}
                port['trades'].append(f"BUY {shares} {trade_ticker} @ ${current_price:.2f}")
                st.success(f"✅ Bought {shares} shares of {trade_ticker}")
            else:
                st.error("❌ Not enough cash!")
        else:  # SELL
            if trade_ticker in port['positions'] and port['positions'][trade_ticker]['shares'] >= shares:
                port['cash'] += trade_value
                port['positions'][trade_ticker]['shares'] -= shares
                if port['positions'][trade_ticker]['shares'] == 0:
                    del port['positions'][trade_ticker]
                port['trades'].append(f"SELL {shares} {trade_ticker} @ ${current_price:.2f}")
                st.success(f"✅ Sold {shares} shares of {trade_ticker}")
            else:
                st.error("❌ You don't own enough shares!")
    
    st.markdown("---")
    
    # Current Positions
    st.subheader("📋 Current Positions")
    if port['positions']:
        for ticker, pos in port['positions'].items():
            current = get_data(ticker)['price']
            pnl = (current - pos['avg_price']) * pos['shares']
            st.write(f"**{ticker}** — {pos['shares']} shares @ ${pos['avg_price']:.2f} | Current: ${current:.2f} | P&L: ${pnl:.2f}")
    else:
        st.info("No open positions yet.")
    
    # Trade History
    if port['trades']:
        st.subheader("📜 Trade History")
        for trade in port['trades'][-10:]:
            st.write(trade)

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
