"""
Autonomous SEO Analysis Engine
Coordinates multiple APIs to provide comprehensive SEO analysis and recommendations
"""

import os
import asyncio
import concurrent.futures
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import json
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
import time

# Import our API clients
from api_clients import (
    anthropic_client, openai_client, perplexity_client,
    dataforseo_client, keywords_everywhere_client,
    APIResponse, get_ai_client
)

class SEOAnalysisEngine:
    """Main engine for autonomous SEO analysis"""

    def __init__(self, ai_provider: str = None):
        self.ai_client = get_ai_client(ai_provider)
        self.max_workers = int(os.getenv('MAX_CONCURRENT_REQUESTS', '3'))

    def analyze_website(self, website_url: str, analysis_type: str = "comprehensive",
                       client_name: str = None) -> Dict:
        """
        Perform complete autonomous SEO analysis

        Args:
            website_url: URL to analyze
            analysis_type: quick, comprehensive, technical, or local
            client_name: Optional client name for personalized output

        Returns:
            Complete SEO analysis results
        """

        # Normalize URL
        if not website_url.startswith(('http://', 'https://')):
            website_url = f"https://{website_url}"

        analysis_start = time.time()

        # Initialize results structure
        results = {
            "website_url": website_url,
            "client_name": client_name,
            "analysis_type": analysis_type,
            "timestamp": datetime.now().isoformat(),
            "analysis_duration": None,
            "data_sources": [],
            "seo_score": None,
            "analysis": None,
            "technical_data": {},
            "keyword_data": {},
            "competitive_data": {},
            "recommendations": [],
            "errors": []
        }

        try:
            # Step 1: Basic website analysis (fast)
            basic_data = self._get_basic_website_data(website_url)
            results["technical_data"]["basic"] = basic_data

            # Determine industry/business type from website
            industry = self._detect_industry(basic_data)

            # Step 2: Parallel API calls based on analysis type
            api_results = self._run_parallel_analysis(website_url, analysis_type, industry)

            # Step 3: Collect keyword data
            if analysis_type in ["comprehensive", "quick"]:
                keyword_results = self._analyze_keywords(website_url, basic_data)
                results["keyword_data"] = keyword_results

            # Step 4: Competitive analysis for comprehensive reports
            if analysis_type == "comprehensive":
                competitive_results = self._analyze_competition(website_url, industry)
                results["competitive_data"] = competitive_results

            # Step 5: Compile all data and get AI analysis
            results["technical_data"].update(api_results)

            # Step 6: Get AI-powered insights and recommendations
            ai_analysis = self._get_ai_analysis(website_url, results, analysis_type)
            if ai_analysis.success:
                results["analysis"] = ai_analysis.data.get("analysis", "")
                results["seo_score"] = self._extract_seo_score(ai_analysis.data.get("analysis", ""))
            else:
                results["errors"].append(f"AI analysis failed: {ai_analysis.error}")

            # Step 7: Generate actionable recommendations
            results["recommendations"] = self._generate_recommendations(results)

        except Exception as e:
            results["errors"].append(f"Analysis error: {str(e)}")

        finally:
            results["analysis_duration"] = round(time.time() - analysis_start, 2)

        return results

    def _get_basic_website_data(self, website_url: str) -> Dict:
        """Get basic website data through web scraping"""
        data = {
            "title": "",
            "meta_description": "",
            "h1_tags": [],
            "meta_keywords": "",
            "language": "en",
            "responsive": False,
            "https": website_url.startswith('https://'),
            "load_time": None,
            "status_code": None,
            "content_type": "",
            "robots_txt_exists": False,
            "sitemap_exists": False
        }

        try:
            # Time the request
            start_time = time.time()
            response = requests.get(website_url, timeout=10, headers={
                'User-Agent': 'SEO-Analysis-Bot/1.0'
            })
            load_time = time.time() - start_time

            data["status_code"] = response.status_code
            data["load_time"] = round(load_time, 2)
            data["content_type"] = response.headers.get('content-type', '')

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')

                # Extract basic SEO elements
                title_tag = soup.find('title')
                data["title"] = title_tag.text.strip() if title_tag else ""

                meta_desc = soup.find('meta', attrs={'name': 'description'})
                data["meta_description"] = meta_desc.get('content', '') if meta_desc else ""

                meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
                data["meta_keywords"] = meta_keywords.get('content', '') if meta_keywords else ""

                # Get H1 tags
                h1_tags = soup.find_all('h1')
                data["h1_tags"] = [h1.text.strip() for h1 in h1_tags]

                # Check for responsive design
                viewport = soup.find('meta', attrs={'name': 'viewport'})
                data["responsive"] = bool(viewport)

                # Language detection
                html_lang = soup.find('html')
                if html_lang and html_lang.get('lang'):
                    data["language"] = html_lang.get('lang')[:2]

            # Check robots.txt and sitemap
            domain = urlparse(website_url).netloc

            try:
                robots_response = requests.get(f"https://{domain}/robots.txt", timeout=5)
                data["robots_txt_exists"] = robots_response.status_code == 200
            except:
                pass

            try:
                sitemap_response = requests.get(f"https://{domain}/sitemap.xml", timeout=5)
                data["sitemap_exists"] = sitemap_response.status_code == 200
            except:
                pass

        except Exception as e:
            data["error"] = str(e)

        return data

    def _detect_industry(self, basic_data: Dict) -> str:
        """Detect industry/business type from website content"""
        title = basic_data.get("title", "").lower()
        description = basic_data.get("meta_description", "").lower()
        content = f"{title} {description}"

        # Simple keyword-based industry detection
        industry_keywords = {
            "ecommerce": ["shop", "buy", "store", "product", "cart", "checkout"],
            "restaurant": ["restaurant", "menu", "food", "dining", "kitchen"],
            "legal": ["lawyer", "attorney", "legal", "law", "court"],
            "medical": ["doctor", "medical", "health", "clinic", "hospital"],
            "real_estate": ["real estate", "property", "homes", "realtor"],
            "local_service": ["service", "local", "repair", "cleaning", "plumbing"],
            "saas": ["software", "app", "platform", "service", "cloud"],
            "blog": ["blog", "article", "news", "post"]
        }

        for industry, keywords in industry_keywords.items():
            if any(keyword in content for keyword in keywords):
                return industry

        return "general"

    def _run_parallel_analysis(self, website_url: str, analysis_type: str, industry: str) -> Dict:
        """Run API calls in parallel for faster results"""
        results = {}

        # Define which APIs to call based on analysis type
        api_calls = []

        if analysis_type in ["comprehensive", "technical"]:
            api_calls.extend([
                ("dataforseo_domain", lambda: dataforseo_client.get_domain_analysis(website_url)),
                ("dataforseo_audit", lambda: dataforseo_client.get_on_page_audit(website_url))
            ])

        # Run API calls with thread pool for I/O bound operations
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_key = {
                executor.submit(api_call): key
                for key, api_call in api_calls
            }

            for future in concurrent.futures.as_completed(future_to_key, timeout=60):
                key = future_to_key[future]
                try:
                    api_response = future.result()
                    if api_response.success:
                        results[key] = api_response.data
                    else:
                        results[f"{key}_error"] = api_response.error
                except Exception as e:
                    results[f"{key}_error"] = str(e)

        return results

    def _analyze_keywords(self, website_url: str, basic_data: Dict) -> Dict:
        """Extract and analyze keywords from website content"""
        keyword_results = {
            "extracted_keywords": [],
            "keyword_data": [],
            "opportunities": []
        }

        try:
            # Extract potential keywords from content
            content_keywords = self._extract_keywords_from_content(basic_data)
            keyword_results["extracted_keywords"] = content_keywords

            if content_keywords:
                # Get search volume and competition data
                kw_response = keywords_everywhere_client.get_keyword_data(content_keywords[:10])  # Limit to avoid high costs
                if kw_response.success:
                    keyword_results["keyword_data"] = kw_response.data.get("keyword_data", [])

                # Get related keywords for the main keyword
                if content_keywords:
                    related_response = keywords_everywhere_client.get_related_keywords(content_keywords[0])
                    if related_response.success:
                        keyword_results["opportunities"] = related_response.data.get("related_keywords", [])[:20]

        except Exception as e:
            keyword_results["error"] = str(e)

        return keyword_results

    def _extract_keywords_from_content(self, basic_data: Dict) -> List[str]:
        """Extract potential keywords from website content"""
        import re

        # Combine title and description
        content = f"{basic_data.get('title', '')} {basic_data.get('meta_description', '')} {' '.join(basic_data.get('h1_tags', []))}"

        # Simple keyword extraction (remove common stop words)
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should'}

        # Extract words, clean and filter
        words = re.findall(r'\b[a-zA-Z]{3,}\b', content.lower())
        keywords = [word for word in words if word not in stop_words and len(word) > 2]

        # Get most frequent keywords
        from collections import Counter
        keyword_counts = Counter(keywords)
        return [kw for kw, count in keyword_counts.most_common(15)]

    def _analyze_competition(self, website_url: str, industry: str) -> Dict:
        """Analyze competitive landscape"""
        competitive_data = {}

        try:
            # Use Perplexity for real-time competitive analysis
            comp_response = perplexity_client.analyze_competitors(website_url, industry)
            if comp_response.success:
                competitive_data = comp_response.data
            else:
                competitive_data["error"] = comp_response.error

        except Exception as e:
            competitive_data["error"] = str(e)

        return competitive_data

    def _get_ai_analysis(self, website_url: str, data: Dict, analysis_type: str) -> APIResponse:
        """Get AI-powered analysis of all collected data"""

        # Use Claude (Anthropic) as primary AI for analysis
        return anthropic_client.analyze_seo_data(website_url, data, analysis_type)

    def _extract_seo_score(self, analysis_text: str) -> Optional[int]:
        """Extract SEO score from AI analysis text"""
        import re

        # Look for patterns like "SEO score: 75" or "score of 85"
        patterns = [
            r'SEO score[:\s]+(\d+)',
            r'score[:\s]+(\d+)',
            r'(\d+)[\s/]+100',
            r'(\d+)%'
        ]

        for pattern in patterns:
            match = re.search(pattern, analysis_text, re.IGNORECASE)
            if match:
                score = int(match.group(1))
                if 0 <= score <= 100:
                    return score

        return None

    def _generate_recommendations(self, results: Dict) -> List[Dict]:
        """Generate prioritized recommendations from analysis results"""
        recommendations = []

        # Analyze technical issues
        basic_data = results["technical_data"].get("basic", {})

        if not basic_data.get("title"):
            recommendations.append({
                "priority": "High",
                "category": "Technical",
                "issue": "Missing page title",
                "recommendation": "Add descriptive title tags to all pages",
                "impact": "Critical for search rankings and click-through rates"
            })

        if not basic_data.get("meta_description"):
            recommendations.append({
                "priority": "High",
                "category": "On-Page",
                "issue": "Missing meta description",
                "recommendation": "Add compelling meta descriptions to improve click-through rates",
                "impact": "Higher CTR from search results"
            })

        if not basic_data.get("responsive"):
            recommendations.append({
                "priority": "High",
                "category": "Technical",
                "issue": "Not mobile-friendly",
                "recommendation": "Implement responsive design with proper viewport meta tag",
                "impact": "Critical for mobile rankings and user experience"
            })

        if basic_data.get("load_time", 0) > 3:
            recommendations.append({
                "priority": "High",
                "category": "Performance",
                "issue": f"Slow loading time ({basic_data.get('load_time')}s)",
                "recommendation": "Optimize images, enable compression, and use CDN",
                "impact": "Better user experience and search rankings"
            })

        if not basic_data.get("https"):
            recommendations.append({
                "priority": "High",
                "category": "Security",
                "issue": "Not using HTTPS",
                "recommendation": "Implement SSL certificate and redirect HTTP to HTTPS",
                "impact": "Essential for security and search rankings"
            })

        if not basic_data.get("h1_tags"):
            recommendations.append({
                "priority": "Medium",
                "category": "On-Page",
                "issue": "Missing H1 tags",
                "recommendation": "Add descriptive H1 tags to structure content hierarchy",
                "impact": "Better content organization and keyword relevance"
            })

        # Add keyword-based recommendations
        keyword_data = results.get("keyword_data", {})
        if keyword_data.get("opportunities"):
            recommendations.append({
                "priority": "Medium",
                "category": "Content",
                "issue": "Keyword opportunities identified",
                "recommendation": f"Create content targeting high-volume keywords: {', '.join([kw.get('keyword', '') for kw in keyword_data['opportunities'][:3]])}",
                "impact": "Increased organic traffic potential"
            })

        return recommendations

# Convenience function for direct usage
def analyze_website_seo(website_url: str, analysis_type: str = "quick",
                       client_name: str = None, ai_provider: str = None) -> Dict:
    """
    Direct function to analyze website SEO

    Args:
        website_url: Website URL to analyze
        analysis_type: Type of analysis (quick, comprehensive, technical, local)
        client_name: Optional client name
        ai_provider: AI provider to use (anthropic, openai, perplexity)

    Returns:
        Complete SEO analysis results
    """
    engine = SEOAnalysisEngine(ai_provider)
    return engine.analyze_website(website_url, analysis_type, client_name)

if __name__ == "__main__":
    # Test the engine
    import os

    # Load test environment
    test_url = "https://example.com"
    print(f"Testing SEO analysis for: {test_url}")

    results = analyze_website_seo(test_url, "quick", "Test Client")
    print(json.dumps(results, indent=2))