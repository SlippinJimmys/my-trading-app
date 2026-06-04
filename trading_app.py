import streamlit as st
import yfinance as yf
from datetime import datetime
import pytz
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="My Trading App", layout="wide")
st.title("🚀 MY TRADING APP")
st.write("**$50–$100 Account** | Smart Signals • Paper Trading • Options Education")

# ==================== STOCK LISTS ====================
penny_stocks = ['XOS', 'SELX', 'HUBC', 'LASE', 'WCT', 'STAK', 'SBEV', 'DBGI', 'FNGR']
big_stocks = ['NVDA', 'AAPL', 'MSFT', 'AMZN', 'GOOGL', 'TSLA', 'META', 'AVGO', 'COST', 'NFLX', 'ADBE', 'CRM', 'AMD', 'INTC', 'QCOM', 'TXN', 'MU', 'AMAT', 'LRCX', 'KLAC', 'PANW', 'CRWD']
upcoming_stocks = ['PLTR', 'ARM', 'SMCI', 'SNOW', 'DDOG', 'NET', 'MDB', 'ZS', 'OKTA', 'RBLX', 'COIN', 'HOOD', 'SOFI', 'RDDT', 'APP']
all_stocks = list(set(penny_stocks + big_stocks + upcoming_stocks))

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

# ==================== DASHBOARD (Improved) ====================
if page == "🏠 Dashboard":
    st.subheader("📊 Dashboard Overview")
    st.write(f"**Last Updated:** {current_time}")
    
    # Quick Stats
    col1, col2, col3, col4 = st.columns(4)
    strong_buys = sum(1 for t in penny_stocks if get_data(t)['change'] >= 10)
    
    with col1:
        st.metric("Strong Buys Today", strong_buys)
    with col2:
        st.metric("Max Risk/Trade", f"${max_risk}")
    with col3:
        st.metric("Market Bias", "Bullish")
    with col4:
        st.metric("Active Filters", f"{price_sort} | {potential_sort}")
    
    st.markdown("---")
    
    # How to Use
    with st.expander("📖 How to Use This App"):
        st.write("""
        1. Use the **sidebar** to navigate between sections.
        2. **Global Filters** (in sidebar) affect most tabs automatically.
        3. Use **⭐ Today's Highlights** to see the best opportunities right now.
        4. Practice safely in **📝 Paper Trading** before using real money.
        5. Learn strategies in **📈 Options Strategies**.
        6. Analyze charts in **📊 Charts & Analysis**.
        """)
    
    st.markdown("---")
    
    # Top Movers
    st.subheader("🔥 Top Movers Right Now")
    movers = [(t, get_data(t)['name'], get_data(t)['price'], get_data(t)['change']) 
              for t in penny_stocks if get_data(t)['change'] >= 5]
    movers.sort(key=lambda x: x[3], reverse=True)
    
    if movers:
        for t, name, price, chg in movers[:6]:
            st.success(f"**{t} - {name}** → ${price:.3f} | **+{chg:.1f}%**")
    else:
        st.info("No strong movers at the moment.")

# ==================== TODAY'S HIGHLIGHTS ====================
elif page == "⭐ Today's Highlights":
    st.subheader("⭐ TOP 10 STOCKS WITH BEST POTENTIAL TODAY")
    st.caption("Sorted by strongest momentum + analyst upside")
    filtered = apply_filters(all_stocks)[:10]
    for i, (ticker, name, price, chg, upside, score, vol) in enumerate(filtered, 1):
        st.success(f"**#{i} {ticker} - {name}** → ${price:.3f} | **+{chg:.1f}%** | Upside: {upside:.1f}%")

# ==================== TODAY'S BUYS ====================
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

