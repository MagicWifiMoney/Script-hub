"""
Marketing Tools Helper Module
Provides user-friendly interface enhancements for marketing tools
"""

import json
import os
import streamlit as st
from pathlib import Path

def load_marketing_catalog():
    """Load the marketing tools catalog with descriptions"""
    catalog_path = Path(__file__).parent / "marketing_catalog.json"
    if catalog_path.exists():
        with open(catalog_path, 'r') as f:
            return json.load(f)
    return {}

def get_script_info(script_path):
    """Get user-friendly information about a script"""
    catalog = load_marketing_catalog()
    script_name = os.path.basename(script_path)

    # Check all categories for the script
    for category_name, scripts in catalog.items():
        if script_name in scripts:
            return scripts[script_name]

    # Default fallback for unknown scripts
    return {
        "name": script_name.replace('.py', '').replace('_', ' ').title(),
        "description": "Python script for automation",
        "status": "❓ Unknown",
        "category": "Other"
    }

def display_marketing_tool_card(script_path, script_info):
    """Display a user-friendly card for a marketing tool"""

    # Create an expandable card
    with st.expander(f"{script_info.get('name', 'Unknown Tool')} - {script_info.get('status', '❓')}"):

        # Basic info
        st.markdown(f"**Category:** {script_info.get('category', 'Other')}")
        st.markdown(f"**What it does:** {script_info.get('description', 'No description available')}")

        if 'what_it_does' in script_info:
            st.markdown(f"**Details:** {script_info['what_it_does']}")

        if 'perfect_for' in script_info:
            st.markdown(f"💡 **Perfect for:** {script_info['perfect_for']}")

        if 'example_use' in script_info:
            st.markdown(f"📝 **Example:** {script_info['example_use']}")

        if 'time_to_complete' in script_info:
            st.markdown(f"⏱️ **Time:** {script_info['time_to_complete']}")

        # Setup notes if any
        if script_info.get('setup_note'):
            st.warning(f"ℹ️ {script_info['setup_note']}")

        # Next steps
        if 'next_steps' in script_info:
            st.markdown(f"**Next steps:** {script_info['next_steps']}")

def create_guided_form(script_path, script_info):
    """Create user-friendly form for script parameters"""

    if 'inputs_needed' not in script_info:
        # Fall back to simple input for scripts without guided forms
        return st.text_input("Parameters:", placeholder="Enter any parameters needed")

    positional_params = []
    optional_params = []
    inputs = script_info['inputs_needed']

    st.markdown("### 📋 Fill out these details:")

    for input_name, input_config in inputs.items():
        label = input_config.get('label', input_name.replace('_', ' ').title())
        help_text = input_config.get('help', '')
        arg_type = input_config.get('argument_type', 'optional')  # Default to optional for backwards compatibility

        # Handle different input types
        if 'options' in input_config:
            # Dropdown/radio selection
            options_list = input_config['options']
            if isinstance(options_list[0], dict):
                # Complex options with descriptions
                option_labels = [f"{opt['label']}" + (f" - {opt['description']}" if 'description' in opt else "") for opt in options_list]
                selected_index = st.selectbox(
                    label,
                    range(len(option_labels)),
                    format_func=lambda x: option_labels[x],
                    help=help_text
                )
                selected_value = options_list[selected_index]['value']
            else:
                # Simple options
                selected_value = st.selectbox(label, options_list, help=help_text)

            # Add to appropriate parameter list based on argument type
            if arg_type == "positional":
                positional_params.append(selected_value)
            else:
                optional_params.append(f"--{input_name} {selected_value}")

        else:
            # Text input
            placeholder = input_config.get('placeholder', '')
            required = input_config.get('required', False)
            value = st.text_input(label, placeholder=placeholder, help=help_text)

            if value or required:  # Include if value provided or if required
                if arg_type == "positional":
                    positional_params.append(f'"{value}"' if value else '""')
                else:
                    if value:  # Only add optional params if they have values
                        optional_params.append(f"--{input_name} \"{value}\"")

    # Combine positional arguments first, then optional arguments
    all_params = positional_params + optional_params
    return " ".join(all_params)

