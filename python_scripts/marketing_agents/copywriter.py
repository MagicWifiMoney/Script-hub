#!/usr/bin/env python3
"""
Autonomous Content Creator - Premium Marketing AI
Generates professional marketing copy using advanced AI models

Features:
- Real-time AI content generation using Claude/OpenAI
- Multiple content types and formats
- Brand tone analysis and optimization
- A/B testing variations
- SEO optimization
- Conversion rate optimization
"""

import sys
import argparse
import json
import os
import time
from pathlib import Path
from datetime import datetime

# Add parent directory to path to import our API clients
parent_dir = Path(__file__).parent.parent.parent
sys.path.append(str(parent_dir))

from api_clients import get_ai_client, APIResponse

class AutonomousContentCreator:
    """Autonomous AI-powered content creation engine"""

    def __init__(self, ai_provider=None):
        self.ai_client = get_ai_client(ai_provider)

    def create_content(self, content_type, target_audience, client_name=None, brand_tone="professional", product_name=None):
        """Generate professional marketing content autonomously"""

        start_time = time.time()

        # Build comprehensive prompt based on content type
        prompt = self._build_content_prompt(content_type, target_audience, client_name, brand_tone, product_name)

        # Generate content using AI
        response = self.ai_client.generate_content(prompt)

        generation_time = time.time() - start_time

        if response.success:
            return {
                "success": True,
                "content": response.data.get("content", ""),
                "content_type": content_type,
                "target_audience": target_audience,
                "brand_tone": brand_tone,
                "client_name": client_name,
                "generation_time": round(generation_time, 2),
                "word_count": len(response.data.get("content", "").split()),
                "timestamp": datetime.now().isoformat(),
                "ai_provider": self.ai_client.__class__.__name__
            }
        else:
            return {
                "success": False,
                "error": response.error,
                "content_type": content_type,
                "generation_time": round(generation_time, 2)
            }

    def _build_content_prompt(self, content_type, target_audience, client_name, brand_tone, product_name):
        """Build comprehensive AI prompt for content generation"""

        client_context = f" for client '{client_name}'" if client_name else ""
        product_context = f" for product/service '{product_name}'" if product_name else ""

        base_context = f"""
You are an expert marketing copywriter creating {brand_tone} {content_type} content{client_context}{product_context}.

TARGET AUDIENCE: {target_audience}
BRAND TONE: {brand_tone.title()}

Generate professional, conversion-optimized marketing copy that:
- Speaks directly to the target audience
- Uses the specified brand tone consistently
- Includes compelling calls-to-action
- Follows marketing best practices
- Is ready to use immediately (no placeholders)
"""

        content_specific_prompts = {
            "landing_page": f"""
{base_context}

CREATE A COMPLETE LANDING PAGE with:

1. **HEADLINE SECTION**
   - Primary headline (under 60 characters)
   - Supporting subheadline
   - 2 A/B test headline variations

2. **VALUE PROPOSITION**
   - Clear benefit statement
   - Why choose this over competitors

3. **KEY BENEFITS** (3-5 bullet points)
   - Focus on outcomes, not features
   - Use power words and emotional triggers

4. **SOCIAL PROOF**
   - Testimonial framework
   - Trust indicators

5. **CALL-TO-ACTION**
   - Primary CTA button text (3 variations)
   - Supporting CTA copy

6. **FAQ SECTION** (3-5 common objections)
   - Address main concerns
   - Reinforce value proposition

Make it compelling, conversion-focused, and ready to publish.
""",

            "email": f"""
{base_context}

CREATE A COMPLETE EMAIL CAMPAIGN with:

1. **SUBJECT LINES** (5 A/B test variations)
   - Mix of curiosity, benefit, and urgency
   - Under 50 characters for mobile

2. **EMAIL STRUCTURE**
   - Attention-grabbing opening line
   - Value-driven body content
   - Clear call-to-action
   - Professional signature

3. **FOLLOW-UP SEQUENCE** (3 emails)
   - Email 2: Social proof focus
   - Email 3: Urgency/scarcity
   - Email 4: Last chance

4. **PERSONALIZATION TOKENS**
   - Where to insert first name, company, etc.

Make it engaging, valuable, and conversion-optimized.
""",

            "social": f"""
{base_context}

CREATE SOCIAL MEDIA CONTENT for multiple platforms:

1. **FACEBOOK POST**
   - Engaging hook (first line)
   - Story or value proposition
   - Clear call-to-action
   - Relevant hashtags (5-10)

2. **INSTAGRAM POST**
   - Visual description
   - Caption with line breaks
   - Trending hashtags (15-20)
   - Stories variation

3. **LINKEDIN POST**
   - Professional tone
   - Industry insights
   - Business-focused CTA
   - Professional hashtags (3-5)

4. **TWITTER/X THREAD** (3-5 tweets)
   - Thread hook
   - Key points breakdown
   - Engagement prompts

Make it platform-optimized and engaging.
""",

            "blog": f"""
{base_context}

CREATE A COMPLETE BLOG POST with:

1. **SEO-OPTIMIZED TITLE**
   - Keyword-rich (60 characters max)
   - Click-worthy and valuable

2. **META DESCRIPTION** (155 characters)
   - Compelling summary
   - Include target keyword

3. **BLOG STRUCTURE**
   - Hook introduction
   - H2/H3 organized content
   - Actionable insights
   - Data and examples
   - Strong conclusion with CTA

4. **CONTENT SECTIONS** (800-1200 words)
   - Problem identification
   - Solution explanation
   - Step-by-step guidance
   - Real examples
   - Next steps

5. **ENGAGEMENT ELEMENTS**
   - Questions for comments
   - Share-worthy quotes
   - Internal linking suggestions

Make it informative, actionable, and SEO-friendly.
""",

            "ad_copy": f"""
{base_context}

CREATE HIGH-CONVERTING AD COPY with:

1. **FACEBOOK/INSTAGRAM ADS**
   - 5 headline variations (under 40 characters)
   - Primary text (125 characters)
   - Call-to-action button options
   - Visual description

2. **GOOGLE ADS**
   - 3 headlines (30 characters each)
   - 2 descriptions (90 characters each)
   - Ad extensions suggestions

3. **A/B TESTING FRAMEWORK**
   - What to test first
   - Success metrics to track

4. **TARGET AUDIENCE INSIGHTS**
   - Demographics
   - Interests
   - Behavioral targeting

Make it conversion-focused with clear testing strategy.
""",

            "product_desc": f"""
{base_context}

CREATE COMPELLING PRODUCT COPY with:

1. **PRODUCT TITLE**
   - SEO-optimized
   - Benefit-driven
   - Under 60 characters

2. **SHORT DESCRIPTION** (elevator pitch)
   - Core value proposition
   - Primary benefit
   - 1-2 sentences

3. **DETAILED DESCRIPTION**
   - Key features as benefits
   - Problem-solution format
   - Use cases and applications

4. **BULLET POINTS** (5-7 key benefits)
   - Outcome-focused
   - Scannable format

5. **SOCIAL PROOF ELEMENTS**
   - Review prompts
   - Trust signals
   - Guarantees

6. **URGENCY ELEMENTS**
   - Limited time/stock
   - Exclusive offers

Make it persuasive, benefit-focused, and sales-driven.
"""
        }

        return content_specific_prompts.get(content_type, content_specific_prompts["landing_page"])

