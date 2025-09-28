"""
API Clients for Marketing Agency Script Hub
Handles connections to all external APIs for autonomous marketing analysis
"""

import os
import json
import time
import hashlib
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
from datetime import datetime, timedelta
import requests
import base64
from pathlib import Path

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

@dataclass
class APIResponse:
    """Standardized API response format"""
    success: bool
    data: Dict[str, Any]
    error: Optional[str] = None
    api_provider: Optional[str] = None
    cached: bool = False

class CacheManager:
    """Simple file-based cache for API responses"""

    def __init__(self, cache_dir: str = "cache", duration_hours: int = 24):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.duration = timedelta(hours=duration_hours)

    def get_cache_key(self, api_name: str, params: Dict) -> str:
        """Generate cache key from API name and parameters"""
        cache_string = f"{api_name}_{json.dumps(params, sort_keys=True)}"
        return hashlib.md5(cache_string.encode()).hexdigest()

    def get(self, api_name: str, params: Dict) -> Optional[Dict]:
        """Get cached response if available and not expired"""
        if not os.getenv('ENABLE_CACHING', 'true').lower() == 'true':
            return None

        cache_key = self.get_cache_key(api_name, params)
        cache_file = self.cache_dir / f"{cache_key}.json"

        if not cache_file.exists():
            return None

        try:
            with open(cache_file, 'r') as f:
                cached_data = json.load(f)

            # Check expiration
            cached_time = datetime.fromisoformat(cached_data['timestamp'])
            if datetime.now() - cached_time > self.duration:
                cache_file.unlink()  # Delete expired cache
                return None

            return cached_data['data']
        except Exception:
            return None

    def set(self, api_name: str, params: Dict, data: Dict):
        """Cache API response"""
        if not os.getenv('ENABLE_CACHING', 'true').lower() == 'true':
            return

        cache_key = self.get_cache_key(api_name, params)
        cache_file = self.cache_dir / f"{cache_key}.json"

        cached_data = {
            'timestamp': datetime.now().isoformat(),
            'data': data
        }

        try:
            with open(cache_file, 'w') as f:
                json.dump(cached_data, f)
        except Exception as e:
            print(f"Cache write error: {e}")

# Global cache manager
cache = CacheManager(duration_hours=int(os.getenv('CACHE_DURATION', '24')))

