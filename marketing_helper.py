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

    params = []
    inputs = script_info['inputs_needed']

    st.markdown("### 📋 Fill out these details:")

    for input_name, input_config in inputs.items():
        label = input_config.get('label', input_name.replace('_', ' ').title())
        help_text = input_config.get('help', '')

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

            params.append(f"--{input_name} {selected_value}")

        else:
            # Text input
            placeholder = input_config.get('placeholder', '')
            value = st.text_input(label, placeholder=placeholder, help=help_text)
            if value:
                params.append(f"--{input_name} \"{value}\"")

    return " ".join(params)

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