def show_marketing_tutorial():
    """Display marketing tools tutorial"""
    st.markdown("## 🎯 Welcome to Your Marketing Automation Hub!")

    st.markdown("""
    **New to marketing tools?** No problem! Here's what you can do:

    ### 🔍 **Start Here - SEO Strategist**
    Perfect first tool - analyzes your website for Google ranking improvements.
    Just enter your website URL and get actionable SEO recommendations.

    ### ✍️ **Content Creator**
    Stuck on what to write? This creates detailed briefs for any marketing content.
    Great for website copy, emails, social media posts, and more.

    ### 📊 **Market Researcher**
    Want to understand your competition? This tool creates research frameworks
    to analyze competitors and find market opportunities.

    ### 💡 **Campaign Creator**
    Need fresh marketing ideas? Get creative campaign concepts tailored
    to your audience and budget.
    """)

    st.info("💡 **Pro Tip:** All outputs work perfectly with ChatGPT or Claude. Just copy and paste for detailed AI recommendations!")

    if st.button("📖 View Complete User Guide"):
        st.markdown("*User guide will be displayed here*")

def display_success_stories():
    """Show example success stories and use cases"""
    st.markdown("## 🎉 Success Stories")

    stories = [
        {
            "title": "Local Restaurant Doubled Website Traffic",
            "tool": "SEO Strategist",
            "result": "Found 15 local SEO improvements, implemented top 5, saw 120% traffic increase in 3 months",
            "tip": "Focus on Google My Business optimization for local businesses"
        },
        {
            "title": "E-commerce Store Improved Conversion Rate by 40%",
            "tool": "Conversion Optimizer",
            "result": "Optimized checkout process, reduced cart abandonment from 70% to 42%",
            "tip": "Test one change at a time to see what really works"
        },
        {
            "title": "SaaS Company Generated 300 New Leads",
            "tool": "Content Creator + Campaign Creator",
            "result": "Created lead magnet content and promotional campaign, 3x lead generation",
            "tip": "Combine multiple tools for compound results"
        }
    ]

    for story in stories:
        with st.expander(f"📈 {story['title']} (using {story['tool']})"):
            st.markdown(f"**Result:** {story['result']}")
            st.markdown(f"💡 **Tip:** {story['tip']}")

