"""
Enhanced Script Hub with Marketing Tools
User-friendly interface with guided forms and helpful descriptions
"""

import streamlit as st
import subprocess
import sys
import os
import json
from datetime import datetime
import glob
from pathlib import Path
import importlib.util
import traceback
import shlex

# Import our helper modules
try:
    from marketing_helper import (
        load_marketing_catalog, get_script_info,
        display_marketing_tool_card, create_guided_form,
        show_marketing_categories, display_seo_analysis_results
    )
    from welcome import show_welcome_screen, show_first_time_tips
    from premium_ui import (
        apply_premium_theme, premium_header, premium_metrics_row,
        premium_tool_card, premium_loading_animation, premium_success_banner,
        premium_dashboard_stats, premium_feature_spotlight
    )
    from client_intelligence import ClientIntelligenceSystem
    MARKETING_HELPERS_AVAILABLE = True
    PREMIUM_UI_AVAILABLE = True
    CLIENT_INTELLIGENCE_AVAILABLE = True
except ImportError as e:
    MARKETING_HELPERS_AVAILABLE = False
    PREMIUM_UI_AVAILABLE = False
    CLIENT_INTELLIGENCE_AVAILABLE = False

def parse_script_arguments(params):
    """
    Parse script parameters with proper handling of quoted arguments.
    Returns a list of arguments ready for subprocess.
    """
    if not params.strip():
        return []

    try:
        # Use shlex.split for proper shell-like argument parsing
        return shlex.split(params)
    except ValueError:
        # Fallback to simple split if shlex fails
        return params.split()

# Page config
st.set_page_config(
    page_title="⚡ Fermat AI Marketing Hub",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Apply premium theme
if PREMIUM_UI_AVAILABLE:
    apply_premium_theme()

# Initialize session state
if 'script_output' not in st.session_state:
    st.session_state.script_output = ""
if 'edited_output' not in st.session_state:
    st.session_state.edited_output = ""
if 'history' not in st.session_state:
    st.session_state.history = []
if 'show_welcome' not in st.session_state:
    st.session_state.show_welcome = True
if 'first_visit' not in st.session_state:
    st.session_state.first_visit = True
if 'selected_client_id' not in st.session_state:
    st.session_state.selected_client_id = None
if 'client_intelligence' not in st.session_state and CLIENT_INTELLIGENCE_AVAILABLE:
    st.session_state.client_intelligence = ClientIntelligenceSystem()

# Premium Header
if PREMIUM_UI_AVAILABLE:
    premium_header()
    premium_dashboard_stats()
    premium_feature_spotlight()
else:
    st.title("🎯 Script Hub - Marketing Automation Made Simple")

# Show welcome screen for first-time users
if st.session_state.show_welcome and MARKETING_HELPERS_AVAILABLE:
    show_welcome_screen()

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚀 Get Started with Marketing Tools", use_container_width=True):
            st.session_state.show_welcome = False
            st.rerun()

    st.stop()

# Main interface
st.markdown("**Your AI-powered marketing team - no technical skills required!**")

# Show first-time tips if user is new
if MARKETING_HELPERS_AVAILABLE and st.session_state.first_visit:
    show_first_time_tips()

# Create tabs
if CLIENT_INTELLIGENCE_AVAILABLE:
    tab0, tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "👥 Client Dashboard",
        "🚀 Marketing Tools",
        "✏️ Edit Output",
        "📚 Tool Library",
        "📜 History",
        "❓ Help & Guide"
    ])
else:
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🚀 Marketing Tools",
        "✏️ Edit Output",
        "📚 Tool Library",
        "📜 History",
        "❓ Help & Guide"
    ])

