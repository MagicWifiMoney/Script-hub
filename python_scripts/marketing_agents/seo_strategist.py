#!/usr/bin/env python3
"""
Autonomous SEO Strategist Marketing Agent
Script Hub Integration - Marketing Category

Provides real-time SEO analysis using multiple APIs:
- DataForSEO for technical analysis
- Keywords Everywhere for keyword data
- Claude/ChatGPT/Perplexity for AI insights

Usage:
- website_url: Website to analyze
- analysis_type: quick, comprehensive, technical, or local (default: quick)
- client_name: Optional client name for personalized output
- ai_provider: AI provider (anthropic, openai, perplexity) - optional
"""

import sys
import os
import json
import argparse
import time
from pathlib import Path
from datetime import datetime

# Add the parent directory to path to access analysis engine
script_dir = Path(__file__).parent
project_root = script_dir.parent.parent  # Go up two levels to reach Script-hub root
sys.path.append(str(project_root))

try:
    from seo_analysis_engine import analyze_website_seo
except ImportError as e:
    print(f"❌ Error: Could not import SEO analysis engine: {e}")
    print("Make sure you have set up your .env file with API keys.")
    sys.exit(1)

def format_seo_results_for_display(results: dict) -> str:
    """Format SEO analysis results for user-friendly display"""
    output = []

    # Header
    output.append("=" * 70)
    output.append("🎯 AUTONOMOUS SEO ANALYSIS COMPLETE")
    output.append("=" * 70)
    output.append("")

    # Basic info
    client_info = f"Client: {results.get('client_name', 'N/A')}" if results.get('client_name') else ""
    output.append(f"🌐 Website: {results.get('website_url', 'N/A')}")
    if client_info:
        output.append(f"👤 {client_info}")
    output.append(f"📊 Analysis Type: {results.get('analysis_type', 'N/A').title()}")
    output.append(f"⏱️  Analysis Duration: {results.get('analysis_duration', 'N/A')}s")
    output.append(f"🕒 Timestamp: {results.get('timestamp', 'N/A')}")
    output.append("")

    # SEO Score
    seo_score = results.get('seo_score')
    if seo_score is not None:
        score_emoji = "🟢" if seo_score >= 80 else "🟡" if seo_score >= 60 else "🔴"
        output.append(f"📈 SEO SCORE: {score_emoji} {seo_score}/100")
        output.append("")

    # Technical Data Summary
    basic_data = results.get('technical_data', {}).get('basic', {})
    if basic_data:
        output.append("🔧 QUICK TECHNICAL OVERVIEW:")
        output.append(f"   ✅ HTTPS: {'Yes' if basic_data.get('https') else 'No'}")
        output.append(f"   ✅ Mobile Friendly: {'Yes' if basic_data.get('responsive') else 'No'}")
        output.append(f"   ⚡ Load Time: {basic_data.get('load_time', 'N/A')}s")
        output.append(f"   📄 Page Title: {'Present' if basic_data.get('title') else 'Missing'}")
        output.append(f"   📝 Meta Description: {'Present' if basic_data.get('meta_description') else 'Missing'}")
        output.append("")

    # AI Analysis
    if results.get('analysis'):
        output.append("🤖 AI-POWERED ANALYSIS:")
        output.append(results['analysis'])
        output.append("")

    # Recommendations
    recommendations = results.get('recommendations', [])
    if recommendations:
        output.append("⚡ PRIORITY RECOMMENDATIONS:")
        for i, rec in enumerate(recommendations[:8], 1):  # Show top 8
            priority_emoji = "🚨" if rec.get('priority') == 'High' else "⚠️" if rec.get('priority') == 'Medium' else "ℹ️"
            output.append(f"{i}. {priority_emoji} [{rec.get('category', 'General')}] {rec.get('recommendation', 'N/A')}")
            output.append(f"   Impact: {rec.get('impact', 'N/A')}")
            output.append("")

    # Keyword Opportunities
    keyword_data = results.get('keyword_data', {})
    opportunities = keyword_data.get('opportunities', [])
    if opportunities:
        output.append("🎯 KEYWORD OPPORTUNITIES:")
        for kw in opportunities[:5]:  # Show top 5
            if isinstance(kw, dict):
                kw_name = kw.get('keyword', kw.get('kw', 'Unknown'))
                volume = kw.get('vol', kw.get('search_volume', 'N/A'))
                output.append(f"   • {kw_name} (Volume: {volume})")
        output.append("")

    # Data Sources
    if results.get('technical_data'):
        sources = []
        if 'dataforseo_domain' in results['technical_data']:
            sources.append("DataForSEO")
        if keyword_data:
            sources.append("Keywords Everywhere")
        if results.get('competitive_data'):
            sources.append("Perplexity")
        if results.get('analysis'):
            sources.append("Claude AI")

        if sources:
            output.append(f"📡 Data Sources: {', '.join(sources)}")
            output.append("")

    # Errors (if any)
    errors = results.get('errors', [])
    if errors:
        output.append("⚠️ ANALYSIS WARNINGS:")
        for error in errors:
            output.append(f"   • {error}")
        output.append("")

    # Footer
    output.append("=" * 70)
    output.append("🎉 ANALYSIS COMPLETE - Results ready for action!")
    output.append("💡 Use these insights to improve your website's SEO performance.")
    output.append("=" * 70)

    return "\n".join(output)

