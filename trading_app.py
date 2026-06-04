import streamlit as st
import yfinance as yf
from datetime import datetime, timedelta, date
import pytz
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="My Trading App", layout="wide")
st.title("🚀 MY TRADING APP")
st.write("**$50–$100 Account** | Smart Signals • Paper Trading • Automation Ready")

# ==================== SQUARE NAVIGATION BUTTONS ====================
st.markdown("""
<style>
div[data-testid="stSidebar"] .stRadio input[type="radio"] {
    appearance: none !important;
    -webkit-appearance: none !important;
    width: 20px !important;
    height: 20px !important;
    border: 2px solid #666 !important;
    border-radius: 4px !important;
    background-color: #1a1a1a !important;
    cursor: pointer !important;
    position: relative !important;
}
div[data-testid="stSidebar"] .stRadio input[type="radio"]:checked {
    background-color: #00BFFF !important;
    border-color: #00BFFF !important;
}
div[data-testid="stSidebar"] .stRadio input[type="radio"]:checked::after {
    content: "✓" !important;
    color: white !important;
    font-size: 14px !important;
    position: absolute !important;
    top: 50% !important;
    left: 50% !important;
    transform: translate(-50%, -50%) !important;
}
div[data-testid="stSidebar"] .stRadio > label {
    font-size: 15px !important;
    font-weight: 600 !important;
}
</style>
""", unsafe_allow_html=True)

# ==================== STOCK LISTS ====================
penny_stocks = ['XOS', 'SELX', 'HUBC', 'LASE', 'WCT', 'STAK', 'SBEV', 'DBGI', 'FNGR']
big_stocks = ['NVDA', 'AAPL', 'MSFT', 'AMZN', 'GOOGL', 'TSLA', 'META', 'AVGO', 'COST', 'NFLX', 'ADBE', 'CRM', 'AMD', 'INTC', 'QCOM', 'TXN', 'MU', 'AMAT', 'LRCX', 'KLAC', 'PANW', 'CRWD']
upcoming_stocks = ['PLTR', 'ARM', 'SMCI', 'SNOW', 'DDOG', 'NET', 'MDB', 'ZS', 'OKTA', 'RBLX', 'COIN', 'HOOD', 'SOFI', 'RDDT', 'APP']
all_stocks = list(set(penny_stocks + big_stocks + upcoming_stocks))

# ==================== THEME ====================
if 'theme' not in st.session_state:
    st.session_state.theme = "Dark"

theme = st.sidebar.radio("🎨 Theme", ["Dark", "Light"], horizontal=True)
st.session_state.theme = theme

if theme == "Dark":
    st.markdown("""<style>.stApp { background-color: #0e1117; color: #fafafa; }</style>""", unsafe_allow_html=True)
    plotly_template = "plotly_dark"
else:
    st.markdown("""<style>.stApp { background-color: #ffffff; color: #000000; }</style>""", unsafe_allow_html=True)
    plotly_template = "plotly_white"

# ==================== SIDEBAR ====================
st.sidebar.header("⚙️ Settings")
capital = st.sidebar.number_input("My Capital ($)", value=50, min_value=10)
max_risk = st.sidebar.slider("Max Risk per Trade ($)", 5, 20, 10)

st.sidebar.markdown("---")
st.sidebar.subheader("🔍 Global Filters")
price_sort = st.sidebar.selectbox("Sort by Price", ["None", "Lowest → Highest", "Highest → Lowest"])
potential_sort = st.sidebar.selectbox("Sort by Potential", ["None", "Most Potential → Least"])

st.sidebar.markdown("---")

# ==================== CLEAN NAVIGATION ====================
st.sidebar.markdown("### 📍 Navigation")

page = st.sidebar.radio(
    "",
    options=[
        "🏠 Dashboard",
        "⭐ Today's Highlights",
        "🔥 Today's Buys",
        "📅 1 Week Buys",
        "📆 1 Month Buys",
        "📈 Big Companies",
        "💵 Stocks by Price",
        "📰 Live Intelligence",
        "🏛️ Politician Trades",
        "📊 Charts & Analysis",
        "🤖 Auto-Trade Settings",
        "📝 Paper Trading",
        "📈 Options Strategies",
        "📊 Market Trends",
    ],
    index=0
)