# Client Dashboard Tab
if CLIENT_INTELLIGENCE_AVAILABLE:
    with tab0:
        st.markdown("### 👥 Smart Client Management")
        st.markdown("Build detailed client profiles automatically from website URLs for better marketing insights.")

        # Client onboarding section
        st.markdown("#### 🚀 Quick Client Onboarding")

        col1, col2 = st.columns([2, 1])

        with col1:
            # New client form
            with st.form("new_client_form"):
                st.markdown("**Add New Client**")
                website_url = st.text_input("Website URL", placeholder="https://example.com")
                client_name = st.text_input("Client Name (Optional)", placeholder="Leave blank to auto-detect")

                submitted = st.form_submit_button("🔍 Create Client Profile", type="primary")

                if submitted and website_url:
                    with st.spinner("🤖 Building comprehensive client profile... This may take 2-3 minutes"):
                        try:
                            result = st.session_state.client_intelligence.create_client_from_website(
                                website_url, client_name if client_name else None
                            )

                            if result["success"]:
                                st.success(f"✅ Successfully created profile for {result['client_name']}")
                                st.session_state.selected_client_id = result["client_id"]

                                # Show profile summary
                                with st.expander("📊 Client Profile Summary", expanded=True):
                                    profile = result["client_profile"]
                                    st.markdown(f"**Industry:** {profile.get('industry', 'Unknown')}")
                                    st.markdown(f"**Business Type:** {profile.get('business_type', 'Unknown')}")
                                    st.markdown(f"**Target Audience:** {profile.get('target_audience', 'Not specified')}")

                                    if profile.get('key_services'):
                                        services = profile['key_services'][:3]  # Show first 3
                                        st.markdown(f"**Key Services:** {', '.join(services)}")

                                    if profile.get('competitive_advantages'):
                                        advantages = profile['competitive_advantages'][:2]  # Show first 2
                                        st.markdown(f"**Competitive Advantages:** {', '.join(advantages)}")

                                # Show recommendations
                                if result.get("smart_recommendations"):
                                    with st.expander("💡 Smart Marketing Recommendations"):
                                        for rec in result["smart_recommendations"][:5]:
                                            st.markdown(f"• {rec}")

                            else:
                                st.error(f"❌ Failed to create profile: {result.get('error', 'Unknown error')}")

                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")

        with col2:
            # Existing clients list
            st.markdown("**Existing Clients**")
            try:
                clients = st.session_state.client_intelligence.list_clients()

                if clients:
                    for client in clients[:5]:  # Show first 5
                        client_display = f"{client['name']} ({client['domain']})"
                        if st.button(client_display, key=f"select_{client['id']}", use_container_width=True):
                            st.session_state.selected_client_id = client['id']
                            st.success(f"Selected: {client['name']}")
                else:
                    st.info("No clients yet. Add your first client above!")

            except Exception as e:
                st.warning("Client database not initialized yet")

        # Selected client details
        if st.session_state.selected_client_id:
            try:
                client_profile = st.session_state.client_intelligence.get_client_profile(
                    st.session_state.selected_client_id
                )

                if client_profile:
                    st.markdown("---")
                    st.markdown(f"### 📋 Active Client: {client_profile['name']}")

                    # Client profile tabs
                    profile_tab1, profile_tab2, profile_tab3 = st.tabs([
                        "📊 Profile Overview",
                        "🎯 Recommendations",
                        "📈 Campaign History"
                    ])

                    with profile_tab1:
                        col1, col2 = st.columns(2)

                        with col1:
                            st.markdown("**Business Info**")
                            st.markdown(f"**Domain:** {client_profile['domain']}")
                            st.markdown(f"**Industry:** {client_profile.get('industry', 'Unknown')}")
                            st.markdown(f"**Type:** {client_profile.get('business_type', 'Unknown')}")

                            if client_profile.get('location'):
                                st.markdown(f"**Location:** {client_profile['location']}")

                        with col2:
                            st.markdown("**Marketing Context**")
                            st.markdown(f"**Target Audience:** {client_profile.get('target_audience', 'Not specified')}")

                            if client_profile.get('key_services'):
                                services = client_profile['key_services'][:3]
                                st.markdown(f"**Services:** {', '.join(services)}")

                    with profile_tab2:
                        # Get fresh recommendations
                        recommendations = st.session_state.client_intelligence.get_client_recommendations(
                            st.session_state.selected_client_id
                        )

                        if recommendations:
                            for i, rec in enumerate(recommendations[:8], 1):
                                st.markdown(f"{i}. {rec}")
                        else:
                            st.info("No recommendations available yet")

                    with profile_tab3:
                        st.info("Campaign history feature coming soon")

            except Exception as e:
                st.error(f"Error loading client profile: {str(e)}")