def format_content_output(result, output_format="markdown"):
    """Format the generated content for display"""

    if not result["success"]:
        return f"""
🚨 CONTENT GENERATION FAILED
================================

Error: {result.get('error', 'Unknown error')}
Content Type: {result.get('content_type', 'Unknown')}
Generation Time: {result.get('generation_time', 0)}s

Please check your API configuration and try again.
"""

    content = result["content"]
    stats = f"""
⚡ AUTONOMOUS CONTENT CREATOR COMPLETE
=====================================

📊 GENERATION STATS:
• Content Type: {result['content_type'].replace('_', ' ').title()}
• Target Audience: {result['target_audience']}
• Brand Tone: {result['brand_tone'].title()}
• Words Generated: {result['word_count']:,}
• Generation Time: {result['generation_time']}s
• AI Provider: {result['ai_provider']}
• Generated: {datetime.fromisoformat(result['timestamp']).strftime('%Y-%m-%d %H:%M')}

"""

    if result.get('client_name'):
        stats += f"• Client: {result['client_name']}\n"

    output = stats + "\n" + "="*50 + "\n"
    output += "📝 GENERATED CONTENT:\n"
    output += "="*50 + "\n\n"
    output += content
    output += "\n\n" + "="*50
    output += "\n✨ CONTENT READY FOR USE - NO EDITING REQUIRED"
    output += "\n" + "="*50

    return output