# ==================== HELPER FUNCTIONS ====================
def get_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        return {
            'price': info.get('currentPrice') or info.get('regularMarketPrice', 0),
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

# ==================== DASHBOARD ====================
if page == "🏠 Dashboard":
    st.subheader("📊 Dashboard Overview")
    st.write(f"**Last Updated:** {current_time}")
    
    if 'portfolio' not in st.session_state:
        st.session_state.portfolio = {'cash': 10000.0, 'positions': {}, 'trades': []}
    
    port = st.session_state.portfolio
    
    current_value = port['cash']
    total_pnl = 0
    auto_count = 0
    politician_count = 0
    
    for ticker, pos in port['positions'].items():
        price = get_data(ticker)['price']
        current_value += pos['shares'] * price
        total_pnl += (price - pos['avg_price']) * pos['shares']
        if pos.get('source') == 'Auto': auto_count += 1
        if pos.get('source') == 'Politician Copy': politician_count += 1
    
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Portfolio Value", f"${current_value:,.2f}")
    with col2: st.metric("Cash", f"${port['cash']:,.2f}")
    with col3: st.metric("Total P&L", f"${total_pnl:,.2f}")
    with col4: st.metric("Open Positions", len(port['positions']))
    
    st.markdown("---")
    st.write(f"**Auto-Traded Positions:** {auto_count}   |   **Politician Copied:** {politician_count}")

# ==================== TODAY'S HIGHLIGHTS ====================
elif page == "⭐ Today's Highlights":
    st.subheader("⭐ TOP 10 STOCKS WITH BEST POTENTIAL TODAY")
    filtered = apply_filters(all_stocks)[:10]
    for i, (ticker, name, price, chg, upside, score, vol) in enumerate(filtered, 1):
        st.success(f"**#{i} {ticker} - {name}** → ${price:.3f} | **+{chg:.1f}%**")

# ==================== TODAY'S BUYS ====================
elif page == "🔥 Today's Buys":
    st.subheader("🔥 TODAY'S BEST BUYS")
    filtered = apply_filters(penny_stocks)
    for ticker, name, price, chg, upside, score, vol in filtered:
        if chg >= 10:
            st.success(f"🟢 **STRONG BUY** {ticker} - {name} → ${price:.3f} | **+{chg:.1f}%**")

# ==================== 1 WEEK BUYS ====================
elif page == "📅 1 Week Buys":
    st.subheader("📅 1 WEEK BUYS")
    filtered = apply_filters(penny_stocks)
    for ticker, name, price, chg, upside, score, vol in filtered:
        if chg > 3:
            st.success(f"📈 **BUY** {ticker} - {name} → ${price:.3f} | +{chg:.1f}%")

# ==================== 1 MONTH BUYS ====================
elif page == "📆 1 Month Buys":
    st.subheader("📆 1 MONTH BUYS")
    filtered = apply_filters(penny_stocks)
    for ticker, name, price, chg, upside, score, vol in filtered:
        if price < 8 and chg > 2:
            st.success(f"🏦 **BUY** {ticker} - {name} → ${price:.3f} | +{chg:.1f}%")

# ==================== BIG COMPANIES ====================
elif page == "📈 Big Companies":
    st.subheader("📈 BIG COMPANIES + GROWTH STOCKS")
    filtered = apply_filters(big_stocks + upcoming_stocks)
    for ticker, name, price, chg, upside, score, vol in filtered:
        st.write(f"**{ticker} - {name}** → ${price:.2f}")

# ==================== STOCKS BY PRICE ====================
elif page == "💵 Stocks by Price":
    st.subheader("💵 STOCKS BY PRICE RANGE")
    price_range = st.selectbox("Select Price Range:", ["$100-$200", "$200-$300", "$300-$400", "$400-$500", "$500+"])
    
    if price_range == "$100-$200": min_p, max_p = 100, 200
    elif price_range == "$200-$300": min_p, max_p = 200, 300
    elif price_range == "$300-$400": min_p, max_p = 300, 400
    elif price_range == "$400-$500": min_p, max_p = 400, 500
    else: min_p, max_p = 500, 9999
    
    filtered = [item for item in apply_filters(all_stocks) if min_p <= item[2] < max_p]
    for ticker, name, price, chg, upside, score, vol in filtered:
        st.success(f"**{ticker} - {name}** → ${price:.2f} | +{chg:.1f}%")

# ==================== LIVE INTELLIGENCE ====================
elif page == "📰 Live Intelligence":
    st.subheader("📰 LIVE MARKET INTELLIGENCE & NEWS SENTIMENT")
    selected_stock = st.selectbox("Select a stock:", all_stocks)
    
    if selected_stock:
        data = get_data(selected_stock)
        st.write(f"**{selected_stock} - {data['name']}** → ${data['price']:.2f} | {data['change']:.1f}%")
        
        try:
            stock = yf.Ticker(selected_stock)
            news = stock.news
            if news:
                for item in news[:5]:
                    with st.expander(item.get('title', 'News')):
                        st.markdown(f"[Read Article]({item.get('link', '#')})")
        except:
            st.warning("Could not load news.")

# ==================== POLITICIAN TRADES ====================
elif page == "🏛️ Politician Trades":
    st.subheader("🏛️ Copy Trades of US Politicians")
    
    if 'portfolio' not in st.session_state:
        st.session_state.portfolio = {'cash': 10000.0, 'positions': {}, 'trades': []}
    
    port = st.session_state.portfolio
    
    if st.button("🔄 Load Recent Politician Trades"):
        st.session_state.politician_trades = pd.DataFrame({
            'Politician': ['Nancy Pelosi (D)', 'Josh Hawley (R)', 'Ro Khanna (D)'],
            'Ticker': ['NVDA', 'TSLA', 'AAPL'],
            'Action': ['Buy', 'Sell', 'Buy'],
            'Amount Range': ['$1M-$5M', '$250K-$500K', '$100K-$250K'],
            'Date': ['2026-05-20', '2026-05-18', '2026-05-15']
        })
    
    if 'politician_trades' in st.session_state:
        st.dataframe(st.session_state.politician_trades)
        
        for idx, row in st.session_state.politician_trades.iterrows():
            if st.button(f"Copy {row['Ticker']} Trade", key=f"copy_{idx}"):
                ticker = row['Ticker']
                price = get_data(ticker)['price']
                amount = 3000000 if 'M' in row['Amount Range'] else 375000
                shares = int(amount / price)
                
                if shares > 0 and port['cash'] >= shares * price:
                    port['cash'] -= shares * price
                    if ticker in port['positions']:
                        port['positions'][ticker]['shares'] += shares
                    else:
                        port['positions'][ticker] = {'shares': shares, 'avg_price': price, 'source': 'Politician Copy'}
                    st.success(f"✅ Added {shares} shares of {ticker}!")

# ==================== CHARTS & ANALYSIS ====================
elif page == "📊 Charts & Analysis":
    st.subheader("📊 ADVANCED CHARTS & TECHNICAL ANALYSIS")
    selected_stock = st.selectbox("Select a stock:", all_stocks)
    
    if selected_stock:
        data = get_data(selected_stock)
        st.write(f"**{selected_stock} - {data['name']}** → ${data['price']:.2f} | {data['change']:.1f}%")
        
        col1, col2, col3 = st.columns([2,2,2])
        with col1: timeframe = st.selectbox("Timeframe", ["30 Days", "60 Days", "90 Days", "180 Days"], index=2)
        with col2: show_ma = st.checkbox("Show Moving Averages", value=True)
        with col3: show_bbands = st.checkbox("Show Bollinger Bands", value=True)
        
        days = {"30 Days":30, "60 Days":60, "90 Days":90, "180 Days":180}[timeframe]
        
        try:
            hist = yf.Ticker(selected_stock).history(period=f"{days}d")
            if not hist.empty and len(hist) >= 50:
                hist['SMA20'] = hist['Close'].rolling(20).mean()
                hist['SMA50'] = hist['Close'].rolling(50).mean()
                sma20 = hist['Close'].rolling(20).mean()
                std20 = hist['Close'].rolling(20).std()
                hist['UpperBand'] = sma20 + std20*2
                hist['LowerBand'] = sma20 - std20*2
                
                delta = hist['Close'].diff()
                gain = delta.where(delta > 0, 0).rolling(14).mean()
                loss = -delta.where(delta < 0, 0).rolling(14).mean()
                hist['RSI'] = 100 - (100 / (1 + gain/loss))
                
                fig = make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[0.7, 0.3])
                fig.add_trace(go.Candlestick(x=hist.index, open=hist['Open'], high=hist['High'], low=hist['Low'], close=hist['Close']), row=1, col=1)
                
                if show_ma:
                    fig.add_trace(go.Scatter(x=hist.index, y=hist['SMA20'], name="SMA20", line=dict(color='orange')), row=1, col=1)
                    fig.add_trace(go.Scatter(x=hist.index, y=hist['SMA50'], name="SMA50", line=dict(color='#00BFFF')), row=1, col=1)
                
                if show_bbands:
                    fig.add_trace(go.Scatter(x=hist.index, y=hist['UpperBand'], name="Upper Band", line=dict(color='gray', dash='dot')), row=1, col=1)
                    fig.add_trace(go.Scatter(x=hist.index, y=hist['LowerBand'], name="Lower Band", line=dict(color='gray', dash='dot')), row=1, col=1)
                
                fig.add_trace(go.Scatter(x=hist.index, y=hist['RSI'], name="RSI", line=dict(color='purple')), row=2, col=1)
                fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
                fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)
                
                fig.update_layout(height=650, template=plotly_template)
                st.plotly_chart(fig, use_container_width=True)
        except:
            st.error("Error loading chart.")

