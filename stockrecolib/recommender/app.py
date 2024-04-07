import streamlit as st
import random
from sklearn.impute import SimpleImputer
import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.neighbors import NearestNeighbors
import plotly.graph_objs as go
import streamlit as st
from sklearn.impute import SimpleImputer
import yfinance as yf
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.neighbors import NearestNeighbors
import plotly.graph_objs as go
import datetime

stock_categories = {
    'AAPL': {'market': 'Technology', 'segment': 'Hardware & Software'},
    'MSFT': {'market': 'Technology', 'segment': 'Hardware & Software'},
    'GOOGL': {'market': 'Technology', 'segment': 'Internet & AI'},
    'AMZN': {'market': 'E-Commerce & Cloud', 'segment': 'Retail & Cloud Services'},
    'FB': {'market': 'Technology', 'segment': 'Social Media & Advertising'},
    'TSLA': {'market': 'Automobile', 'segment': 'Electric Vehicles & Manufacturing'},
    'GM': {'market': 'Automobile', 'segment': 'Electric Vehicles & Manufacturing'},
    'F': {'market': 'Automobile', 'segment': 'Electric Vehicles & Manufacturing'},
    'NVDA': {'market': 'Technology', 'segment': 'Semiconductors & AI'},
    'AMD': {'market': 'Technology', 'segment': 'Semiconductors & AI'},
    'INTC': {'market': 'Technology', 'segment': 'Semiconductors & AI'},
    'NFLX': {'market': 'Entertainment', 'segment': 'Streaming Media'},
    'DIS': {'market': 'Entertainment', 'segment': 'Media & Entertainment'},
    'PFE': {'market': 'Healthcare', 'segment': 'Pharmaceuticals & Biotech'},
    'MRNA': {'market': 'Healthcare', 'segment': 'Pharmaceuticals & Biotech'},
    'JNJ': {'market': 'Healthcare', 'segment': 'Pharmaceuticals & Biotech'},
    'XOM': {'market': 'Energy', 'segment': 'Oil, Gas & Renewable Energy'},
    'CVX': {'market': 'Energy', 'segment': 'Oil, Gas & Renewable Energy'},
    'COP': {'market': 'Energy', 'segment': 'Oil, Gas & Renewable Energy'},
    'BAC': {'market': 'Financial Services', 'segment': 'Banking & Investment'},
    'JPM': {'market': 'Financial Services', 'segment': 'Banking & Investment'},
    'GS': {'market': 'Financial Services', 'segment': 'Banking & Investment'},
    'WMT': {'market': 'Retail', 'segment': 'Retail & Wholesale'},
    'COST': {'market': 'Retail', 'segment': 'Retail & Wholesale'},
    'TGT': {'market': 'Retail', 'segment': 'Retail & Wholesale'},
    'PG': {'market': 'Consumer Goods', 'segment': 'Consumer Products & Services'},
    'KO': {'market': 'Beverages', 'segment': 'Soft Drinks & Snacks'},
    'PEP': {'market': 'Beverages', 'segment': 'Soft Drinks & Snacks'},
    'ORCL': {'market': 'Technology', 'segment': 'Enterprise Software & Cloud'},
    'CRM': {'market': 'Technology', 'segment': 'Enterprise Software & Cloud'},
    'ADBE': {'market': 'Technology', 'segment': 'Enterprise Software & Cloud'},
    'V': {'market': 'Financial Services', 'segment': 'Payment Processing & Financial Tech'},
    'MA': {'market': 'Financial Services', 'segment': 'Payment Processing & Financial Tech'},
    'PYPL': {'market': 'Financial Services', 'segment': 'Payment Processing & Financial Tech'},
    'UNH': {'market': 'Healthcare', 'segment': 'Healthcare Providers & Services'},
    'ABBV': {'market': 'Healthcare', 'segment': 'Pharmaceuticals & Biotech'},
    'TMO': {'market': 'Healthcare', 'segment': 'Life Sciences & Health Tech'},
    'LLY': {'market': 'Healthcare', 'segment': 'Pharmaceuticals & Biotech'},
    'VZ': {'market': 'Telecommunications', 'segment': 'Wireless & Broadband Services'},
    'T': {'market': 'Telecommunications', 'segment': 'Wireless & Broadband Services'},
    'NKE': {'market': 'Apparel', 'segment': 'Footwear & Sportswear'},
    'LULU': {'market': 'Apparel', 'segment': 'Athletic Apparel & Accessories'},
    'SBUX': {'market': 'Restaurants', 'segment': 'Coffee Shops & Quick Service'},
    'MCD': {'market': 'Restaurants', 'segment': 'Fast Food & Quick Service'},
    'BA': {'market': 'Aerospace', 'segment': 'Aerospace & Defense'},
    'RTX': {'market': 'Aerospace', 'segment': 'Aerospace & Defense'},
    'LMT': {'market': 'Aerospace', 'segment': 'Aerospace & Defense'},
    'SPG': {'market': 'Real Estate', 'segment': 'Commercial Real Estate & REITs'},
    'O': {'market': 'Real Estate', 'segment': 'Commercial Real Estate & REITs'},
    'DLR': {'market': 'Real Estate', 'segment': 'Data Centers & Technology REITs'},
    'ENPH': {'market': 'Technology', 'segment': 'Renewable Energy Tech & Equipment'},
    'NEE': {'market': 'Utilities', 'segment': 'Electric & Renewable Energy'},
    'DUK': {'market': 'Utilities', 'segment': 'Electric & Renewable Energy'},
    'SO': {'market': 'Utilities', 'segment': 'Electric & Renewable Energy'},
    'SQ': {'market': 'Financial Services', 'segment': 'Payment Processing & Financial Tech'},
    'SHOP': {'market': 'E-Commerce & Cloud', 'segment': 'E-Commerce Platforms & Services'},
    'TWTR': {'market': 'Technology', 'segment': 'Social Media & Advertising'},
    'SNAP': {'market': 'Technology', 'segment': 'Social Media & Advertising'},
    'SPOT': {'market': 'Entertainment', 'segment': 'Streaming Media & Online Content'},
    'ZM': {'market': 'Technology', 'segment': 'Software & Cloud Services'},
    'DOCU': {'market': 'Technology', 'segment': 'Software & Cloud Services'},
    'ADSK': {'market': 'Technology', 'segment': 'Software & Cloud Services'},
    'INTU': {'market': 'Technology', 'segment': 'Software & Cloud Services'},
    'ASML': {'market': 'Technology', 'segment': 'Semiconductor Equipment & Services'},
    'TXN': {'market': 'Technology', 'segment': 'Semiconductors & Electronic Components'},
    'QCOM': {'market': 'Technology', 'segment': 'Semiconductors & Electronic Components'},
    'AVGO': {'market': 'Technology', 'segment': 'Semiconductors & Electronic Components'},
    'MU': {'market': 'Technology', 'segment': 'Semiconductors & Electronic Components'},
    'TSM': {'market': 'Technology', 'segment': 'Semiconductors & Electronic Components'},
    'AMAT': {'market': 'Technology', 'segment': 'Semiconductor Equipment & Services'},
    'UBER': {'market': 'Technology', 'segment': 'Ride-Hailing & Mobility Services'},
    'LYFT': {'market': 'Technology', 'segment': 'Ride-Hailing & Mobility Services'},
    'PLTR': {'market': 'Technology', 'segment': 'Software & Data Analytics'},
    'CSCO': {'market': 'Technology', 'segment': 'Networking Equipment & Services'},
    'IBM': {'market': 'Technology', 'segment': 'Enterprise Software & Hardware'},
    'HPQ': {'market': 'Technology', 'segment': 'Computer Hardware & Equipment'},
    'DELL': {'market': 'Technology', 'segment': 'Computer Hardware & Equipment'},
    'VMW': {'market': 'Technology', 'segment': 'Cloud Computing & Virtualization'},
    'SAP': {'market': 'Technology', 'segment': 'Enterprise Software & Solutions'},
    'HPE': {'market': 'Technology', 'segment': 'Enterprise Solutions & Services'},
    'CTSH': {'market': 'Technology', 'segment': 'IT Services & Consulting'},
    'WDAY': {'market': 'Technology', 'segment': 'Enterprise Software & Cloud Services'},
    'NOW': {'market': 'Technology', 'segment': 'Enterprise Software & Cloud Services'},
    'TEAM': {'market': 'Technology', 'segment': 'Software & Collaboration Solutions'},
    'ADP': {'market': 'Technology', 'segment': 'Software & HR Tech'},
    'RHT': {'market': 'Technology', 'segment': 'Enterprise Software & Solutions'},
    'NTAP': {'market': 'Technology', 'segment': 'Data Storage & Management'},
}

