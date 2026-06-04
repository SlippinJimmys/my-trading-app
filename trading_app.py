import streamlit as st
import yfinance as yf
from datetime import datetime
import pytz
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="My Trading App", layout="wide")
st.title("🚀 MY TRADING APP")
st.write("**$50–$100 Account** | Smart Signals • Paper Trading • Automation Ready")

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
        "📰 Live Intelligence",
        "🤖 Auto-Trade Settings",
        "📈 Options Strategies",
        "📝 Paper Trading",
        "📊 Charts & Analysis",
        "📊 Market Trends"
    ],
    horizontal=False
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
    
    col1, col2, col3, col4 = st.columns(4)
    strong_buys = sum(1 for t in penny_stocks if get_data(t)['change'] >= 10)
    
    with col1: st.metric("Strong Buys Today", strong_buys)
    with col2: st.metric("Max Risk/Trade", f"${max_risk}")
    with col3: st.metric("Market Bias", "Bullish")
    with col4: st.metric("Active Filters", f"{price_sort} | {potential_sort}")
    
    with st.expander("📖 How to Use This App"):
        st.write("""
        1. Use **sidebar** to navigate
        2. Check **📰 Live Intelligence** before trading
        3. Set your rules in **🤖 Auto-Trade Settings**
        4. Practice in **📝 Paper Trading**
        5. Analyze in **📊 Charts & Analysis**
        """)

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
    st.subheader("📈 BIG COMPANIES + GROWTH STOCKS")
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
                st.subheader("📰 Recent News + Sentiment")
                positive_count = negative_count = neutral_count = 0
                
                positive_words = ['beat', 'surge', 'gain', 'rise', 'strong', 'growth', 'upgrade', 'bullish', 'profit', 'rally']
                negative_words = ['miss', 'drop', 'fall', 'weak', 'loss', 'downgrade', 'bearish', 'decline', 'warning']
                
                for item in news[:6]:
                    title = item.get('title', '')
                    title_lower = title.lower()
                    pos = sum(1 for w in positive_words if w in title_lower)
                    neg = sum(1 for w in negative_words if w in title_lower)
                    
                    if pos > neg:
                        sentiment = "🟢 Positive"
                        positive_count += 1
                    elif neg > pos:
                        sentiment = "🔴 Negative"
                        negative_count += 1
                    else:
                        sentiment = "🟡 Neutral"
                        neutral_count += 1
                    
                    with st.expander(f"{sentiment} | {title}"):
                        st.markdown(f"[Read Article]({item.get('link', '#')})")
                
                st.markdown("---")
                st.subheader("📊 Overall Sentiment")
                total = positive_count + negative_count + neutral_count
                if total > 0:
                    if positive_count > negative_count:
                        st.success("🟢 Overall: Bullish sentiment in recent news")
                    elif negative_count > positive_count:
                        st.error("🔴 Overall: Bearish sentiment in recent news")
                    else:
                        st.info("🟡 Overall: Neutral / Mixed sentiment")
        except:
            st.warning("Could not load news right now.")

# ==================== AUTO-TRADE SETTINGS (NEW) ====================
elif page == "🤖 Auto-Trade Settings":
    st.subheader("🤖 AUTO-TRADE SETTINGS")
    st.warning("⚠️ This is for **Paper Trading** only right now. Real automation coming soon.")
    
    if 'auto_settings' not in st.session_state:
        st.session_state.auto_settings = {
            'enabled': False,
            'only_highlights': True,
            'min_price': 2.0,
            'max_risk_per_trade': 10,
            'rsi_filter': True,
            'max_daily_loss': 30,
            'max_positions': 3
        }
    
    settings = st.session_state.auto_settings
    
    settings['enabled'] = st.checkbox("Enable Auto-Trading (Paper Only)", value=settings['enabled'])
    settings['only_highlights'] = st.checkbox("Only trade stocks from Today's Highlights", value=settings['only_highlights'])
    settings['min_price'] = st.number_input("Minimum Stock Price ($)", value=settings['min_price'], step=0.5)
    settings['max_risk_per_trade'] = st.number_input("Max Risk Per Trade ($)", value=settings['max_risk_per_trade'])
    settings['rsi_filter'] = st.checkbox("Only buy if RSI < 35 (Oversold)", value=settings['rsi_filter'])
    settings['max_daily_loss'] = st.number_input("Max Daily Loss Limit ($)", value=settings['max_daily_loss'])
    settings['max_positions'] = st.number_input("Maximum Open Positions", value=settings['max_positions'], step=1)
    
    st.markdown("---")
    st.subheader("Current Auto-Trade Rules Summary")
    st.write(f"""
    - Auto Trading: **{'Enabled' if settings['enabled'] else 'Disabled'}**
    - Only trade Highlights: **{settings['only_highlights']}**
    - Min Price: **${settings['min_price']}**
    - Max Risk per Trade: **${settings['max_risk_per_trade']}**
    - RSI Filter: **{settings['rsi_filter']}**
    - Max Daily Loss: **${settings['max_daily_loss']}**
    - Max Positions: **{settings['max_positions']}**
    """)
    
    st.info("💡 These settings will be used when we connect to Alpaca paper trading in the future.")

# OPTIONS STRATEGIES
elif page == "📈 Options Strategies":
    st.subheader("📈 OPTIONS STRATEGIES EXPLORER")
    st.warning("High risk. Practice in Paper Trading first.")
    
    strategies = {
        "Long Call": "Strongly Bullish • High risk/reward",
        "Bull Call Spread": "Moderately Bullish • Defined risk",
        "Covered Call": "Mildly Bullish • Generate income",
        "Iron Condor": "Neutral • High probability",
        "Protective Put": "Bullish with protection"
    }
    for name, desc in strategies.items():
        with st.expander(f"📌 {name}"):
            st.write(desc)