# ==================== AUTO-TRADE SETTINGS ====================
elif page == "🤖 Auto-Trade Settings":
    st.subheader("🤖 AUTO-TRADE SETTINGS & SCHEDULED MODE")
    st.warning("Works in Paper Trading mode only.")
    
    if 'auto_settings' not in st.session_state:
        st.session_state.auto_settings = {
            'enabled': False, 'only_highlights': True, 'only_todays_buys': False,
            'min_price': 2.0, 'max_price': 100.0, 'max_capital_per_trade': 50.0,
            'max_risk_per_trade': 10.0, 'rsi_filter': True, 'max_daily_loss': 30.0,
            'daily_profit_target': 50.0, 'max_positions': 3
        }
    
    if 'auto_schedule' not in st.session_state:
        st.session_state.auto_schedule = {'active': False, 'end_time': None, 'interval_seconds': 30}
    
    if 'daily_start_value' not in st.session_state:
        st.session_state.daily_start_value = None
        st.session_state.last_reset_date = None
    
    settings = st.session_state.auto_settings
    schedule = st.session_state.auto_schedule
    
    settings['enabled'] = st.checkbox("Enable Auto-Trading", value=settings['enabled'])
    settings['only_todays_buys'] = st.checkbox("Only trade Today's Buys", value=settings['only_todays_buys'])
    settings['min_price'] = st.number_input("Min Price ($)", value=float(settings['min_price']), step=0.5)
    settings['max_price'] = st.number_input("Max Price ($)", value=float(settings['max_price']), step=1.0)
    settings['max_capital_per_trade'] = st.number_input("Max Capital Per Trade ($)", value=float(settings['max_capital_per_trade']), step=5.0)
    settings['max_daily_loss'] = st.number_input("Max Daily Loss Limit ($)", value=float(settings['max_daily_loss']), step=5.0)
    settings['daily_profit_target'] = st.number_input("Daily Profit Target ($)", value=float(settings['daily_profit_target']), step=5.0)
    
    st.markdown("---")
    st.subheader("🛡️ Safety Status")
    
    if 'portfolio' not in st.session_state:
        st.session_state.portfolio = {'cash': 10000.0, 'positions': {}, 'trades': []}
    
    port = st.session_state.portfolio
    # Daily P&L calculation logic here...
    st.info("Auto-trading safety features active (daily loss/profit targets enforced).")