def display_seo_analysis_results(output_text: str):
    """Parse and display SEO analysis results in a rich format"""

    # Check if this looks like JSON output
    try:
        if output_text.strip().startswith('{'):
            results = json.loads(output_text)
            _display_structured_seo_results(results)
            return
    except:
        pass

    # Parse text output for key information
    lines = output_text.split('\n')

    # Look for key sections in the output
    seo_score = None
    for line in lines:
        if 'SEO SCORE:' in line:
            # Extract score
            try:
                import re
                score_match = re.search(r'(\d+)/100', line)
                if score_match:
                    seo_score = int(score_match.group(1))
            except:
                pass
            break

    # Display SEO score prominently if found
    if seo_score is not None:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if seo_score >= 80:
                st.success(f"🟢 SEO Score: {seo_score}/100")
            elif seo_score >= 60:
                st.warning(f"🟡 SEO Score: {seo_score}/100")
            else:
                st.error(f"🔴 SEO Score: {seo_score}/100")

    # Display the full output with syntax highlighting
    st.markdown("### 📊 Complete Analysis Results")

    # Check if it's a structured analysis
    if "AUTONOMOUS SEO ANALYSIS COMPLETE" in output_text:
        # It's our structured output, display with better formatting
        st.code(output_text, language='text')

        # Add download button for results
        st.download_button(
            label="📥 Download Analysis Report",
            data=output_text,
            file_name=f"seo_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )

        # Show data sources if available
        if "Real data collected from:" in output_text:
            st.success("✅ This analysis used real data from multiple APIs!")
            with st.expander("ℹ️ About the Data Sources"):
                st.markdown("""
                This autonomous SEO analysis collected real data from:
                - **Website crawling**: Technical analysis of your site
                - **DataForSEO API**: Domain authority and backlink data
                - **Keywords Everywhere API**: Search volume and keyword competition
                - **AI Analysis**: Claude/ChatGPT for insights and recommendations

                This is much more accurate than generic SEO advice!
                """)
    else:
        # Standard output display
        st.code(output_text, language='text')

def _display_structured_seo_results(results: dict):
    """Display structured SEO results from JSON"""
    from datetime import datetime

    st.markdown("## 🎯 SEO Analysis Results")

    # Basic info
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Website", results.get('website_url', 'N/A'))
        st.metric("Analysis Type", results.get('analysis_type', 'N/A').title())
    with col2:
        if results.get('client_name'):
            st.metric("Client", results['client_name'])
        st.metric("Analysis Duration", f"{results.get('analysis_duration', 'N/A')}s")

    # SEO Score
    seo_score = results.get('seo_score')
    if seo_score is not None:
        if seo_score >= 80:
            st.success(f"🟢 Excellent SEO Score: {seo_score}/100")
        elif seo_score >= 60:
            st.warning(f"🟡 Good SEO Score: {seo_score}/100")
        else:
            st.error(f"🔴 Needs Improvement: {seo_score}/100")

    # Technical overview
    basic_data = results.get('technical_data', {}).get('basic', {})
    if basic_data:
        st.markdown("### 🔧 Technical Overview")

        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            https_status = "✅" if basic_data.get('https') else "❌"
            st.metric("HTTPS", https_status)
        with col2:
            mobile_status = "✅" if basic_data.get('responsive') else "❌"
            st.metric("Mobile", mobile_status)
        with col3:
            load_time = basic_data.get('load_time', 0)
            st.metric("Load Time", f"{load_time}s")
        with col4:
            title_status = "✅" if basic_data.get('title') else "❌"
            st.metric("Title", title_status)
        with col5:
            desc_status = "✅" if basic_data.get('meta_description') else "❌"
            st.metric("Meta Desc", desc_status)

    # AI Analysis
    if results.get('analysis'):
        st.markdown("### 🤖 AI Analysis")
        st.markdown(results['analysis'])

    # Recommendations
    recommendations = results.get('recommendations', [])
    if recommendations:
        st.markdown("### ⚡ Priority Recommendations")

        for i, rec in enumerate(recommendations[:6], 1):
            priority = rec.get('priority', 'Medium')
            if priority == 'High':
                st.error(f"**{i}. [{rec.get('category', 'General')}]** {rec.get('recommendation', 'N/A')}")
            elif priority == 'Medium':
                st.warning(f"**{i}. [{rec.get('category', 'General')}]** {rec.get('recommendation', 'N/A')}")
            else:
                st.info(f"**{i}. [{rec.get('category', 'General')}]** {rec.get('recommendation', 'N/A')}")

            if rec.get('impact'):
                st.caption(f"Impact: {rec['impact']}")

    # Keyword opportunities
    keyword_data = results.get('keyword_data', {})
    opportunities = keyword_data.get('opportunities', [])
    if opportunities:
        st.markdown("### 🎯 Keyword Opportunities")

        for kw in opportunities[:5]:
            if isinstance(kw, dict):
                kw_name = kw.get('keyword', kw.get('kw', 'Unknown'))
                volume = kw.get('vol', kw.get('search_volume', 'N/A'))
                st.markdown(f"• **{kw_name}** (Volume: {volume})")

    # Download options
    st.markdown("### 📥 Export Options")
    col1, col2 = st.columns(2)

    with col1:
        st.download_button(
            label="📊 Download JSON Report",
            data=json.dumps(results, indent=2),
            file_name=f"seo_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )

    with col2:
        # Create text summary
        summary = f"""
SEO Analysis Report
==================
Website: {results.get('website_url', 'N/A')}
SEO Score: {results.get('seo_score', 'N/A')}/100
Analysis Date: {results.get('timestamp', 'N/A')}

Key Recommendations:
{chr(10).join([f"• {rec.get('recommendation', 'N/A')}" for rec in recommendations[:5]])}
"""
        st.download_button(
            label="📝 Download Text Summary",
            data=summary,
            file_name=f"seo_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )

def show_marketing_categories():
    """Display marketing tools organized by category"""
    catalog = load_marketing_catalog()

    categories = {
        "🚀 Getting Started": ["seo_strategist.py", "copywriter.py"],
        "🔍 Research & Analysis": ["research_strategist.py", "analyzer.py"],
        "🎯 Conversion & Growth": ["conversion_strategist.py", "idea_strategist.py"],
        "📱 Social & Content": ["social_strategist.py"],
        "📊 Reporting & Management": ["generate_marketing_report.py", "client_onboarding.py", "notion_sync.py"]
    }

    for category_name, script_files in categories.items():
        st.markdown(f"### {category_name}")

        for script_file in script_files:
            # Find the script info
            script_info = None
            for cat_scripts in catalog.values():
                if script_file in cat_scripts:
                    script_info = cat_scripts[script_file]
                    break

            if script_info:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**{script_info['name']}**")
                    st.markdown(f"*{script_info['description']}*")
                with col2:
                    st.markdown(script_info.get('status', '❓'))

                st.markdown("---")