class AnthropicClient:
    """Claude API client"""

    def __init__(self):
        self.api_key = os.getenv('ANTHROPIC_API_KEY')
        self.base_url = "https://api.anthropic.com/v1"

    def analyze_seo_data(self, website_url: str, seo_data: Dict, analysis_type: str = "comprehensive") -> APIResponse:
        """Use Claude to analyze SEO data and provide insights"""
        if not self.api_key:
            return APIResponse(False, {}, "Anthropic API key not configured")

        cache_params = {"website": website_url, "analysis_type": analysis_type, "data_hash": hashlib.md5(str(seo_data).encode()).hexdigest()[:10]}
        cached_result = cache.get("anthropic_seo_analysis", cache_params)
        if cached_result:
            return APIResponse(True, cached_result, api_provider="anthropic", cached=True)

        prompt = self._build_seo_analysis_prompt(website_url, seo_data, analysis_type)

        try:
            import anthropic
            client = anthropic.Anthropic(api_key=self.api_key)

            response = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=4000,
                messages=[{"role": "user", "content": prompt}]
            )

            result = {
                "analysis": response.content[0].text,
                "timestamp": datetime.now().isoformat()
            }

            cache.set("anthropic_seo_analysis", cache_params, result)
            return APIResponse(True, result, api_provider="anthropic")

        except Exception as e:
            return APIResponse(False, {}, f"Claude API error: {str(e)}")

    def _build_seo_analysis_prompt(self, website_url: str, seo_data: Dict, analysis_type: str) -> str:
        """Build comprehensive SEO analysis prompt"""
        return f"""
You are an expert SEO strategist analyzing website performance data. Provide a comprehensive analysis of {website_url}.

SEO DATA TO ANALYZE:
{json.dumps(seo_data, indent=2)}

ANALYSIS TYPE: {analysis_type}

Please provide a detailed analysis in the following format:

## 🎯 SEO SCORE & OVERVIEW
- Overall SEO score (0-100) with explanation
- Key strengths and weaknesses summary
- Critical issues requiring immediate attention

## 🔧 TECHNICAL SEO ANALYSIS
- Site speed and Core Web Vitals assessment
- Mobile-friendliness evaluation
- Crawlability and indexing issues
- Technical recommendations with priority levels

## 📝 ON-PAGE SEO ANALYSIS
- Title tags and meta descriptions optimization
- Heading structure evaluation
- Content quality and keyword optimization
- Internal linking opportunities

## 🔗 BACKLINK & AUTHORITY ANALYSIS
- Domain authority assessment
- Backlink profile quality
- Link building opportunities
- Competitive positioning

## 🎯 KEYWORD STRATEGY
- Current keyword rankings performance
- Keyword gaps and opportunities
- Content strategy recommendations
- Local SEO opportunities (if applicable)

## ⚡ PRIORITY ACTION PLAN
Provide 10 specific, actionable items ranked by:
1. Impact level (High/Medium/Low)
2. Implementation difficulty (Easy/Medium/Hard)
3. Expected timeline for results

Format each action as:
- **Action**: Specific task
- **Impact**: Expected improvement
- **Difficulty**: Implementation complexity
- **Timeline**: Expected results timeframe

Make all recommendations specific, actionable, and data-driven based on the provided SEO data.
"""

    def generate_content(self, prompt: str) -> APIResponse:
        """Generate marketing content using Claude"""
        if not self.api_key:
            return APIResponse(False, {}, "Anthropic API key not configured")

        # Create cache parameters based on prompt hash
        cache_params = {"prompt_hash": hashlib.md5(prompt.encode()).hexdigest()[:16]}
        cached_result = cache.get("anthropic_content_generation", cache_params)
        if cached_result:
            return APIResponse(True, cached_result, api_provider="anthropic", cached=True)

        try:
            import anthropic
            client = anthropic.Anthropic(api_key=self.api_key)

            response = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=4000,
                messages=[{"role": "user", "content": prompt}]
            )

            result = {
                "content": response.content[0].text,
                "timestamp": datetime.now().isoformat()
            }

            # Cache the result
            cache.set("anthropic_content_generation", cache_params, result)
            return APIResponse(True, result, api_provider="anthropic")

        except Exception as e:
            return APIResponse(False, {}, f"Claude API error: {str(e)}")

class OpenAIClient:
    """ChatGPT API client"""

    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')

    def analyze_content_opportunities(self, website_url: str, keyword_data: List[Dict]) -> APIResponse:
        """Use ChatGPT for content strategy and opportunity analysis"""
        if not self.api_key:
            return APIResponse(False, {}, "OpenAI API key not configured")

        cache_params = {"website": website_url, "keywords": len(keyword_data)}
        cached_result = cache.get("openai_content_analysis", cache_params)
        if cached_result:
            return APIResponse(True, cached_result, api_provider="openai", cached=True)

        try:
            import openai
            client = openai.OpenAI(api_key=self.api_key)

            prompt = f"""
Analyze content opportunities for {website_url} based on keyword research data:

KEYWORD DATA:
{json.dumps(keyword_data, indent=2)}

Provide:
1. Content gaps analysis
2. High-opportunity keywords for content creation
3. Content cluster recommendations
4. Content calendar suggestions (next 3 months)
5. Competitor content analysis insights
"""

            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=3000
            )

            result = {
                "content_analysis": response.choices[0].message.content,
                "timestamp": datetime.now().isoformat()
            }

            cache.set("openai_content_analysis", cache_params, result)
            return APIResponse(True, result, api_provider="openai")

        except Exception as e:
            return APIResponse(False, {}, f"OpenAI API error: {str(e)}")

    def generate_content(self, prompt: str) -> APIResponse:
        """Generate marketing content using OpenAI/ChatGPT"""
        if not self.api_key:
            return APIResponse(False, {}, "OpenAI API key not configured")

        # Create cache parameters based on prompt hash
        cache_params = {"prompt_hash": hashlib.md5(prompt.encode()).hexdigest()[:16]}
        cached_result = cache.get("openai_content_generation", cache_params)
        if cached_result:
            return APIResponse(True, cached_result, api_provider="openai", cached=True)

        try:
            import openai
            client = openai.OpenAI(api_key=self.api_key)

            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=4000
            )

            result = {
                "content": response.choices[0].message.content,
                "timestamp": datetime.now().isoformat()
            }

            # Cache the result
            cache.set("openai_content_generation", cache_params, result)
            return APIResponse(True, result, api_provider="openai")

        except Exception as e:
            return APIResponse(False, {}, f"OpenAI API error: {str(e)}")