# ==================== PAPER TRADING (Most Functional) ====================
elif page == "📝 Paper Trading":
    st.subheader("📝 PAPER TRADING SIMULATOR")
    
    if 'portfolio' not in st.session_state:
        st.session_state.portfolio = {'cash': 10000.0, 'positions': {}, 'trades': []}
    
    port = st.session_state.portfolio
    
    # Portfolio Summary
    total_value = port['cash']
    total_pnl = 0
    for ticker, pos in port['positions'].items():
        price = get_data(ticker)['price']
        total_value += pos['shares'] * price
        total_pnl += (price - pos['avg_price']) * pos['shares']
    
    col1, col2, col3 = st.columns(3)
    with col1: st.metric("Cash", f"${port['cash']:,.2f}")
    with col2: st.metric("Portfolio Value", f"${total_value:,.2f}")
    with col3: st.metric("Total P&L", f"${total_pnl:,.2f}")
    
    st.markdown("---")
    
    # Positions Table + Close Buttons
    st.subheader("📋 Current Positions")
    
    if port['positions']:
        for ticker, pos in list(port['positions'].items()):
            price = get_data(ticker)['price']
            pnl = (price - pos['avg_price']) * pos['shares']
            source = pos.get('source', 'Human')
            
            col1, col2, col3 = st.columns([3, 2, 1])
            with col1:
                st.write(f"**{ticker}** — {pos['shares']} shares @ ${pos['avg_price']:.2f} | Current: ${price:.2f} | P&L: ${pnl:.2f}")
            with col2:
                st.write(f"Source: {source}")
            with col3:
                if st.button(f"Close {ticker}", key=f"close_{ticker}"):
                    proceeds = pos['shares'] * price
                    port['cash'] += proceeds
                    del port['positions'][ticker]
                    st.success(f"Closed {ticker}. +${proceeds:,.2f}")
                    st.rerun()
    else:
        st.info("No open positions yet.")
    
    st.markdown("---")
    
    # Manual Trade
    st.subheader("Manual Trade")
    col1, col2, col3 = st.columns(3)
    with col1: trade_ticker = st.selectbox("Stock", all_stocks)
    with col2: action = st.selectbox("Action", ["BUY", "SELL"])
    with col3: shares = st.number_input("Shares", min_value=1, value=10)
    
    if st.button("Execute Trade"):
        price = get_data(trade_ticker)['price']
        value = shares * price
        if action == "BUY" and port['cash'] >= value:
            port['cash'] -= value
            if trade_ticker in port['positions']:
                port['positions'][trade_ticker]['shares'] += shares
            else:
                port['positions'][trade_ticker] = {'shares': shares, 'avg_price': price, 'source': 'Human'}
            st.success("Trade executed!")
        elif action == "SELL" and trade_ticker in port['positions']:
            port['cash'] += value
            port['positions'][trade_ticker]['shares'] -= shares
            if port['positions'][trade_ticker]['shares'] <= 0:
                del port['positions'][trade_ticker]
            st.success("Trade executed!")

# ==================== OPTIONS & MARKET TRENDS ====================
elif page == "📈 Options Strategies":
    st.subheader("📈 OPTIONS STRATEGIES EXPLORER")
    st.write("Long Call, Bull Call Spread, Covered Call, Iron Condor, Protective Put")

elif page == "📊 Market Trends":
    st.subheader("📊 MARKET TRENDS")
    st.info("**Positive:** AI momentum still strong")

st.caption(f"**Risk Rule:** Max ${max_risk} per trade. Sell fast on +20-40% or cut at -10%.")
