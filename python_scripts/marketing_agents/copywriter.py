#!/usr/bin/env python3
"""
Copywriter Marketing Agent
Script Hub Integration - Marketing Category

Usage:
- content_type: landing_page, email, social, blog, ad_copy, or product_desc
- target_audience: Brief description of target audience
- client_name: Optional client name
- brand_tone: professional, casual, friendly, authoritative (default: professional)
"""

import sys
import argparse
import json
from pathlib import Path

def format_copy_request(content_type, target_audience, client_name=None, brand_tone="professional"):
    """Format the copywriting request"""

    client_prefix = f"[Client: {client_name}] " if client_name else ""

    copy_templates = {
        "landing_page": """
📝 LANDING PAGE COPY REQUEST

{client_prefix}Target Audience: {target_audience}
Brand Tone: {brand_tone}

Please create:
1. 🎯 Compelling Headline (A/B test variations)
2. 💡 Value Proposition (clear & concise)
3. 📋 Key Benefits (3-5 bullet points)
4. 🎨 Feature Descriptions (with benefits)
5. 🏆 Social Proof Section (testimonial framework)
6. 📞 Call-to-Action (multiple variations)
7. ❓ FAQ Section (address objections)
8. 🔥 Urgency/Scarcity Elements
""",
        "email": """
📧 EMAIL CAMPAIGN COPY REQUEST

{client_prefix}Target Audience: {target_audience}
Brand Tone: {brand_tone}

Please create email sequence:
1. 📬 Subject Lines (5 variations for A/B testing)
2. 🎯 Opening Hook (grab attention first 2 lines)
3. 📖 Email Body (value-first approach)
4. 🔗 Clear Call-to-Action
5. 📱 Mobile-Optimized Format
6. 🎨 Personalization Opportunities
7. 📈 Follow-up Sequence (3-email series)
""",
        "social": """
📱 SOCIAL MEDIA COPY REQUEST

{client_prefix}Target Audience: {target_audience}
Brand Tone: {brand_tone}

Please create social content:
1. 📊 Platform-Specific Posts (Facebook, Instagram, LinkedIn, Twitter)
2. #️⃣ Relevant Hashtag Strategy (10-15 hashtags per platform)
3. 🎨 Caption Variations (short, medium, long)
4. 📞 Call-to-Action Options
5. 🔄 Engagement Questions
6. 📅 Content Calendar Framework (7 days)
7. 📸 Visual Content Descriptions
""",
        "blog": """
📚 BLOG CONTENT REQUEST

{client_prefix}Target Audience: {target_audience}
Brand Tone: {brand_tone}

Please create blog structure:
1. 🎯 SEO-Optimized Title (with keyword focus)
2. 📖 Compelling Introduction (hook + value promise)
3. 📋 Detailed Outline (H2/H3 structure)
4. 💡 Key Points & Takeaways
5. 📊 Data/Statistics Integration
6. 🔗 Internal Linking Opportunities
7. 📞 Clear Call-to-Action
8. 📱 Meta Description (155 characters)
""",
        "ad_copy": """
🎯 ADVERTISING COPY REQUEST

{client_prefix}Target Audience: {target_audience}
Brand Tone: {brand_tone}

Please create ad variations:
1. 📢 Headlines (5 variations for testing)
2. 📝 Primary Text (Facebook/Google Ads)
3. 📞 Call-to-Action Text (multiple options)
4. 🎨 Visual Description/Requirements
5. 🎯 Targeting Suggestions
6. 📊 A/B Testing Framework
7. 📈 Conversion Optimization Tips
""",
        "product_desc": """
🛍️ PRODUCT DESCRIPTION REQUEST

{client_prefix}Target Audience: {target_audience}
Brand Tone: {brand_tone}

Please create product copy:
1. 🎯 Product Title (SEO + conversion optimized)
2. 📝 Short Description (elevator pitch)
3. 📋 Detailed Features & Benefits
4. 🏆 Unique Selling Proposition
5. 📊 Technical Specifications (user-friendly)
6. ❓ FAQ Section (common concerns)
7. 🔥 Urgency/Scarcity Elements
8. 📱 Mobile-Optimized Format
"""
    }

    template = copy_templates.get(content_type, copy_templates["landing_page"])
    return template.format(
        client_prefix=client_prefix,
        target_audience=target_audience,
        brand_tone=brand_tone.title()
    )

def main():
    parser = argparse.ArgumentParser(description='Copywriter Marketing Agent')
    parser.add_argument('content_type',
                        choices=['landing_page', 'email', 'social', 'blog', 'ad_copy', 'product_desc'],
                        help='Type of content to create')
    parser.add_argument('target_audience', help='Description of target audience')
    parser.add_argument('--client_name', help='Client name for personalized output')
    parser.add_argument('--brand_tone',
                        choices=['professional', 'casual', 'friendly', 'authoritative'],
                        default='professional', help='Brand tone of voice')
    parser.add_argument('--output_format', choices=['markdown', 'json', 'text'],
                        default='markdown', help='Output format')

    args = parser.parse_args()

    # Generate copy request
    copy_request = format_copy_request(
        args.content_type,
        args.target_audience,
        args.client_name,
        args.brand_tone
    )

    # Output the structured copy request
    print("=" * 60)
    print("✍️  COPYWRITER AGENT ACTIVATED")
    print("=" * 60)
    print()
    print(copy_request)
    print()
    print("=" * 60)
    print("📋 COPY OPTIMIZATION TIPS:")
    print("• Test multiple headline variations")
    print("• Focus on benefits over features")
    print("• Use power words and emotional triggers")
    print("• Include social proof elements")
    print("• Create urgency without being pushy")
    print("• Optimize for mobile readability")
    print("=" * 60)

    # Output metadata for Script Hub
    metadata = {
        "agent": "copywriter",
        "content_type": args.content_type,
        "target_audience": args.target_audience,
        "brand_tone": args.brand_tone,
        "client": args.client_name,
        "timestamp": "2024-01-01",
        "status": "copy_brief_ready"
    }

    if args.output_format == 'json':
        print("\n🔧 SCRIPT METADATA:")
        print(json.dumps(metadata, indent=2))

if __name__ == "__main__":
    main()