class PerplexityClient:
    """Perplexity API client for real-time competitive analysis"""

    def __init__(self):
        self.api_key = os.getenv('PERPLEXITY_API_KEY')

    def analyze_competitors(self, website_url: str, industry: str) -> APIResponse:
        """Use Perplexity for real-time competitive analysis"""
        if not self.api_key:
            return APIResponse(False, {}, "Perplexity API key not configured")

        cache_params = {"website": website_url, "industry": industry}
        cached_result = cache.get("perplexity_competitor_analysis", cache_params)
        if cached_result:
            return APIResponse(True, cached_result, api_provider="perplexity", cached=True)

        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }

            prompt = f"""
Analyze the competitive landscape for {website_url} in the {industry} industry. Provide:

1. Top 5 direct competitors with their strengths/weaknesses
2. Market positioning analysis
3. Content strategy comparison
4. SEO strategy insights from competitor analysis
5. Opportunity gaps in the market
6. Recent industry trends and changes

Focus on actionable competitive insights for SEO and marketing strategy.
"""

            response = requests.post(
                'https://api.perplexity.ai/chat/completions',
                headers=headers,
                json={
                    "model": "llama-3.1-sonar-large-128k-online",
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 3000
                }
            )

            response.raise_for_status()
            result_data = response.json()

            result = {
                "competitive_analysis": result_data['choices'][0]['message']['content'],
                "timestamp": datetime.now().isoformat()
            }

            cache.set("perplexity_competitor_analysis", cache_params, result)
            return APIResponse(True, result, api_provider="perplexity")

        except Exception as e:
            return APIResponse(False, {}, f"Perplexity API error: {str(e)}")

    def conduct_market_research(self, target_subject: str, research_type: str, depth: str = "standard") -> APIResponse:
        """Conduct real-time market research using Perplexity"""
        if not self.api_key:
            return APIResponse(False, {}, "Perplexity API key not configured")

        cache_params = {"subject": target_subject, "type": research_type, "depth": depth}
        cached_result = cache.get("perplexity_market_research", cache_params)
        if cached_result:
            return APIResponse(True, cached_result, api_provider="perplexity", cached=True)

        # Build research prompt based on type
        research_prompts = {
            "competitive": f"""
            Conduct a comprehensive competitive analysis for {target_subject}. Provide current, actionable intelligence on:
            1. Top 5 direct competitors with recent market moves and changes
            2. Current pricing strategies and recent pricing changes
            3. Latest marketing campaigns and messaging strategies
            4. Recent product launches, partnerships, or strategic moves
            5. Market share changes and competitive positioning shifts
            6. SEO and content marketing strategies comparison
            7. Social media presence and engagement analysis
            8. Customer review sentiment and recent feedback trends
            9. Emerging competitive threats and new market entrants
            10. Strategic recommendations for competitive advantage

            Focus on actionable, recent intelligence (within last 6 months) with specific examples and data points.
            """,

            "market": f"""
            Analyze the current market landscape for {target_subject}. Provide comprehensive market intelligence on:
            1. Market size, growth rate, and recent market dynamics
            2. Current industry trends and emerging opportunities
            3. Customer behavior shifts and changing preferences
            4. Technology disruptions and innovation trends
            5. Regulatory changes and compliance requirements
            6. Economic factors affecting market conditions
            7. Geographic market variations and expansion opportunities
            8. Seasonal patterns and cyclical trends
            9. Investment activity and funding trends in the space
            10. Future market predictions and growth forecasts

            Include specific data, recent studies, and actionable market insights.
            """,

            "audience": f"""
            Research the target audience for {target_subject}. Provide detailed audience intelligence on:
            1. Demographics and psychographic profiles with recent data
            2. Current consumer behavior patterns and purchasing trends
            3. Pain points, challenges, and unmet needs analysis
            4. Preferred communication channels and media consumption habits
            5. Social media behavior and platform preferences
            6. Search behavior, keywords used, and information seeking patterns
            7. Brand loyalty patterns and switching behavior
            8. Price sensitivity and value perception analysis
            9. Influence factors in decision making process
            10. Recent surveys, studies, and consumer sentiment data

            Focus on actionable insights for marketing and product strategy.
            """,

            "keyword": f"""
            Conduct keyword and search trend research for {target_subject}. Provide intelligence on:
            1. High-volume, high-intent keywords with search trends
            2. Emerging search terms and trending queries
            3. Long-tail keyword opportunities with low competition
            4. Search intent analysis (informational, commercial, transactional)
            5. Seasonal keyword trends and cyclical patterns
            6. Geographic variations in search behavior
            7. Related topics and semantic keyword clusters
            8. Question-based keywords and voice search trends
            9. Competitor keyword strategies and gaps
            10. Content opportunities based on search demand

            Include specific search volume data and trend analysis where available.
            """,

            "industry": f"""
            Analyze the {target_subject} industry with comprehensive intelligence on:
            1. Industry size, growth trajectory, and market maturity
            2. Key trends, disruptions, and transformation drivers
            3. Major players, market consolidation, and competitive landscape
            4. Innovation trends, emerging technologies, and R&D focus
            5. Regulatory environment and compliance challenges
            6. Supply chain dynamics and operational considerations
            7. Investment patterns, M&A activity, and funding trends
            8. Customer expectations evolution and service standards
            9. Sustainability trends and environmental considerations
            10. Future industry outlook and strategic recommendations

            Provide strategic-level insights with supporting data and examples.
            """
        }

        prompt = research_prompts.get(research_type, research_prompts["competitive"])

        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }

            response = requests.post(
                'https://api.perplexity.ai/chat/completions',
                headers=headers,
                json={
                    "model": "llama-3.1-sonar-large-128k-online",
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 4000
                }
            )

            response.raise_for_status()
            result_data = response.json()

            result = {
                "research_intelligence": result_data['choices'][0]['message']['content'],
                "research_type": research_type,
                "target_subject": target_subject,
                "depth": depth,
                "timestamp": datetime.now().isoformat(),
                "sources": "Real-time web intelligence via Perplexity AI"
            }

            cache.set("perplexity_market_research", cache_params, result)
            return APIResponse(True, result, api_provider="perplexity")

        except Exception as e:
            return APIResponse(False, {}, f"Perplexity research API error: {str(e)}")

