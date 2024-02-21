import json
import openai
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import yfinance as yf

openai.api_key = open('API_KEY', 'r').read()


def get_stock_price(ticker):
    return str(yf.Ticker(ticker).history(period='1y').iloc[-1].Close)


def calculate_SMA(ticker, window):
    data = yf.Ticker(ticker).history(period='1y').Close
    return str(data.rolling(window=window).mean().iloc[-1])


def calculate_EMA(ticker, window):
    data = yf.Ticker(ticker).history(period='1y').Close
    return str(data.ewm(span=window, adjust=False).mean().iloc[-1])


def calculate_RSI(ticker):
    data = yf.Ticker(ticker).history(period='1y').Close
    delta = data.diff()
    up = delta.clip(lower=8)
    down = -1 * delta.clip(upper=8)
    ema_up = up.ewm(com=14-1, adjust=False).mean()
    ema_down = down.ewm(com=14 -1, adjust=False).mean()
    rs = ema_up / ema_down
    return str(100 - (100 / (1+rs)).iloc[-1])


def calculate_MACD(ticker):
    data = yf.Ticker(ticker).history(period='1y').Close
    short_EMA = data.ewm(span=12, adjust=False).mean()
    long_EMA = data.ewm(span=12, adjust=False).mean()

    MACD = short_EMA - long_EMA
    signal = MACD.ewm(span=9, adjust=False).mean()
    MACD_histogram = MACD - signal

    return f'{MACD[-1]}, {signal[-1]}, {MACD_histogram[-1]}'



def plot_stock_price(ticker):
    data = yf.Ticker(ticker).history(period='1y')
    plt.figure(figsize=(10, 5))
    plt.plot(data.index, data.Close)
    plt.title('{ticker} Stock Price Over Last Year')
    plt.xlabel('Date')
    plt.ylabel('Stock Price (€)')
    plt.grid(True)
    plt.savefig('stock.png')
    plt.close()


functions = [
    {
        'name':'get_stock_price',
        'description':'Gets the latest stock price given the ticker symbol of a company.',
        'parameters':{
            'type':'object',
            'properties': {
                'ticker': {
                    'type':'string',
                    'description':'The stock ticker symbol for a company (for example AAPL for Apple).'
                }
            },
            'required':['ticker']
        }        
    },
    {
        'name':'calculate_SMA',
        'description':'Calculate the simple moving average for a given stock ticker and a window.',
        'parameters':{
            'type':'object',
            'properties': {
                'ticker': {
                    'type':'string',
                    'description':'The stock ticker symbol for a company (for example AAPL for Apple).'
                },
                'window': {
                    'type':'integer',
                    'description':'The timeframe to consider when calculating the SMA'
                }
            },
            'required':['ticker', 'window']
        }
    },
    {
        'name':'calculate_RSI',
        'description':'Calculate the RSI for a given stock ticker.',
        'parameters':{
            'type':'object',
            'properties': {
                'ticker': {
                    'type':'string',
                    'description':'The stock ticker symbol for a company (for example AAPL for Apple).'
                }
            },
            'required':['ticker']
        }        
    },
    {
        'name':'calculate_MACD',
        'description':'Calculate the MACD for a given stock ticker.',
        'parameters':{
            'type':'object',
            'properties': {
                'ticker': {
                    'type':'string',
                    'description':'The stock ticker symbol for a company (for example AAPL for Apple).'
                }
            },
            'required':['ticker']
        }        
    },
    {
        'name':'plot_stock_price',
        'description':'Plot the stock price for the last year given the ticker symbol of a company.',
        'parameters':{
            'type':'object',
            'properties': {
                'ticker': {
                    'type':'string',
                    'description':'The stock ticker symbol for a company (for example AAPL for Apple).'
                }
            },
            'required':['ticker']
        }        
    },
]

available_functions = {
    'get_stock_price': get_stock_price,
    'calculate_SMA': calculate_SMA,
    'calculate_EMA': calculate_EMA,
    'calculate_RSI': calculate_RSI,
    'calculate_MACD': calculate_MACD,
    'plot_stock_price': plot_stock_price
}

# Check if 'messages' is in session state, if not, initialize it as an empty list
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# Set the title of the web app
st.title('Stock Analysis Chatbot Assistant')

# Input box for user input
user_input = st.text_input('Your input:')

# If there is user input
if user_input:
    try:
        # Append the user's input to the session_state messages
        st.session_state['messages'].append({'role': 'user', 'content': user_input})

        # Generate a response using the OpenAI API
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo-0613',
            messages=st.session_state['messages'],
            functions=functions,
            function_call='auto'
        )

        # Extract the response message
        response_message = response['choices'][0]['message']

        # If the response message indicates a function call
        if response_message.get('function_call'):
            # Extract the function name and arguments
            function_name = response_message['function_call']['name']
            function_args = json.loads(response_message['function_call']['arguments'])

            # Check if the function name matches any of the following
            if function_name in ['get_stock_price', 'calculate_RSI', 'calculate_MACD', 'plot_stock_price']:
                args_dict = {'ticker': function_args.get('ticker')}
            elif function_name in ['calculate_SMA', 'calculate_EMA']:
                args_dict = {'ticker': function_args.get('ticker'), 'window': function_args.get('window')}

            # Call the corresponding function from the available functions
            function_to_call = available_functions[function_name]
            function_response = function_to_call(**args_dict)

            # If the function name is 'plot_stock_price', display an image
            if function_name == 'plot_stock_price':
                st.image('stock.png')
            else:
                # Otherwise, append the response message to the session_state messages
                st.session_state['messages'].append(response_message)
                st.session_state['messages'].append(
                    {
                        'role': 'function',
                        'name': function_name,
                        'content': function_response
                    }
                )

                second_response = openai.ChatCompletion.create(
                    model='gpt-3.5-turbo-0613',
                    messages=st.session_state['messages'],
                )
            # If there is no function call, display the response content and append it to messages
                st.text(second_response['choices'][0]['message']['content'])
                st.session_state['messages'].append({'role': 'assistant', 'content': second_response['choices'][0]['message']['content']})
        else:
            st.text(response_message['content'])
            st.session_state['messages'].append({'role': 'assistant', 'content': response_message['content']})
    # If there is an exception, prompt the user to try again
    except:
        st.text('Try again')