with tab1:
    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("### 🎯 Choose Your Marketing Tool")

        # Script directory selector
        default_scripts_dir = os.environ.get("SCRIPTS_DIR") or "./python_scripts"
        script_dir = st.text_input(
            "Scripts folder:",
            value=default_scripts_dir,
            help="Directory containing your marketing scripts"
        )

        if not os.path.exists(script_dir):
            st.error(f"📁 Directory not found: {script_dir}")
            st.stop()

        # Get all Python files
        pattern = os.path.join(script_dir, "**", "*.py")
        all_files = glob.glob(pattern, recursive=True)

        # Filter and organize files
        visible_files = []
        marketing_files = []
        other_files = []

        for path in all_files:
            fname = os.path.basename(path)
            if fname.startswith("__") or fname.startswith("test_") or fname.endswith("_test.py"):
                continue

            # Categorize files
            if "marketing" in path or "client" in path:
                marketing_files.append(path)
            else:
                other_files.append(path)

            visible_files.append(path)

        if visible_files:
            # Categorized selection
            st.markdown("#### 🤖 Marketing Experts")

            if marketing_files:
                # Show marketing tools with friendly names
                if MARKETING_HELPERS_AVAILABLE:
                    marketing_options = {}
                    catalog = load_marketing_catalog()

                    for path in marketing_files:
                        script_name = os.path.basename(path)
                        script_info = get_script_info(path)
                        friendly_name = f"{script_info.get('name', script_name)} {script_info.get('status', '')}"
                        marketing_options[friendly_name] = path

                    if marketing_options:
                        selected_friendly = st.selectbox(
                            "Choose marketing tool:",
                            list(marketing_options.keys()),
                            help="Select which marketing expert you'd like to use"
                        )
                        selected_script = marketing_options[selected_friendly]
                else:
                    selected_script = st.selectbox(
                        "Choose marketing script:",
                        marketing_files,
                        format_func=lambda x: os.path.basename(x)
                    )
            else:
                st.info("No marketing tools found. Make sure marketing scripts are in the python_scripts folder.")
                selected_script = None

            # Show other tools if available
            if other_files:
                st.markdown("#### 🔧 Other Tools")
                with st.expander("View other available scripts"):
                    for path in other_files:
                        st.text(os.path.basename(path))

            # Show selected tool information
            if selected_script and MARKETING_HELPERS_AVAILABLE:
                script_info = get_script_info(selected_script)
                st.markdown("---")
                st.markdown(f"### {script_info.get('name', 'Selected Tool')}")
                st.markdown(f"**What it does:** {script_info.get('description', 'No description available')}")

                if 'perfect_for' in script_info:
                    st.info(f"💡 **Perfect for:** {script_info['perfect_for']}")

                if 'time_to_complete' in script_info:
                    st.markdown(f"⏱️ **Estimated time:** {script_info['time_to_complete']}")

            # Parameters input - Enhanced for marketing tools
            if selected_script:
                st.markdown("### 📝 Tool Configuration")

                # Initialize input_method to avoid scope issues
                input_method = "guided_form"  # Default for marketing tools

                if MARKETING_HELPERS_AVAILABLE and selected_script in marketing_files:
                    script_info = get_script_info(selected_script)

                    # Get client profile for context-aware forms
                    client_profile = None
                    if CLIENT_INTELLIGENCE_AVAILABLE and st.session_state.selected_client_id:
                        try:
                            client_profile = st.session_state.client_intelligence.get_client_profile(
                                st.session_state.selected_client_id
                            )
                        except:
                            pass

                    params = create_guided_form(selected_script, script_info, client_profile)
                else:
                    # Fallback to simple input
                    input_method = st.radio(
                        "Parameter input method:",
                        ["Simple (one line)", "Arguments (key=value)", "JSON"],
                        help="Choose how you want to provide parameters to the script"
                    )

                    if input_method == "Simple (one line)":
                        params = st.text_input(
                            "Parameters:",
                            placeholder="e.g., https://yourwebsite.com --analysis_type quick"
                        )
                    elif input_method == "Arguments (key=value)":
                        params = st.text_area(
                            "Parameters (one per line):",
                            placeholder="website_url=https://example.com\nanalysis_type=comprehensive\nclient_name=My Company"
                        )
                    else:  # JSON
                        params = st.text_area(
                            "JSON Parameters:",
                            placeholder='{"website_url": "https://example.com", "analysis_type": "quick"}'
                        )

                # Run button
                if st.button("🚀 Run Analysis", type="primary", use_container_width=True):
                    try:
                        # Show different progress messages based on the tool
                        progress_msg = "Running your marketing analysis..."
                        if "seo_strategist.py" in selected_script:
                            progress_msg = "🔍 Analyzing website... This may take 30-60 seconds for real SEO data collection..."

                        with st.spinner(progress_msg):
                            # Build command
                            if input_method == "guided_form":
                                # Handle guided form params (already formatted by create_guided_form)
                                if params.strip():
                                    # Use helper function for proper argument parsing
                                    parsed_args = parse_script_arguments(params)
                                    cmd = ["python3", selected_script] + parsed_args
                                else:
                                    cmd = ["python3", selected_script, "--help"]
                            elif input_method == "JSON" and params.strip():
                                # Handle JSON input
                                try:
                                    json_params = json.loads(params)
                                    cmd_args = []
                                    for key, value in json_params.items():
                                        cmd_args.extend([f"--{key}", str(value)])
                                    cmd = ["python3", selected_script] + cmd_args
                                except json.JSONDecodeError:
                                    st.error("Invalid JSON format")
                                    st.stop()
                            elif input_method == "Arguments (key=value)" and params.strip():
                                # Handle key=value format
                                cmd_args = []
                                for line in params.strip().split('\n'):
                                    if '=' in line:
                                        key, value = line.split('=', 1)
                                        cmd_args.extend([f"--{key.strip()}", value.strip()])
                                cmd = ["python3", selected_script] + cmd_args
                            else:
                                # Handle simple format or guided form
                                if params.strip():
                                    # Use helper function for consistent argument parsing
                                    parsed_args = parse_script_arguments(params)
                                    cmd = ["python3", selected_script] + parsed_args
                                else:
                                    cmd = ["python3", selected_script, "--help"]

                            # Execute script
                            # Fix path handling - use absolute path or adjust working directory correctly
                            script_dir = os.path.dirname(selected_script)
                            script_name = os.path.basename(selected_script)

                            # If we have a full path, use it directly without changing working directory
                            if os.path.isabs(selected_script):
                                # Use absolute path with original working directory
                                result = subprocess.run(
                                    cmd,
                                    capture_output=True,
                                    text=True,
                                    timeout=300,  # 5 minutes
                                    cwd=None  # Don't change working directory
                                )
                            else:
                                # Use relative path with script's directory as working directory
                                adjusted_cmd = cmd.copy()
                                adjusted_cmd[1] = script_name  # Use just the filename
                                result = subprocess.run(
                                    adjusted_cmd,
                                    capture_output=True,
                                    text=True,
                                    timeout=300,  # 5 minutes
                                    cwd=script_dir
                                )

                            output = result.stdout
                            if result.stderr:
                                output += f"\n\nErrors/Warnings:\n{result.stderr}"

                            st.session_state.script_output = output
                            st.session_state.edited_output = output

                            # Add to history
                            st.session_state.history.append({
                                "script": os.path.basename(selected_script),
                                "params": params,
                                "output": output,
                                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            })

                            st.success("✅ Analysis complete! Check the output →")

                    except subprocess.TimeoutExpired:
                        st.error("⏱️ Analysis timed out (5 minutes max)")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
                        st.code(traceback.format_exc())
        else:
            st.warning(f"📂 No scripts found in: {script_dir}")
            st.info("Add your marketing scripts to this folder and refresh the page")

    with col2:
        st.markdown("### 📊 Analysis Results")

        if st.session_state.script_output:
            # Show helpful context for marketing tools
            if MARKETING_HELPERS_AVAILABLE and selected_script and selected_script in marketing_files:
                script_info = get_script_info(selected_script)
                if 'output_description' in script_info:
                    st.info(f"ℹ️ **About this output:** {script_info['output_description']}")

                if 'next_steps' in script_info:
                    with st.expander("📋 What to do next"):
                        st.markdown(script_info['next_steps'])

            # Display output - use special handling for SEO Strategist
            output_container = st.container()
            with output_container:
                if (MARKETING_HELPERS_AVAILABLE and selected_script and
                    "seo_strategist.py" in selected_script and
                    ("AUTONOMOUS SEO ANALYSIS COMPLETE" in st.session_state.script_output or
                     st.session_state.script_output.strip().startswith('{'))):
                    # Use rich SEO analysis display
                    display_seo_analysis_results(st.session_state.script_output)
                else:
                    # Standard code display
                    st.code(st.session_state.script_output, language="text")

            # Quick actions
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("✏️ Edit Output", use_container_width=True):
                    st.info("👉 Go to 'Edit Output' tab to customize")
            with col2:
                if st.button("📋 Copy to AI", use_container_width=True):
                    st.success("💡 Copy the text above and paste into ChatGPT with: 'Please analyze this and give me detailed recommendations'")
            with col3:
                st.download_button(
                    "💾 Download",
                    st.session_state.script_output,
                    f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    use_container_width=True
                )
        else:
            st.info("👈 Choose a marketing tool and run analysis to see results here")

            if MARKETING_HELPERS_AVAILABLE:
                st.markdown("### 🎯 Suggested First Steps:")
                st.markdown("""
                1. **New to SEO?** → Choose "SEO Strategist" and enter your website URL
                2. **Need marketing copy?** → Choose "Content Creator" and specify what you're writing
                3. **Research competitors?** → Choose "Market Researcher" for competitive analysis
                4. **Want campaign ideas?** → Choose "Campaign Creator" for fresh marketing concepts
                """)