class DataForSEOClient:
    """DataForSEO API client for comprehensive SEO data"""

    def __init__(self):
        self.login = os.getenv('DATAFORSEO_LOGIN')
        self.password = os.getenv('DATAFORSEO_PASSWORD')
        self.base_url = "https://api.dataforseo.com/v3"

    def _make_request(self, endpoint: str, data: List[Dict]) -> Dict:
        """Make authenticated request to DataForSEO API"""
        auth = base64.b64encode(f"{self.login}:{self.password}".encode()).decode()
        headers = {
            'Authorization': f'Basic {auth}',
            'Content-Type': 'application/json'
        }

        response = requests.post(f"{self.base_url}/{endpoint}", headers=headers, json=data)
        response.raise_for_status()
        return response.json()

    def get_domain_analysis(self, website_url: str) -> APIResponse:
        """Get comprehensive domain analysis including backlinks, organic traffic, etc."""
        if not self.login or not self.password:
            return APIResponse(False, {}, "DataForSEO credentials not configured")

        domain = website_url.replace('https://', '').replace('http://', '').split('/')[0]
        cache_params = {"domain": domain, "analysis": "comprehensive"}
        cached_result = cache.get("dataforseo_domain_analysis", cache_params)
        if cached_result:
            return APIResponse(True, cached_result, api_provider="dataforseo", cached=True)

        try:
            # Get domain overview
            domain_data = self._make_request("domain_analytics/overview/live", [{
                "target": domain,
                "location_code": 2840,  # USA
                "language_code": "en"
            }])

            # Get backlink data
            backlink_data = self._make_request("backlinks/summary/live", [{
                "target": domain,
                "internal_list_limit": 10,
                "backlinks_status_type": "live"
            }])

            result = {
                "domain_overview": domain_data,
                "backlink_summary": backlink_data,
                "timestamp": datetime.now().isoformat()
            }

            cache.set("dataforseo_domain_analysis", cache_params, result)
            return APIResponse(True, result, api_provider="dataforseo")

        except Exception as e:
            return APIResponse(False, {}, f"DataForSEO API error: {str(e)}")

    def get_on_page_audit(self, website_url: str) -> APIResponse:
        """Get technical SEO audit data"""
        if not self.login or not self.password:
            return APIResponse(False, {}, "DataForSEO credentials not configured")

        cache_params = {"url": website_url, "audit": "technical"}
        cached_result = cache.get("dataforseo_onpage_audit", cache_params)
        if cached_result:
            return APIResponse(True, cached_result, api_provider="dataforseo", cached=True)

        try:
            # Start on-page audit
            task_data = self._make_request("on_page/task_post", [{
                "target": website_url,
                "max_crawl_pages": 100,
                "load_resources": True,
                "enable_javascript": True,
                "enable_browser_rendering": True
            }])

            # Note: In a real implementation, you'd need to poll for completion
            # For now, return the task ID for later retrieval
            result = {
                "audit_task_id": task_data['tasks'][0]['id'] if task_data.get('tasks') else None,
                "status": "audit_started",
                "timestamp": datetime.now().isoformat()
            }

            cache.set("dataforseo_onpage_audit", cache_params, result)
            return APIResponse(True, result, api_provider="dataforseo")

        except Exception as e:
            return APIResponse(False, {}, f"DataForSEO API error: {str(e)}")