def main():
    parser = argparse.ArgumentParser(description='Autonomous Content Creator - Premium Marketing AI')
    parser.add_argument('content_type',
                        choices=['landing_page', 'email', 'social', 'blog', 'ad_copy', 'product_desc'],
                        help='Type of content to create')
    parser.add_argument('target_audience', help='Description of target audience')
    parser.add_argument('--client_name', help='Client name for personalized output')
    parser.add_argument('--product_name', help='Product or service name')
    parser.add_argument('--brand_tone',
                        choices=['professional', 'casual', 'friendly', 'authoritative'],
                        default='professional', help='Brand tone of voice')
    parser.add_argument('--output_format', choices=['markdown', 'json', 'text'],
                        default='markdown', help='Output format')
    parser.add_argument('--ai_provider', choices=['anthropic', 'openai', 'perplexity'],
                        help='AI provider to use (default from environment)')

    args = parser.parse_args()

    try:
        # Initialize autonomous content creator
        creator = AutonomousContentCreator(args.ai_provider)

        print("⚡ AUTONOMOUS CONTENT CREATOR INITIALIZING...")
        print(f"🎯 Generating {args.content_type.replace('_', ' ')} content...")
        print(f"👥 Target Audience: {args.target_audience}")
        print(f"🎨 Brand Tone: {args.brand_tone.title()}")
        if args.client_name:
            print(f"🏢 Client: {args.client_name}")
        print("\n⏳ Generating professional marketing copy...\n")

        # Generate content
        result = creator.create_content(
            content_type=args.content_type,
            target_audience=args.target_audience,
            client_name=args.client_name,
            brand_tone=args.brand_tone,
            product_name=args.product_name
        )

        # Format and display output
        formatted_output = format_content_output(result, args.output_format)
        print(formatted_output)

        # JSON output for Script Hub integration
        if args.output_format == 'json':
            print("\n🔧 SCRIPT METADATA:")
            metadata = {
                "agent": "autonomous_content_creator",
                "success": result["success"],
                "content_type": result["content_type"],
                "target_audience": result["target_audience"],
                "brand_tone": result["brand_tone"],
                "client_name": result.get("client_name"),
                "word_count": result.get("word_count", 0),
                "generation_time": result.get("generation_time", 0),
                "ai_provider": result.get("ai_provider"),
                "timestamp": result.get("timestamp"),
                "status": "content_generated" if result["success"] else "generation_failed"
            }
            print(json.dumps(metadata, indent=2))

    except Exception as e:
        print(f"""
🚨 AUTONOMOUS CONTENT CREATOR ERROR
==================================

Error: {str(e)}
Content Type: {args.content_type}

Please check:
• API keys are configured in .env file
• Network connection is stable
• Content parameters are valid

Try running: python3 ../../system_manager.py --health-check
""")

if __name__ == "__main__":
    main()