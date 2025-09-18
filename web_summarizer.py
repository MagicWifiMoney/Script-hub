#!/usr/bin/env python3
"""
Web Article Summarizer - Extract and summarize any web article
Requires: pip install requests beautifulsoup4
"""

import sys
import re
from urllib.parse import urlparse

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("ERROR: Required packages not installed!")
    print("Please run: pip install requests beautifulsoup4")
    sys.exit(1)

def clean_text(text):
    """Clean and format text"""
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters but keep punctuation
    text = re.sub(r'[^\w\s\.\,\!\?\-\:\;\'\"]', '', text)
    return text.strip()

def summarize_article(url):
    """Extract and summarize article from URL"""
    
    print("="*60)
    print("WEB ARTICLE ANALYZER")
    print("="*60)
    print(f"URL: {url}\n")
    
    try:
        # Fetch the webpage
        print("📡 Fetching article...")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract title
        title = soup.find('title')
        if title:
            print(f"📰 Title: {title.text.strip()}\n")
        
        # Extract metadata
        print("METADATA")
        print("-"*40)
        
        # Try to find author
        author = soup.find('meta', {'name': 'author'})
        if author:
            print(f"Author: {author.get('content', 'Unknown')}")
        
        # Try to find publish date
        date = soup.find('meta', {'property': 'article:published_time'})
        if date:
            print(f"Published: {date.get('content', 'Unknown')[:10]}")
        
        # Domain
        domain = urlparse(url).netloc
        print(f"Source: {domain}")
        print()
        
        # Extract main content
        print("CONTENT EXTRACTION")
        print("-"*40)
        
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "header", "footer", "aside"]):
            script.decompose()
        
        # Try to find main content area
        main_content = None
        for selector in ['article', 'main', '.content', '#content', '.post', '.entry-content']:
            main_content = soup.select_one(selector)
            if main_content:
                break
        
        if not main_content:
            main_content = soup.find('body')
        
        if main_content:
            # Extract text
            text = main_content.get_text()
            text = clean_text(text)
            
            # Basic statistics
            words = text.split()
            sentences = text.split('.')
            
            print(f"✓ Extracted {len(words)} words")
            print(f"✓ Found {len(sentences)} sentences")
            print(f"✓ Estimated reading time: {len(words)//200} minutes")
            print()
            
            # Extract key points (paragraphs)
            paragraphs = []
            for p in main_content.find_all('p'):
                p_text = clean_text(p.get_text())
                if len(p_text) > 50:  # Filter out short paragraphs
                    paragraphs.append(p_text)
            
            print("KEY POINTS")
            print("-"*40)
            
            if paragraphs:
                # Show first 3 substantial paragraphs
                for i, para in enumerate(paragraphs[:3], 1):
                    print(f"\n{i}. {para[:200]}...")
            else:
                # Fallback to first 500 chars
                print(text[:500] + "...")
            
            print()
            
            # Extract headings for structure
            headings = []
            for h in main_content.find_all(['h1', 'h2', 'h3']):
                h_text = clean_text(h.get_text())
                if h_text:
                    headings.append(h_text)
            
            if headings:
                print("ARTICLE STRUCTURE")
                print("-"*40)
                for heading in headings[:10]:
                    print(f"• {heading}")
                print()
            
            # Extract links
            links = main_content.find_all('a', href=True)
            external_links = []
            for link in links:
                href = link['href']
                if href.startswith('http') and domain not in href:
                    external_links.append(href)
            
            if external_links:
                print("REFERENCED SOURCES")
                print("-"*40)
                for link in list(set(external_links))[:5]:
                    print(f"• {link}")
                print()
            
            # Summary
            print("SUMMARY")
            print("-"*40)
            
            # Create a basic summary (first + last substantial paragraph)
            if len(paragraphs) >= 2:
                print("Opening:")
                print(paragraphs[0][:300] + "...")
                print("\nConclusion:")
                print(paragraphs[-1][:300] + "...")
            else:
                print(text[:600] + "...")
            
            print("\n" + "="*60)
            print("✅ ANALYSIS COMPLETE")
            print("="*60)
            
        else:
            print("❌ Could not extract main content from the page")
            
    except requests.RequestException as e:
        print(f"❌ Error fetching URL: {str(e)}")
    except Exception as e:
        print(f"❌ Error processing article: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        url = sys.argv[1]
        
        # Add http if not present
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        summarize_article(url)
    else:
        print("Usage: python web_summarizer.py URL")
        print("Example: python web_summarizer.py https://example.com/article")
        print("\nTesting with example article...")
        summarize_article("https://en.wikipedia.org/wiki/Artificial_intelligence")