# Function to fetch and display the latest stock price
def display_latest_price(ticker_symbol, placeholder):
    if ticker_symbol:
        stock = yf.Ticker(ticker_symbol)
        hist = stock.history(period="1d")
        if not hist.empty:
            latest_price = hist['Close'].iloc[-1]
            placeholder.metric(label=f"Latest Price: {ticker_symbol}", value=f"${latest_price:.2f}")
        else:
            placeholder.error("Could not retrieve data.")

# Adding a button to start fetching real-time data
if st.button('Fetch Real-time Data'):
    st.session_state.fetch_real_time_data = True

# Creating a placeholder outside the conditional check to ensure it exists
real_time_data_placeholder = st.empty()

# Query ticker input with unique key for real-time data
real_time_data_input = st.text_input('Enter stock ticker for real-time data (e.g., AAPL):', key='realTimeTicker').upper()

# Triggering the real-time data fetch based on a session state variable
if 'fetch_real_time_data' in st.session_state and st.session_state.fetch_real_time_data:
    # Call the function to display the latest stock price
    display_latest_price(real_time_data_input, real_time_data_placeholder)

# Displaying the next scheduled update time
if 'next_update_time' in st.session_state:
    st.write(f"Next update scheduled at: {st.session_state.next_update_time}")


# Displaying the next scheduled update time
if 'next_update_time' in st.session_state:
    st.write(f"Next update scheduled at: {st.session_state.next_update_time}")