class KeywordsEverywhereClient:
    """Keywords Everywhere API client"""

    def __init__(self):
        self.api_key = os.getenv('KEYWORDS_EVERYWHERE_API_KEY')
        self.base_url = "https://api.keywordseverywhere.com/v1"

    def get_keyword_data(self, keywords: List[str], country: str = "US") -> APIResponse:
        """Get search volume and CPC data for keywords"""
        if not self.api_key:
            return APIResponse(False, {}, "Keywords Everywhere API key not configured")

        cache_params = {"keywords": sorted(keywords), "country": country}
        cached_result = cache.get("keywords_everywhere_data", cache_params)
        if cached_result:
            return APIResponse(True, cached_result, api_provider="keywords_everywhere", cached=True)

        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }

            data = {
                "kw": keywords,
                "country": country,
                "currency": "USD"
            }

            response = requests.post(f"{self.base_url}/get_keyword_data", headers=headers, json=data)
            response.raise_for_status()
            result_data = response.json()

            result = {
                "keyword_data": result_data.get('data', []),
                "credits_used": result_data.get('credits', 0),
                "timestamp": datetime.now().isoformat()
            }

            cache.set("keywords_everywhere_data", cache_params, result)
            return APIResponse(True, result, api_provider="keywords_everywhere")

        except Exception as e:
            return APIResponse(False, {}, f"Keywords Everywhere API error: {str(e)}")

    def get_related_keywords(self, seed_keyword: str, country: str = "US") -> APIResponse:
        """Get related keywords and search volume data"""
        if not self.api_key:
            return APIResponse(False, {}, "Keywords Everywhere API key not configured")

        cache_params = {"seed": seed_keyword, "country": country, "type": "related"}
        cached_result = cache.get("keywords_everywhere_related", cache_params)
        if cached_result:
            return APIResponse(True, cached_result, api_provider="keywords_everywhere", cached=True)

        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }

            data = {
                "kw": seed_keyword,
                "country": country,
                "currency": "USD"
            }

            response = requests.post(f"{self.base_url}/get_related_keywords", headers=headers, json=data)
            response.raise_for_status()
            result_data = response.json()

            result = {
                "related_keywords": result_data.get('data', []),
                "seed_keyword": seed_keyword,
                "timestamp": datetime.now().isoformat()
            }

            cache.set("keywords_everywhere_related", cache_params, result)
            return APIResponse(True, result, api_provider="keywords_everywhere")

        except Exception as e:
            return APIResponse(False, {}, f"Keywords Everywhere API error: {str(e)}")

# Initialize all clients
anthropic_client = AnthropicClient()
openai_client = OpenAIClient()
perplexity_client = PerplexityClient()
dataforseo_client = DataForSEOClient()
keywords_everywhere_client = KeywordsEverywhereClient()

def get_ai_client(provider: str = None):
    """Get AI client based on provider preference or default"""
    if not provider:
        provider = os.getenv('DEFAULT_AI_PROVIDER', 'anthropic')

    clients = {
        'anthropic': anthropic_client,
        'openai': openai_client,
        'perplexity': perplexity_client
    }

    return clients.get(provider, anthropic_client)