#!/usr/bin/env python3
"""
Stock Market Analyzer - Get real stock data and analysis
Requires: pip install yfinance pandas
"""

import sys
import json
try:
    import yfinance as yf
    import pandas as pd
except ImportError:
    print("ERROR: Required packages not installed!")
    print("Please run: pip install yfinance pandas")
    sys.exit(1)

def analyze_stock(symbol='AAPL', period='1mo'):
    """Analyze a stock and provide insights"""
    
    print(f"{'='*60}")
    print(f"STOCK ANALYSIS: {symbol}")
    print(f"{'='*60}\n")
    
    # Get stock data
    stock = yf.Ticker(symbol)
    
    # Get basic info
    info = stock.info
    print("COMPANY INFORMATION")
    print("-" * 40)
    print(f"Name: {info.get('longName', 'N/A')}")
    print(f"Sector: {info.get('sector', 'N/A')}")
    print(f"Industry: {info.get('industry', 'N/A')}")
    print(f"Market Cap: ${info.get('marketCap', 0):,.0f}")
    print(f"Employees: {info.get('fullTimeEmployees', 'N/A'):,}")
    print()
    
    # Current price data
    print("PRICE INFORMATION")
    print("-" * 40)
    current_price = info.get('currentPrice', info.get('regularMarketPrice', 0))
    print(f"Current Price: ${current_price:.2f}")
    print(f"52 Week High: ${info.get('fiftyTwoWeekHigh', 0):.2f}")
    print(f"52 Week Low: ${info.get('fiftyTwoWeekLow', 0):.2f}")
    print(f"50 Day Avg: ${info.get('fiftyDayAverage', 0):.2f}")
    print(f"200 Day Avg: ${info.get('twoHundredDayAverage', 0):.2f}")
    print()
    
    # Financial metrics
    print("KEY METRICS")
    print("-" * 40)
    print(f"P/E Ratio: {info.get('trailingPE', 'N/A')}")
    print(f"Forward P/E: {info.get('forwardPE', 'N/A')}")
    print(f"PEG Ratio: {info.get('pegRatio', 'N/A')}")
    print(f"Dividend Yield: {info.get('dividendYield', 0)*100:.2f}%")
    print(f"Profit Margin: {info.get('profitMargins', 0)*100:.2f}%")
    print(f"Revenue Growth: {info.get('revenueGrowth', 0)*100:.2f}%")
    print()
    
    # Get historical data
    hist = stock.history(period=period)
    if not hist.empty:
        print("RECENT PERFORMANCE")
        print("-" * 40)
        start_price = hist['Close'].iloc[0]
        end_price = hist['Close'].iloc[-1]
        change = ((end_price - start_price) / start_price) * 100
        
        print(f"Period: {period}")
        print(f"Start Price: ${start_price:.2f}")
        print(f"End Price: ${end_price:.2f}")
        print(f"Change: {change:+.2f}%")
        print(f"Avg Volume: {hist['Volume'].mean():,.0f}")
        print(f"Volatility (std): ${hist['Close'].std():.2f}")
        print()
    
    # Analysis and recommendations
    print("ANALYSIS")
    print("-" * 40)
    
    # Simple technical analysis
    if current_price > info.get('fiftyDayAverage', current_price):
        print("✓ Trading above 50-day average (Bullish)")
    else:
        print("✗ Trading below 50-day average (Bearish)")
    
    if current_price > info.get('twoHundredDayAverage', current_price):
        print("✓ Trading above 200-day average (Long-term Bullish)")
    else:
        print("✗ Trading below 200-day average (Long-term Bearish)")
    
    pe = info.get('trailingPE', 0)
    if pe > 0:
        if pe < 15:
            print("✓ Low P/E ratio - Potentially undervalued")
        elif pe > 30:
            print("⚠ High P/E ratio - Potentially overvalued")
        else:
            print("• P/E ratio in normal range")
    
    print()
    print("RECOMMENDATION")
    print("-" * 40)
    
    # Simple scoring system
    score = 0
    if current_price > info.get('fiftyDayAverage', current_price):
        score += 1
    if current_price > info.get('twoHundredDayAverage', current_price):
        score += 1
    if 15 <= pe <= 25:
        score += 1
    if info.get('revenueGrowth', 0) > 0.1:
        score += 1
    if info.get('profitMargins', 0) > 0.15:
        score += 1
    
    if score >= 4:
        print("🟢 STRONG BUY - Multiple positive indicators")
    elif score >= 3:
        print("🟢 BUY - Generally positive outlook")
    elif score >= 2:
        print("🟡 HOLD - Mixed signals")
    else:
        print("🔴 CAUTION - Multiple negative indicators")
    
    print(f"\nScore: {score}/5")
    print("\n" + "="*60)
    print("Disclaimer: This is algorithmic analysis, not investment advice!")
    print("="*60)

if __name__ == "__main__":
    # Parse arguments
    symbol = sys.argv[1] if len(sys.argv) > 1 else 'AAPL'
    period = sys.argv[2] if len(sys.argv) > 2 else '1mo'
    
    try:
        analyze_stock(symbol.upper(), period)
    except Exception as e:
        print(f"Error analyzing {symbol}: {str(e)}")
        print("\nMake sure the stock symbol is valid!")
        print("Usage: python stock_analyzer.py SYMBOL PERIOD")
        print("Example: python stock_analyzer.py AAPL 3mo")