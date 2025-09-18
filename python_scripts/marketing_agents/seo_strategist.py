#!/usr/bin/env python3
"""
SEO Strategist Marketing Agent
Script Hub Integration - Marketing Category

Usage:
- website_url: Website to analyze
- analysis_type: quick, comprehensive, technical, or local (default: quick)
- client_name: Optional client name for personalized output
"""

import sys
import os
import json
import argparse
from pathlib import Path

# Add the parent directory to path to access prompts
script_dir = Path(__file__).parent
project_root = script_dir.parent
prompts_dir = project_root / "prompts"

def load_agent_prompt(prompt_file="seo-strategist.md"):
    """Load the SEO strategist prompt template"""
    prompt_path = prompts_dir / prompt_file
    if prompt_path.exists():
        with open(prompt_path, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        return """
# SEO Strategist Agent
You are an expert SEO strategist. Analyze the provided website and provide actionable recommendations.

## Analysis Framework:
1. Technical SEO Assessment
2. On-Page Optimization
3. Content Strategy
4. Local SEO (if applicable)
5. Competitive Analysis
6. Priority Action Items
"""

def format_seo_analysis(website_url, analysis_type, client_name=None):
    """Format the SEO analysis request"""

    client_prefix = f"[Client: {client_name}] " if client_name else ""

    analysis_templates = {
        "quick": """
🔍 QUICK SEO ANALYSIS REQUEST

{client_prefix}Website: {website_url}

Please provide:
1. 🏠 Homepage SEO Score (0-100)
2. 🔧 Top 3 Technical Issues
3. 📝 Content Opportunities (3 items)
4. 🎯 Priority Keywords (5 suggestions)
5. ⚡ Quick Wins (3 actionable items)
""",
        "comprehensive": """
🔍 COMPREHENSIVE SEO AUDIT REQUEST

{client_prefix}Website: {website_url}

Please provide detailed analysis:
1. 🏗️ Technical SEO Audit (Core Web Vitals, crawlability, indexing)
2. 📊 On-Page Analysis (titles, meta, headers, content)
3. 🌐 Local SEO Assessment (if applicable)
4. 🔗 Backlink Profile Overview
5. 📱 Mobile Experience Review
6. 🎯 Keyword Strategy (primary & secondary)
7. 🏆 Competitive Analysis (top 3 competitors)
8. 📋 30-Day Action Plan (prioritized)
""",
        "technical": """
🔧 TECHNICAL SEO ANALYSIS REQUEST

{client_prefix}Website: {website_url}

Focus on technical aspects:
1. ⚡ Site Speed & Core Web Vitals
2. 🏗️ Site Architecture & URL Structure
3. 📱 Mobile Responsiveness
4. 🔍 Crawlability & Indexing
5. 📊 Schema Markup Opportunities
6. 🛡️ Security (HTTPS, redirects)
7. 🔧 Technical Quick Fixes
""",
        "local": """
📍 LOCAL SEO ANALYSIS REQUEST

{client_prefix}Website: {website_url}

Focus on local search optimization:
1. 🎯 Google My Business Optimization
2. 📍 Local Citation Audit
3. ⭐ Review Management Strategy
4. 🌐 Local Keyword Opportunities
5. 📱 Mobile Local Experience
6. 🏪 Local Competition Analysis
7. 📋 Local SEO Action Plan
"""
    }

    template = analysis_templates.get(analysis_type, analysis_templates["quick"])
    return template.format(
        client_prefix=client_prefix,
        website_url=website_url
    )

def main():
    parser = argparse.ArgumentParser(description='SEO Strategist Marketing Agent')
    parser.add_argument('website_url', help='Website URL to analyze')
    parser.add_argument('--analysis_type', choices=['quick', 'comprehensive', 'technical', 'local'],
                        default='quick', help='Type of SEO analysis')
    parser.add_argument('--client_name', help='Client name for personalized output')
    parser.add_argument('--output_format', choices=['markdown', 'json', 'text'],
                        default='markdown', help='Output format')

    args = parser.parse_args()

    # Load the agent prompt (for future AI integration)
    agent_prompt = load_agent_prompt()

    # Generate analysis request
    analysis_request = format_seo_analysis(
        args.website_url,
        args.analysis_type,
        args.client_name
    )

    # For now, output the structured analysis request
    # In production, this would be sent to Claude/OpenAI API
    print("=" * 60)
    print("🎯 SEO STRATEGIST AGENT ACTIVATED")
    print("=" * 60)
    print()
    print(analysis_request)
    print()
    print("=" * 60)
    print("📋 NEXT STEPS:")
    print("1. Copy this analysis request to your AI assistant (Claude/ChatGPT)")
    print("2. Paste the AI response into Script Hub for further processing")
    print("3. Use the report generation tools for client deliverables")
    print("=" * 60)

    # Output metadata for Script Hub
    metadata = {
        "agent": "seo_strategist",
        "website": args.website_url,
        "analysis_type": args.analysis_type,
        "client": args.client_name,
        "timestamp": "2024-01-01",  # In production, use actual timestamp
        "status": "analysis_ready"
    }

    if args.output_format == 'json':
        print("\n🔧 SCRIPT METADATA:")
        print(json.dumps(metadata, indent=2))

if __name__ == "__main__":
    main()