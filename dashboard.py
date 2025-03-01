import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import ollama
import tempfile
import base64
import os
from stock_api import StockApiClient


class StockAnalysisDashboard:
    def __init__(self):
        st.set_page_config(layout="wide")
        st.title("AI-Powered Technical Stock Analysis Dashboard")
        st.sidebar.header("Configuration")


    def fetch_stock_data(self, ticker, start_date, end_date):
        """Fetches stock data using yfinance and stores it in session state."""
        client = StockApiClient(ticker=ticker, start_date=start_date, end_date=end_date)
        # data = client.get_data()
        data = pd.read_csv("test_data.csv", index_col="date").loc[start_date:end_date]
        st.session_state["stock_data"] = data
        st.success("Stock data loaded successfully!")
        
        return data


    def build_candlestick_chart(self, data):
        """Creates a Plotly candlestick chart using the provided stock data."""
        fig = go.Figure(data=[
            go.Candlestick(
                x=data.index,
                open=data['open'],
                high=data['high'],
                low=data['low'],
                close=data['close'],
                name="Candlestick"
            )
        ])

        return fig


    def add_indicator(self, fig, data, indicator):
        """Adds a technical indicator to the chart based on user selection."""
        if indicator == "20-Day SMA":
            sma = data['Close'].rolling(window=20).mean()
            fig.add_trace(go.Scatter(x=data.index, y=sma, mode='lines', name='SMA (20)'))
        elif indicator == "20-Day EMA":
            ema = data['Close'].ewm(span=20).mean()
            fig.add_trace(go.Scatter(x=data.index, y=ema, mode='lines', name='EMA (20)'))
        elif indicator == "20-Day Bollinger Bands":
            sma = data['Close'].rolling(window=20).mean()
            std = data['Close'].rolling(window=20).std()
            bb_upper = sma + 2 * std
            bb_lower = sma - 2 * std
            fig.add_trace(go.Scatter(x=data.index, y=bb_upper, mode='lines', name='BB Upper'))
            fig.add_trace(go.Scatter(x=data.index, y=bb_lower, mode='lines', name='BB Lower'))
        elif indicator == "VWAP":
            data['VWAP'] = (data['Close'] * data['Volume']).cumsum() / data['Volume'].cumsum()
            fig.add_trace(go.Scatter(x=data.index, y=data['VWAP'], mode='lines', name='VWAP'))


    def run_ai_analysis(self, fig):
        """Saves the chart as an image, sends it to the AI model for analysis, and displays the result."""
        with st.spinner("Analyzing the chart, please wait..."):
            # Save the current chart to a temporary PNG file
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmpfile:
                fig.write_image(tmpfile.name)
                tmpfile_path = tmpfile.name

            # Read the image and encode it to Base64
            with open(tmpfile_path, "rb") as image_file:
                image_data = base64.b64encode(image_file.read()).decode('utf-8')

            # Define the prompt for AI analysis
            prompt = (
                "You are a Stock Trader specializing in Technical Analysis at a top financial institution."
                "Analyze the stock chart's technical indicators and provide a buy/hold/sell recommendation."
                "Base your recommendation only on the candlestick chart and the displayed technical indicators."
                "First, provide the recommendation, then, provide your detailed reasoning."
            )
            messages = [{
                'role': 'user',
                'content': prompt,
                'images': [image_data]
            }]

            # Get AI analysis using ollama
            response = ollama.chat(model='llama3.2-vision', messages=messages)
            st.write("**AI Analysis Results:**")
            st.write(response["message"]["content"])

            # Clean up the temporary image file
            os.remove(tmpfile_path)


    def run(self):
        # Sidebar inputs for ticker and date range
        ticker = st.sidebar.text_input("Enter Stock Ticker (e.g., AAPL):", "AAPL")
        end_date = str(st.sidebar.date_input("Start Date", value=pd.to_datetime("2023-01-01")))
        start_date = str(st.sidebar.date_input("End Date", value=pd.to_datetime("2024-12-14")))

        # Fetch data when button is pressed
        if st.sidebar.button("Fetch Data"):
            self.fetch_stock_data(ticker, start_date, end_date)

        # Proceed if stock data is available in session state
        if "stock_data" in st.session_state:
            data = st.session_state["stock_data"]

            # Build the initial candlestick chart
            fig = self.build_candlestick_chart(data)

            # Sidebar: Technical Indicators selection
            st.sidebar.subheader("Technical Indicators")
            indicators = st.sidebar.multiselect(
                "Select Indicators:",
                ["20-Day SMA", "20-Day EMA", "20-Day Bollinger Bands", "VWAP"],
                default=["20-Day SMA"]
            )

            # Add each selected indicator to the chart
            # for indicator in indicators:
            #     self.add_indicator(fig, data, indicator)

            fig.update_layout(xaxis_rangeslider_visible=False)
            st.plotly_chart(fig)

            # # AI Analysis Section
            # st.subheader("AI-Powered Analysis")
            # if st.button("Run AI Analysis"):
            #     self.run_ai_analysis(fig)