# Edit Output Tab (keeping existing functionality)
with tab2:
    st.markdown("### ✏️ Edit & Format Output")
    st.markdown("Transform your analysis into a polished report!")

    if st.session_state.script_output:
        # Template selector
        template = st.selectbox(
            "Choose format:",
            ["Raw Output", "Professional Report", "Markdown Report", "Client Summary"]
        )

        if template == "Professional Report":
            st.session_state.edited_output = f"""# Marketing Analysis Report

**Date:** {datetime.now().strftime("%Y-%m-%d")}
**Generated by:** Marketing Automation Tools

---

## Executive Summary
[Add executive summary here]

## Analysis Results
{st.session_state.script_output}

## Recommendations
[Add specific recommendations based on the analysis]

## Next Steps
[Outline implementation steps]

## Appendix
[Additional data and references]

---
*Report generated by Script Hub Marketing Tools*
"""
        elif template == "Client Summary":
            st.session_state.edited_output = f"""# Client Marketing Summary

**Client:** [Client Name]
**Date:** {datetime.now().strftime("%Y-%m-%d")}
**Analysis Type:** [Specify type]

## Key Findings
{st.session_state.script_output[:300]}...

## Priority Actions
1. [Action item 1]
2. [Action item 2]
3. [Action item 3]

## Expected Results
- [Expected outcome 1]
- [Expected outcome 2]
- [Expected outcome 3]

## Timeline
- **Week 1-2:** [Implementation phase 1]
- **Week 3-4:** [Implementation phase 2]
- **Month 2+:** [Ongoing optimization]

---
*Prepared by your marketing team*
"""

        # Editor
        edited = st.text_area(
            "Edit your output:",
            value=st.session_state.edited_output,
            height=400
        )

        st.session_state.edited_output = edited

        # Save options
        col1, col2, col3 = st.columns(3)
        with col1:
            st.download_button(
                "📄 Download as Text",
                st.session_state.edited_output,
                f"edited_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            )
        with col2:
            st.download_button(
                "📝 Download as Markdown",
                st.session_state.edited_output,
                f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            )
        with col3:
            if st.button("💾 Save to History"):
                st.session_state.history.append({
                    "script": "Edited Report",
                    "params": "Custom edit",
                    "output": st.session_state.edited_output,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                st.success("Saved!")
    else:
        st.info("Run a marketing tool first to get output to edit")

# Enhanced Tool Library Tab
with tab3:
    st.markdown("### 📚 Marketing Tools Library")

    if MARKETING_HELPERS_AVAILABLE:
        # Show organized categories
        show_marketing_categories()

        st.markdown("### 🔍 All Available Tools")

        catalog = load_marketing_catalog()
        for category_name, scripts in catalog.items():
            st.markdown(f"#### {category_name.replace('_', ' ').title()}")

            for script_file, script_info in scripts.items():
                with st.expander(f"{script_info['name']} - {script_info.get('status', '❓')}"):
                    col1, col2 = st.columns([2, 1])

                    with col1:
                        st.markdown(f"**{script_info['description']}**")
                        st.markdown(f"*{script_info.get('what_it_does', 'No details available')}*")

                        if 'perfect_for' in script_info:
                            st.markdown(f"💡 **Perfect for:** {script_info['perfect_for']}")

                        if 'example_use' in script_info:
                            st.markdown(f"📝 **Example:** {script_info['example_use']}")

                    with col2:
                        if 'time_to_complete' in script_info:
                            st.markdown(f"⏱️ {script_info['time_to_complete']}")

                        st.markdown(f"**Status:** {script_info.get('status', '❓')}")

                        if script_info.get('setup_note'):
                            st.warning(script_info['setup_note'])
    else:
        # Fallback to basic library view
        st.info("Enhanced library not available. Showing basic file list.")
        pattern = os.path.join(default_scripts_dir, "**", "*.py")
        all_files = glob.glob(pattern, recursive=True)

        for file_path in all_files:
            if not os.path.basename(file_path).startswith("__"):
                st.text(f"📄 {os.path.basename(file_path)}")

# History Tab (keeping existing functionality)
with tab4:
    st.markdown("### 📜 Analysis History")

    if st.session_state.history:
        for i, item in enumerate(reversed(st.session_state.history)):
            with st.expander(f"#{len(st.session_state.history)-i}: {item['script']} - {item['timestamp']}"):
                st.markdown(f"**Script:** {item['script']}")
                st.markdown(f"**Parameters:** {item['params']}")
                st.markdown(f"**Time:** {item['timestamp']}")
                st.code(item['output'], language="text")

                if st.button(f"Restore #{len(st.session_state.history)-i}", key=f"restore_{i}"):
                    st.session_state.script_output = item['output']
                    st.session_state.edited_output = item['output']
                    st.success("Restored to current output!")
    else:
        st.info("No analysis history yet. Run some marketing tools to build your history!")

# Help & Guide Tab
with tab5:
    st.markdown("### ❓ Help & User Guide")

    help_option = st.radio(
        "What do you need help with?",
        ["Quick Start Guide", "Tool Explanations", "FAQ", "Tips & Best Practices"]
    )

    if help_option == "Quick Start Guide":
        st.markdown("""
        ## 🚀 Quick Start Guide

        ### Step 1: Choose Your Tool
        Go to the "🚀 Marketing Tools" tab and select a marketing expert from the dropdown.

        ### Step 2: Fill Out the Form
        Answer the simple questions (like "What's your website?" or "Who's your audience?").

        ### Step 3: Run Analysis
        Click the "🚀 Run Analysis" button and wait for results.

        ### Step 4: Use with AI
        Copy the results and paste into ChatGPT or Claude for detailed recommendations.

        ### 💡 First-Time Recommendations:
        - **New to marketing?** Start with SEO Strategist
        - **Need website copy?** Try Content Creator
        - **Want to research competitors?** Use Market Researcher
        """)

    elif help_option == "Tool Explanations":
        st.markdown("""
        ## 🛠️ Tool Explanations

        ### 🔍 SEO Strategist
        **What:** Analyzes your website for Google ranking improvements
        **Best for:** Getting more organic traffic from search engines
        **Input:** Your website URL
        **Output:** SEO improvement recommendations

        ### ✍️ Content Creator
        **What:** Creates briefs for marketing copy and content
        **Best for:** Writing website copy, emails, social media posts
        **Input:** Content type and target audience
        **Output:** Detailed content brief with structure and key points

        ### 📊 Market Researcher
        **What:** Creates frameworks for analyzing competition and market
        **Best for:** Understanding your competitive landscape
        **Input:** Company/industry to research
        **Output:** Research framework and analysis guide

        ### 🎯 Conversion Optimizer
        **What:** Strategies to convert more visitors into customers
        **Best for:** Improving website conversion rates
        **Input:** Current conversion rate and target improvement
        **Output:** Optimization strategy with specific tests
        """)

    elif help_option == "FAQ":
        # Load and display FAQ content
        faq_path = Path(__file__).parent / "FAQ.md"
        if faq_path.exists():
            with open(faq_path, 'r') as f:
                faq_content = f.read()
            st.markdown(faq_content)
        else:
            st.markdown("""
            ## ❓ Frequently Asked Questions

            **Q: I'm not technical. Can I use this?**
            A: Absolutely! Everything uses simple web forms. No technical knowledge required.

            **Q: What do I do with the results?**
            A: Copy them into ChatGPT or Claude for detailed recommendations.

            **Q: Which tool should I start with?**
            A: Try SEO Strategist first - just enter your website URL.

            **Q: How long do the tools take?**
            A: Most complete in 1-5 minutes.
            """)

    elif help_option == "Tips & Best Practices":
        st.markdown("""
        ## 💡 Tips & Best Practices

        ### Getting the Best Results:
        1. **Be specific with inputs** - Better inputs = better outputs
        2. **Use with AI tools** - Copy results to ChatGPT/Claude for full analysis
        3. **Run multiple tools** - Combine SEO + Content + Research for complete strategy
        4. **Start small** - Try quick analyses before comprehensive ones

        ### Workflow Recommendations:
        1. **SEO Strategist** → Understand current position
        2. **Market Researcher** → Analyze competition
        3. **Content Creator** → Plan marketing materials
        4. **Campaign Creator** → Develop promotional ideas
        5. **Performance Analyst** → Set up measurement

        ### Common Mistakes to Avoid:
        - Don't skip the AI step - the real magic happens when you use ChatGPT/Claude
        - Don't try to implement everything at once - prioritize based on impact
        - Don't ignore the "Perfect for" guidance - use the right tool for your needs
        """)

# Sidebar enhancements
with st.sidebar:
    st.markdown("### 🎯 Quick Actions")

    if st.button("🆕 Start Fresh Session"):
        st.session_state.script_output = ""
        st.session_state.edited_output = ""
        st.rerun()

    if st.button("👋 Show Welcome Screen"):
        st.session_state.show_welcome = True
        st.rerun()

    st.markdown("### 💡 Tips")
    st.markdown("""
    - **New user?** Start with SEO Strategist
    - **All results** work great with ChatGPT
    - **Need help?** Check the Help & Guide tab
    - **Multiple tools** can be combined for better results
    """)

    st.markdown("### 📊 Session Stats")
    st.markdown(f"**Tools run:** {len(st.session_state.history)}")
    if st.session_state.script_output:
        st.markdown("**Current output:** Ready")
    else:
        st.markdown("**Current output:** None")