# OPTIONS STRATEGIES EXPLORER
elif page == "📈 Options Strategies":
    st.subheader("📈 OPTIONS STRATEGIES EXPLORER")
    st.warning("⚠️ High risk. Practice in Paper Trading first!")
    
    strategies = {
        "Long Call": "Strongly Bullish • High risk/reward • Good for big upside moves",
        "Bull Call Spread": "Moderately Bullish • Defined risk & reward • Lower cost than long call",
        "Covered Call": "Mildly Bullish/Neutral • Generate income on stocks you own",
        "Iron Condor": "Neutral (Range-bound) • High probability, limited profit & risk",
        "Protective Put": "Bullish with protection • Like insurance for your stocks"
    }
    
    for name, desc in strategies.items():
        with st.expander(f"📌 {name}"):
            st.write(desc)

# PAPER TRADING SIMULATOR
elif page == "📝 Paper Trading":
    st.subheader("📝 PAPER TRADING SIMULATOR")
    st.info("Practice with **$10,000** virtual money. Safe way to test strategies.")
    
    if 'portfolio' not in st.session_state:
        st.session_state.portfolio = {'cash': 10000.0, 'positions': {}, 'trades': []}
    
    port = st.session_state.portfolio
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Cash", f"${port['cash']:.2f}")
    with col2:
        total = port['cash'] + sum(pos['shares'] * get_data(t)['price'] for t, pos in port['positions'].items())
        st.metric("Portfolio Value", f"${total:.2f}")
    with col3:
        st.metric("Open Positions", len(port['positions']))
    
    st.markdown("---")
    
    # Trade Form
    st.subheader("Place Trade")
    col1, col2, col3 = st.columns(3)
    with col1:
        trade_ticker = st.selectbox("Stock", all_stocks)
    with col2:
        action = st.selectbox("Action", ["BUY", "SELL"])
    with col3:
        shares = st.number_input("Shares", min_value=1, value=10)
    
    current_price = get_data(trade_ticker)['price']
    
    if st.button("Execute Trade"):
        trade_value = shares * current_price
        if action == "BUY":
            if port['cash'] >= trade_value:
                port['cash'] -= trade_value
                if trade_ticker in port['positions']:
                    port['positions'][trade_ticker]['shares'] += shares
                else:
                    port['positions'][trade_ticker] = {'shares': shares, 'avg_price': current_price}
                port['trades'].append(f"BUY {shares} {trade_ticker} @ ${current_price:.2f}")
                st.success("Trade executed!")
            else:
                st.error("Not enough cash!")
        else:
            if trade_ticker in port['positions'] and port['positions'][trade_ticker]['shares'] >= shares:
                port['cash'] += trade_value
                port['positions'][trade_ticker]['shares'] -= shares
                if port['positions'][trade_ticker]['shares'] == 0:
                    del port['positions'][trade_ticker]
                port['trades'].append(f"SELL {shares} {trade_ticker} @ ${current_price:.2f}")
                st.success("Trade executed!")
            else:
                st.error("Not enough shares!")
    
    if st.button("Reset Portfolio"):
        st.session_state.portfolio = {'cash': 10000.0, 'positions': {}, 'trades': []}
        st.success("Portfolio reset!")
    
    st.markdown("---")
    
    # Positions
    st.subheader("Current Positions")
    if port['positions']:
        for ticker, pos in port['positions'].items():
            curr = get_data(ticker)['price']
            pnl = (curr - pos['avg_price']) * pos['shares']
            st.write(f"**{ticker}** — {pos['shares']} shares @ ${pos['avg_price']:.2f} | P&L: ${pnl:.2f}")
    else:
        st.info("No open positions.")

