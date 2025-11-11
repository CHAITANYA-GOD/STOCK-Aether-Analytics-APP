# modules/sentiment_fetcher.py
'''import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import re
import streamlit as st
import random # For fallback

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.59'
]

def fetch_and_analyze_sentiment(ticker):
    """
    Fetches news headlines via Google Search simulation and calculates average sentiment polarity.
    Returns a single float score between -1.0 (very negative) and 1.0 (very positive).
    """
    
    # Use a generic query to get broad financial news related to the ticker
    query = f"stock market news {ticker} financial analysis"
    url = f"https://www.google.com/search?q={query}&tbm=nws&hl=en" # tbm=nws limits results to news
    
    headers = {'User-Agent': random.choice(USER_AGENTS)}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() # Raise an exception for bad status codes
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Google news titles are typically found in <div> elements with a specific class
        headlines = [a.get_text() for a in soup.find_all('div', class_=re.compile(r'BNeawe deIvCb AP7Wnd'))]

        if not headlines:
            return 0.0 # Return neutral if no headlines found

        total_polarity = 0
        
        # Analyze top 10 headlines only for quick processing
        for headline in headlines[:10]:
            analysis = TextBlob(headline)
            total_polarity += analysis.sentiment.polarity
            
        # Return the average polarity (score between -1 and 1)
        return total_polarity / len(headlines[:10])
    
    except Exception as e:
        # Fallback to neutral score if scraping fails
        st.warning(f"❌ Real-Time Sentiment Fetch Failed (Using Placeholder Score): {e}")
        return 0.05 # Neutral placeholder score'''

# modules/sentiment_fetcher.py (Final Fix for URL Encoding)
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import re
import streamlit as st
import random 
# --- CRITICAL NEW IMPORT ---
from urllib.parse import quote_plus 
# --- END CRITICAL NEW IMPORT ---

# Define the Google News RSS URL structure
GN_RSS_URL = "https://news.google.com/rss/search?q={query}&hl=en-IN&gl=IN&ceid=IN:en"

# ... (USER_AGENTS list remains the same) ...

def fetch_and_analyze_sentiment(ticker):
    """
    Fetches real-time financial news headlines using Google News RSS 
    and calculates average sentiment polarity.
    """
    try:
        # 1. Prepare Query and Fetch RSS Feed
        search_query = f"{ticker} stock news India"
        
        # --- FIX: URL ENCODE THE QUERY STRING ---
        encoded_query = quote_plus(search_query)
        # --- END FIX ---
        
        feed_url = GN_RSS_URL.format(query=encoded_query)
        
        # Use feedparser to reliably fetch and parse the XML (assuming you installed feedparser)
        import feedparser # Local import for clarity, though it should be at the top
        gn_feed = feedparser.parse(feed_url)
        
        headlines = [entry.title for entry in gn_feed.entries]

        if not headlines:
            return 0.0 

        # 2. Analyze Sentiment
        total_polarity = 0
        
        for headline in headlines:
            analysis = TextBlob(headline)
            total_polarity += analysis.sentiment.polarity
            
        # 3. Return the average polarity
        average_polarity = total_polarity / len(headlines)
        return average_polarity
    
    except Exception as e:
        # Fallback to neutral score if the network or parsing fails
        st.warning(f"❌ Sentiment Fetch Failed (Using Neutral Score): {e}")
        return 0.05