# Function to recommend stocks based on market and segment
def recommend_by_market_segment(ticker, n=3):
    if ticker not in stock_categories:
        return ["Ticker not found in categories."]
    
    ticker_info = stock_categories[ticker]
    ticker_market = ticker_info['market']
    ticker_segment = ticker_info['segment']
    
    recommendations = [
        stock for stock, info in stock_categories.items()
        if info['market'] == ticker_market and info['segment'] == ticker_segment and stock != ticker
    ]
    
    return recommendations[:n]

# Function to fetch financial data
def fetch_financial_data(tickers):
    data = {}
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        market_cap = stock.info.get('marketCap', np.nan)
        pe_ratio = stock.info.get('trailingPE', np.nan)
        data[ticker] = [market_cap, pe_ratio]
    return pd.DataFrame.from_dict(data, orient='index', columns=['Market Cap', 'P/E Ratio'])

# Preparing data for recommendation based on financial metrics
tickers = list(stock_categories.keys())
df = fetch_financial_data(tickers)
imputer = SimpleImputer(strategy='mean')
df_imputed = imputer.fit_transform(df)
scaler = MinMaxScaler()
df_scaled = scaler.fit_transform(df_imputed)
neighbors = NearestNeighbors(n_neighbors=len(tickers))
neighbors.fit(df_scaled)

# Recommendation based on financial metrics
def recommend_stocks(ticker, recommendations_to_exclude=[], n=3):
    if ticker not in df.index:
        return ["Ticker not found."]
    
    recommendations_to_exclude.append(ticker)
    query_index = df.index.get_loc(ticker)
    distances, indices = neighbors.kneighbors([df_scaled[query_index]])
    
    recommended_tickers = [df.index[i] for i in indices[0] if df.index[i] not in recommendations_to_exclude][:n]
    return recommended_tickers

# Streamlit app interface
st.title('Stock Recommender with Dual Categories')

# Plot stock performance using Plotly
def plot_stock_performance(ticker):
    data = yf.download(ticker, period="1y")
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=data.index,
                                 open=data['Open'],
                                 high=data['High'],
                                 low=data['Low'],
                                 close=data['Close'], name='market data'))
    fig.update_layout(title=f'Stock Performance for {ticker}', xaxis_rangeslider_visible=False)
    st.plotly_chart(fig)

# Initialize feedback counters in Streamlit's session state
if 'upvotes' not in st.session_state:
    st.session_state.upvotes = 0
if 'downvotes' not in st.session_state:
    st.session_state.downvotes = 0

# Feedback buttons layout
col1, col2 = st.columns(2)
with col1:
    if st.button('👍', key="upvote"):
        st.session_state.upvotes += 1
with col2:
    if st.button('👎', key="downvote"):
        st.session_state.downvotes += 1

st.write(f"Upvotes: {st.session_state.upvotes}, Downvotes: {st.session_state.downvotes}")

# User preferences selection
interests = st.multiselect(
    "Select your areas of interest:",
    options=["Technology", "Automobile", "Healthcare", "Energy", "Financial Services"],
    default=["Technology"]
)

# Query ticker input with unique key
query_ticker = st.text_input('Enter stock ticker (e.g., AAPL):', key='queryTicker').upper()

# Display recommendations and stock performance chart based on the entered ticker
if query_ticker and st.button('Show Recommendations', key='showRecs'):
    st.write("### Recommendations based on Market and Segment:")
    market_segment_recommendations = recommend_by_market_segment(query_ticker)
    if market_segment_recommendations:
        for rec in market_segment_recommendations:
            st.write(rec)
    else:
        st.write("No market/segment-based recommendations found.")
    
    st.write("### Recommendations based on Financial Metrics:")
    financial_recommendations = recommend_stocks(query_ticker, market_segment_recommendations)
    if financial_recommendations:
        for rec in financial_recommendations:
            st.write(rec)
    else:
        st.write("No financial-based recommendations found.")
    
    plot_stock_performance(query_ticker)


def compare_stock_performance(tickers):
    fig = go.Figure()
    for ticker in tickers:
        data = yf.download(ticker, period="1y")
        fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name=ticker))
    fig.update_layout(title='Comparative Stock Performance', xaxis_title='Date', yaxis_title='Price')
    st.plotly_chart(fig)

# User input for comparing stocks
compare_tickers = st.multiselect('Select stocks to compare:', options=list(stock_categories.keys()), default=['AAPL', 'MSFT'])
if st.button('Compare Stocks'):
    compare_stock_performance(compare_tickers)