# ==================== CHARTS & ANALYSIS ====================
elif page == "📊 Charts & Analysis":
    st.subheader("📊 ADVANCED CHARTS & TECHNICAL ANALYSIS")
    
    selected_stock = st.selectbox("Select a stock to analyze:", all_stocks)
    
    if selected_stock:
        data = get_data(selected_stock)
        st.write(f"**{selected_stock} - {data['name']}** → ${data['price']:.2f} | Change: **{data['change']:.1f}%**")
        
        # Controls
        col1, col2, col3 = st.columns([2, 2, 2])
        
        with col1:
            timeframe = st.selectbox("Timeframe", ["30 Days", "60 Days", "90 Days", "180 Days"], index=2)
        with col2:
            show_ma = st.checkbox("Show Moving Averages", value=True)
        with col3:
            show_bbands = st.checkbox("Show Bollinger Bands", value=True)
        
        days_map = {"30 Days": 30, "60 Days": 60, "90 Days": 90, "180 Days": 180}
        days = days_map[timeframe]
        
        try:
            hist = yf.Ticker(selected_stock).history(period=f"{days}d")
            
            if not hist.empty and len(hist) > 20:
                
                # Calculate indicators
                hist['SMA20'] = hist['Close'].rolling(window=20).mean()
                hist['SMA50'] = hist['Close'].rolling(window=50).mean()
                
                sma20 = hist['Close'].rolling(window=20).mean()
                std20 = hist['Close'].rolling(window=20).std()
                hist['UpperBand'] = sma20 + (std20 * 2)
                hist['LowerBand'] = sma20 - (std20 * 2)
                
                # RSI Calculation
                delta = hist['Close'].diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                rs = gain / loss
                hist['RSI'] = 100 - (100 / (1 + rs))
                
                # Create subplots (Price + RSI)
                fig = make_subplots(
                    rows=2, cols=1,
                    shared_xaxes=True,
                    vertical_spacing=0.08,
                    row_heights=[0.7, 0.3],
                    subplot_titles=(f"{selected_stock} Price", "RSI (14)")
                )
                
                # Candlestick
                fig.add_trace(go.Candlestick(
                    x=hist.index,
                    open=hist['Open'],
                    high=hist['High'],
                    low=hist['Low'],
                    close=hist['Close'],
                    name="Price"
                ), row=1, col=1)
                
                # Moving Averages
                if show_ma:
                    fig.add_trace(go.Scatter(
                        x=hist.index, y=hist['SMA20'],
                        line=dict(color='orange', width=1.5),
                        name="SMA 20"
                    ), row=1, col=1)
                    
                    fig.add_trace(go.Scatter(
                        x=hist.index, y=hist['SMA50'],
                        line=dict(color='#00BFFF', width=1.5),
                        name="SMA 50"
                    ), row=1, col=1)
                
                # Bollinger Bands
                if show_bbands:
                    fig.add_trace(go.Scatter(
                        x=hist.index, y=hist['UpperBand'],
                        line=dict(color='gray', width=1, dash='dot'),
                        name="Upper Band"
                    ), row=1, col=1)
                    
                    fig.add_trace(go.Scatter(
                        x=hist.index, y=hist['LowerBand'],
                        line=dict(color='gray', width=1, dash='dot'),
                        name="Lower Band",
                        fill='tonexty',
                        fillcolor='rgba(128,128,128,0.1)'
                    ), row=1, col=1)
                
                # RSI
                fig.add_trace(go.Scatter(
                    x=hist.index, y=hist['RSI'],
                    line=dict(color='purple', width=1.5),
                    name="RSI"
                ), row=2, col=1)
                
                # Overbought / Oversold lines
                fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
                fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)
                
                # Layout
                fig.update_layout(
                    height=650,
                    showlegend=True,
                    xaxis_rangeslider_visible=False,
                    template="plotly_dark",
                    title=f"{selected_stock} - {data['name']} ({timeframe})",
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                )
                
                fig.update_yaxes(title_text="Price ($)", row=1, col=1)
                fig.update_yaxes(title_text="RSI", row=2, col=1, range=[0, 100])
                
                st.plotly_chart(fig, use_container_width=True)
                
                # RSI Interpretation
                latest_rsi = hist['RSI'].iloc[-1]
                if latest_rsi > 70:
                    st.warning(f"**RSI = {latest_rsi:.1f}** → Overbought (possible pullback)")
                elif latest_rsi < 30:
                    st.success(f"**RSI = {latest_rsi:.1f}** → Oversold (possible bounce)")
                else:
                    st.info(f"**RSI = {latest_rsi:.1f}** → Neutral")
                
            else:
                st.warning("Not enough data to calculate indicators.")
                
        except Exception as e:
            st.error(f"Error loading chart: {str(e)}")