def save_analysis_results(results: dict, output_dir: str = "seo_reports") -> str:
    """Save analysis results to JSON file for later use"""
    try:
        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)

        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        domain = results.get('website_url', 'unknown').replace('https://', '').replace('http://', '').split('/')[0]
        filename = f"seo_analysis_{domain}_{timestamp}.json"

        # Save results
        filepath = output_path / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        return str(filepath)
    except Exception as e:
        return f"Error saving results: {e}"

def main():
    parser = argparse.ArgumentParser(description='Autonomous SEO Strategist Marketing Agent')
    parser.add_argument('website_url', help='Website URL to analyze')
    parser.add_argument('--analysis_type', choices=['quick', 'comprehensive', 'technical', 'local'],
                        default='quick', help='Type of SEO analysis')
    parser.add_argument('--client_name', help='Client name for personalized output')
    parser.add_argument('--ai_provider', choices=['anthropic', 'openai', 'perplexity'],
                        help='AI provider for analysis (default from .env)')
    parser.add_argument('--output_format', choices=['display', 'json', 'save'],
                        default='display', help='Output format')
    parser.add_argument('--save_results', action='store_true',
                        help='Save results to JSON file')

    args = parser.parse_args()

    # Show startup message
    print("🚀 AUTONOMOUS SEO STRATEGIST STARTING...")
    print(f"🌐 Analyzing: {args.website_url}")
    print(f"📊 Analysis Type: {args.analysis_type.title()}")

    if args.client_name:
        print(f"👤 Client: {args.client_name}")

    print("⏳ This may take 30-60 seconds for comprehensive analysis...")
    print()

    try:
        # Run the autonomous SEO analysis
        start_time = time.time()

        results = analyze_website_seo(
            website_url=args.website_url,
            analysis_type=args.analysis_type,
            client_name=args.client_name,
            ai_provider=args.ai_provider
        )

        analysis_time = time.time() - start_time

        # Handle different output formats
        if args.output_format == 'json':
            print(json.dumps(results, indent=2, ensure_ascii=False))
        elif args.output_format == 'save' or args.save_results:
            # Save to file and display summary
            filepath = save_analysis_results(results)
            print(f"✅ Results saved to: {filepath}")
            print()
            # Also show summary
            print(format_seo_results_for_display(results))
        else:
            # Default display format
            print(format_seo_results_for_display(results))

        # Show success message
        print(f"\n✅ Analysis completed successfully in {analysis_time:.1f} seconds!")

        # Show data sources used
        if results.get('technical_data') or results.get('keyword_data'):
            print("\n📊 Real data collected from:")
            if results.get('technical_data', {}).get('basic'):
                print("   • Website crawling and technical analysis")
            if 'dataforseo' in str(results.get('technical_data', {})):
                print("   • DataForSEO API (domain authority, backlinks)")
            if results.get('keyword_data'):
                print("   • Keywords Everywhere API (search volume, competition)")
            if results.get('competitive_data'):
                print("   • Perplexity AI (competitive analysis)")
            if results.get('analysis'):
                ai_provider = args.ai_provider or os.getenv('DEFAULT_AI_PROVIDER', 'Claude')
                print(f"   • {ai_provider.title()} AI (insights and recommendations)")

    except KeyboardInterrupt:
        print("\n❌ Analysis interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Analysis failed: {str(e)}")
        print("\n🔧 Troubleshooting:")
        print("1. Check your .env file has the required API keys")
        print("2. Verify the website URL is accessible")
        print("3. Ensure you have an internet connection")
        print("4. Check API rate limits and quotas")
        sys.exit(1)

if __name__ == "__main__":
    main()