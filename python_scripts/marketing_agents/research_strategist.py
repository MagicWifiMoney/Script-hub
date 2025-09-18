#!/usr/bin/env python3
"""
Research Strategist Marketing Agent
Script Hub Integration - Marketing Category

Usage:
- research_type: competitive, market, audience, keyword, or industry
- target_subject: Company, industry, or keyword to research
- client_name: Optional client name
- depth: quick, standard, or comprehensive (default: standard)
"""

import sys
import argparse
import json
from pathlib import Path

def format_research_request(research_type, target_subject, client_name=None, depth="standard"):
    """Format the research analysis request"""

    client_prefix = f"[Client: {client_name}] " if client_name else ""

    research_templates = {
        "competitive": """
🔍 COMPETITIVE ANALYSIS REQUEST

{client_prefix}Target Subject: {target_subject}
Research Depth: {depth}

Please provide competitive intelligence:
1. 🏆 Top 5 Direct Competitors
2. 💰 Pricing Strategy Analysis
3. 🎯 Marketing Positioning Comparison
4. 📊 Traffic & SEO Performance
5. 📱 Social Media Presence
6. 🎨 Brand Messaging Analysis
7. ⚡ Strengths & Weaknesses
8. 🚀 Market Opportunities
9. 📋 Competitive Action Plan
""",
        "market": """
📊 MARKET ANALYSIS REQUEST

{client_prefix}Target Subject: {target_subject}
Research Depth: {depth}

Please provide market research:
1. 📈 Market Size & Growth Trends
2. 🎯 Target Audience Segments
3. 💡 Industry Pain Points
4. 🔄 Market Dynamics & Forces
5. 📱 Technology Trends
6. 💰 Pricing Benchmarks
7. 🏆 Key Success Factors
8. 🚀 Emerging Opportunities
9. ⚠️  Market Threats & Challenges
""",
        "audience": """
👥 AUDIENCE RESEARCH REQUEST

{client_prefix}Target Subject: {target_subject}
Research Depth: {depth}

Please provide audience insights:
1. 📊 Demographic Breakdown
2. 💭 Psychographic Profiles
3. 🎯 Pain Points & Challenges
4. 💰 Buying Behavior Patterns
5. 📱 Preferred Communication Channels
6. 🔍 Search Behavior & Intent
7. 📚 Content Consumption Habits
8. 🏆 Decision-Making Factors
9. 📋 Audience Persona Templates
""",
        "keyword": """
🔑 KEYWORD RESEARCH REQUEST

{client_prefix}Target Subject: {target_subject}
Research Depth: {depth}

Please provide keyword analysis:
1. 🎯 Primary Keyword Opportunities (10-15)
2. 📊 Search Volume & Difficulty Scores
3. 🔄 Long-tail Keyword Variations
4. 💡 Search Intent Analysis
5. 🏆 Competitor Keyword Gaps
6. 📅 Seasonal Keyword Trends
7. 📱 Local vs Global Opportunities
8. 🔍 Question-based Keywords
9. 📋 Content Topic Clusters
""",
        "industry": """
🏭 INDUSTRY ANALYSIS REQUEST

{client_prefix}Target Subject: {target_subject}
Research Depth: {depth}

Please provide industry research:
1. 📈 Industry Overview & Size
2. 🔄 Key Trends & Disruptions
3. 🏆 Major Players & Market Share
4. 💰 Revenue Models & Pricing
5. 📊 Customer Behavior Shifts
6. 🚀 Innovation & Technology Impact
7. ⚖️  Regulatory Environment
8. 🌍 Geographic Considerations
9. 📋 Strategic Recommendations
"""
    }

    template = research_templates.get(research_type, research_templates["competitive"])
    return template.format(
        client_prefix=client_prefix,
        target_subject=target_subject,
        depth=depth.title()
    )

def main():
    parser = argparse.ArgumentParser(description='Research Strategist Marketing Agent')
    parser.add_argument('research_type',
                        choices=['competitive', 'market', 'audience', 'keyword', 'industry'],
                        help='Type of research to conduct')
    parser.add_argument('target_subject', help='Subject to research (company, industry, keyword)')
    parser.add_argument('--client_name', help='Client name for personalized output')
    parser.add_argument('--depth',
                        choices=['quick', 'standard', 'comprehensive'],
                        default='standard', help='Research depth level')
    parser.add_argument('--output_format', choices=['markdown', 'json', 'text'],
                        default='markdown', help='Output format')

    args = parser.parse_args()

    # Generate research request
    research_request = format_research_request(
        args.research_type,
        args.target_subject,
        args.client_name,
        args.depth
    )

    # Output the structured research request
    print("=" * 60)
    print("🔍 RESEARCH STRATEGIST AGENT ACTIVATED")
    print("=" * 60)
    print()
    print(research_request)
    print()
    print("=" * 60)
    print("📚 RESEARCH BEST PRACTICES:")
    print("• Verify information from multiple sources")
    print("• Look for recent data (within 12 months)")
    print("• Focus on actionable insights")
    print("• Consider seasonal variations")
    print("• Document information sources")
    print("• Create visual summaries when possible")
    print("=" * 60)

    # Output metadata for Script Hub
    metadata = {
        "agent": "research_strategist",
        "research_type": args.research_type,
        "target_subject": args.target_subject,
        "depth": args.depth,
        "client": args.client_name,
        "timestamp": "2024-01-01",
        "status": "research_brief_ready"
    }

    if args.output_format == 'json':
        print("\n🔧 SCRIPT METADATA:")
        print(json.dumps(metadata, indent=2))

if __name__ == "__main__":
    main()