# PAPER TRADING
elif page == "📝 Paper Trading":
    st.subheader("📝 PAPER TRADING SIMULATOR")
    st.info("Practice with $10,000 virtual money.")
    
    if 'portfolio' not in st.session_state:
        st.session_state.portfolio = {'cash': 10000.0, 'positions': {}, 'trades': []}
    
    port = st.session_state.portfolio
    
    col1, col2, col3 = st.columns(3)
    with col1: st.metric("Cash", f"${port['cash']:.2f}")
    with col2: 
        total = port['cash'] + sum(p['shares'] * get_data(t)['price'] for t, p in port['positions'].items())
        st.metric("Portfolio Value", f"${total:.2f}")
    with col3: st.metric("Positions", len(port['positions']))
    
    st.markdown("---")
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
                port['positions'][trade_ticker] = {'shares': shares, 'avg_price': price}
            st.success("Trade executed!")
        elif action == "SELL" and trade_ticker in port['positions'] and port['positions'][trade_ticker]['shares'] >= shares:
            port['cash'] += value
            port['positions'][trade_ticker]['shares'] -= shares
            if port['positions'][trade_ticker]['shares'] == 0:
                del port['positions'][trade_ticker]
            st.success("Trade executed!")
        else:
            st.error("Invalid trade!")
    
    if st.button("Reset Portfolio"):
        st.session_state.portfolio = {'cash': 10000.0, 'positions': {}, 'trades': []}
        st.success("Portfolio reset!")

# CHARTS & ANALYSIS
elif page == "📊 Charts & Analysis":
    st.subheader("📊 ADVANCED CHARTS & TECHNICAL ANALYSIS")
    selected_stock = st.selectbox("Select a stock:", all_stocks)
    
    if selected_stock:
        data = get_data(selected_stock)
        st.write(f"**{selected_stock} - {data['name']}** → ${data['price']:.2f} | {data['change']:.1f}%")
        
        col1, col2, col3 = st.columns([2, 2, 2])
        with col1: timeframe = st.selectbox("Timeframe", ["30 Days", "60 Days", "90 Days", "180 Days"], index=2)
        with col2: show_ma = st.checkbox("Show Moving Averages", value=True)
        with col3: show_bbands = st.checkbox("Show Bollinger Bands", value=True)
        
        days = {"30 Days": 30, "60 Days": 60, "90 Days": 90, "180 Days": 180}[timeframe]
        
        try:
            hist = yf.Ticker(selected_stock).history(period=f"{days}d")
            if hist.empty or len(hist) < 50:
                st.warning("Not enough data.")
            else:
                hist['SMA20'] = hist['Close'].rolling(20).mean()
                hist['SMA50'] = hist['Close'].rolling(50).mean()
                sma20 = hist['Close'].rolling(20).mean()
                std20 = hist['Close'].rolling(20).std()
                hist['UpperBand'] = sma20 + std20 * 2
                hist['LowerBand'] = sma20 - std20 * 2
                
                delta = hist['Close'].diff()
                gain = delta.where(delta > 0, 0).rolling(14).mean()
                loss = -delta.where(delta < 0, 0).rolling(14).mean()
                hist['RSI'] = 100 - (100 / (1 + gain / loss))
                
                fig = make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[0.7, 0.3])
                fig.add_trace(go.Candlestick(x=hist.index, open=hist['Open'], high=hist['High'], low=hist['Low'], close=hist['Close']), row=1, col=1)
                
                if show_ma:
                    fig.add_trace(go.Scatter(x=hist.index, y=hist['SMA20'], name="SMA 20", line=dict(color='orange')), row=1, col=1)
                    fig.add_trace(go.Scatter(x=hist.index, y=hist['SMA50'], name="SMA 50", line=dict(color='#00BFFF')), row=1, col=1)
                
                if show_bbands:
                    fig.add_trace(go.Scatter(x=hist.index, y=hist['UpperBand'], name="Upper Band", line=dict(color='gray', dash='dot')), row=1, col=1)
                    fig.add_trace(go.Scatter(x=hist.index, y=hist['LowerBand'], name="Lower Band", line=dict(color='gray', dash='dot')), row=1, col=1)
                
                fig.add_trace(go.Scatter(x=hist.index, y=hist['RSI'], name="RSI", line=dict(color='purple')), row=2, col=1)
                fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
                fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)
                
                fig.update_layout(height=650, template=plotly_template, title=f"{selected_stock} ({timeframe})")
                st.plotly_chart(fig, use_container_width=True)
                
                rsi = hist['RSI'].iloc[-1]
                if rsi > 70: st.warning(f"RSI = {rsi:.1f} → Overbought")
                elif rsi < 30: st.success(f"RSI = {rsi:.1f} → Oversold")
                else: st.info(f"RSI = {rsi:.1f} → Neutral")
        except:
            st.error("Error loading chart.")

# MARKET TRENDS
elif page == "📊 Market Trends":
    st.subheader("📊 MARKET TRENDS")
    st.info("**Positive:** AI momentum still strong")
    st.warning("**Risks:** High valuations + inflation pressure")
    st.write("**Overall:** Good for momentum plays. Be selective.")

st.caption(f"**Risk Rule:** Max ${max_risk} per trade. Sell fast on +20-40% or cut at -10%.")
