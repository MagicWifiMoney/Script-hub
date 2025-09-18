"""
YOUR SCRIPT RUNNER + REPORT EDITOR
Run your Python scripts AND edit the outputs before saving!
Just run: streamlit run script_hub.py
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

# Page config
st.set_page_config(
    page_title="Script Hub - Run & Edit",
    page_icon="🎯",
    layout="wide"
)

# Initialize session state
if 'script_output' not in st.session_state:
    st.session_state.script_output = ""
if 'edited_output' not in st.session_state:
    st.session_state.edited_output = ""
if 'history' not in st.session_state:
    st.session_state.history = []

# Header
st.title("🎯 Script Hub - Run Your Python Scripts & Edit Reports")
st.markdown("Run your scripts, customize the output, save perfect reports!")

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(["🚀 Run Scripts", "✏️ Edit Output", "📚 Script Library", "📜 History"])

with tab1:
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### 📁 Your Scripts")
        
        # Script directory selector (dynamic default for local/Render)
        default_scripts_dir = os.environ.get("SCRIPTS_DIR") or "./python_scripts"
        script_dir = st.text_input(
            "Scripts folder path:",
            value=default_scripts_dir,
            help="Path to your Python scripts folder (set SCRIPTS_DIR env var to override)"
        )
        # Persist for sidebar display
        st.session_state["script_dir"] = script_dir
        
        # Create the directory if it doesn't exist
        Path(script_dir).mkdir(exist_ok=True)
        
        # Get all Python scripts in the directory
        script_files = glob.glob(os.path.join(script_dir, "*.py"))

        # Category filters and visibility controls
        with st.expander("Filters", expanded=True):
            category_to_keywords = {
                "SEO": ["seo", "keyword", "serp", "backlink", "audit", "crawl", "sitemap", "search_console", "gsc", "ahrefs", "semrush", "moz"],
                "Marketing": ["marketing", "ads", "campaign", "content", "copy", "brand", "email", "newsletter"],
                "Analytics": ["analytics", "metric", "kpi", "report", "tracking", "google_analytics", "ga", "dashboard"],
                "Web Automation": ["scrap", "scraper", "crawl", "selenium", "browser", "firecrawl", "web"],
                "Data Processing": ["data", "pandas", "csv", "xlsx", "process", "clean", "transform", "etl"],
                "Social Media": ["twitter", "instagram", "facebook", "linkedin", "tiktok", "youtube", "social"],
                "Utilities": ["util", "helper", "tool", "cli", "manager"],
            }

            selected_categories = st.multiselect(
                "Categories",
                options=list(category_to_keywords.keys()),
                help="Filter scripts by category keywords"
            )

            col_f1, col_f2 = st.columns(2)
            with col_f1:
                hide_tests = st.checkbox("Hide test files", value=True)
            with col_f2:
                hide_dunder = st.checkbox("Hide dunder files", value=True)

            search_query = st.text_input("Search by filename", placeholder="e.g., audit, scraper, twitter")

        # Apply filters
        def matches_categories(name: str) -> bool:
            if not selected_categories:
                return True
            for cat in selected_categories:
                for kw in category_to_keywords.get(cat, []):
                    if kw in name:
                        return True
            return False

        visible_files = []
        for path in script_files:
            fname = os.path.basename(path)
            lower = fname.lower()
            if hide_dunder and lower.startswith("__"):
                continue
            if hide_tests and (lower.startswith("test_") or lower.endswith("_test.py")):
                continue
            if search_query and search_query.lower() not in lower:
                continue
            if not matches_categories(lower):
                continue
            visible_files.append(path)
        
        if visible_files:
            # Script selector
            selected_script = st.selectbox(
                "Choose a script:",
                visible_files,
                format_func=lambda x: os.path.basename(x)
            )
            
            # Show script info
            if selected_script:
                st.info(f"📄 **Selected:** {os.path.basename(selected_script)}")
                
                # Try to extract script description
                try:
                    with open(selected_script, 'r') as f:
                        first_lines = f.read(500)
                        if '"""' in first_lines:
                            doc = first_lines.split('"""')[1] if len(first_lines.split('"""')) > 1 else "No description"
                            st.caption(doc.strip()[:200])
                except:
                    pass
            
            # Parameters input
            st.markdown("### ⚙️ Script Parameters")
            
            # Different input methods
            input_method = st.radio(
                "How to pass parameters:",
                ["Simple (one line)", "Arguments (key=value)", "JSON"]
            )
            
            if input_method == "Simple (one line)":
                params = st.text_input(
                    "Parameters:",
                    placeholder="e.g., Apple stock analysis 2024"
                )
            elif input_method == "Arguments (key=value)":
                params = st.text_area(
                    "Arguments (one per line):",
                    placeholder="topic=Apple\ndepth=comprehensive\nyear=2024",
                    height=100
                )
            else:  # JSON
                params = st.text_area(
                    "JSON parameters:",
                    value='{\n  "topic": "Apple",\n  "depth": "comprehensive",\n  "year": 2024\n}',
                    height=150
                )
            
            # Run button
            if st.button("🚀 **Run Script**", type="primary", use_container_width=True):
                with st.spinner(f"Running {os.path.basename(selected_script)}..."):
                    try:
                        # Build command
                        cmd = [sys.executable, selected_script]
                        
                        # Add parameters based on input method
                        if params:
                            if input_method == "Simple (one line)":
                                cmd.extend(params.split())
                            elif input_method == "Arguments (key=value)":
                                for line in params.strip().split('\n'):
                                    if '=' in line:
                                        key, value = line.split('=', 1)
                                        cmd.extend([f"--{key}", value])
                            else:  # JSON
                                cmd.extend(['--json', params])
                        
                        # Run the script
                        result = subprocess.run(
                            cmd,
                            capture_output=True,
                            text=True,
                            timeout=300  # 5 minute timeout
                        )
                        
                        # Store output
                        output = result.stdout
                        if result.stderr:
                            output += f"\n\n--- Errors ---\n{result.stderr}"
                        
                        st.session_state.script_output = output
                        st.session_state.edited_output = output
                        
                        # Add to history
                        st.session_state.history.append({
                            "script": os.path.basename(selected_script),
                            "params": params,
                            "output": output,
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        })
                        
                        st.success("✅ Script completed! Check the output →")
                        
                    except subprocess.TimeoutExpired:
                        st.error("⏱️ Script timed out (5 minutes max)")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
                        st.code(traceback.format_exc())
        else:
            st.warning(f"📂 No Python scripts found in: {script_dir}")
            st.info("Add your .py scripts to this folder and refresh the page")
    
    with col2:
        st.markdown("### 📊 Script Output")
        
        if st.session_state.script_output:
            # Display output
            output_container = st.container()
            with output_container:
                st.code(st.session_state.script_output, language="text")
            
            # Quick actions
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("✏️ Edit Output", use_container_width=True):
                    st.info("👉 Go to 'Edit Output' tab to customize")
            with col2:
                if st.button("📋 Copy", use_container_width=True):
                    st.write("Output copied! (use Ctrl+C on the text)")
            with col3:
                # Download raw output
                st.download_button(
                    "💾 Download",
                    st.session_state.script_output,
                    f"output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    use_container_width=True
                )
        else:
            st.info("👈 Run a script to see output here")

with tab2:
    st.markdown("### ✏️ Edit & Format Output")
    st.markdown("Transform your script output into a polished report!")
    
    if st.session_state.script_output:
        # Template selector
        template = st.selectbox(
            "Apply a template:",
            ["No Template", "Executive Report", "Technical Analysis", "Research Paper", "Markdown Report"]
        )
        
        # Apply template
        if template != "No Template" and st.button("Apply Template"):
            if template == "Executive Report":
                st.session_state.edited_output = f"""# Executive Report
Generated: {datetime.now().strftime("%B %d, %Y")}

## Executive Summary
[Add 2-3 sentence summary here]

## Key Findings
{st.session_state.script_output[:500]}

## Detailed Analysis
{st.session_state.script_output}

## Recommendations
1. [Add recommendation]
2. [Add recommendation]
3. [Add recommendation]

## Next Steps
- [ ] Action item 1
- [ ] Action item 2
- [ ] Action item 3
"""
            elif template == "Technical Analysis":
                st.session_state.edited_output = f"""# Technical Analysis Report

## Overview
{st.session_state.script_output[:300]}

## Technical Details
{st.session_state.script_output}

## Performance Metrics
- Metric 1: [Value]
- Metric 2: [Value]
- Metric 3: [Value]

## Conclusions
[Add conclusions]
"""
            elif template == "Research Paper":
                st.session_state.edited_output = f"""# Research Report

## Abstract
[Add abstract]

## Introduction
[Add introduction]

## Methodology
[Describe methodology]

## Results
{st.session_state.script_output}

## Discussion
[Add discussion]

## Conclusion
[Add conclusion]

## References
[Add references]
"""
            elif template == "Markdown Report":
                st.session_state.edited_output = f"""# Report: [Title]

**Date:** {datetime.now().strftime("%Y-%m-%d")}  
**Generated by:** {st.session_state.history[-1]['script'] if st.session_state.history else 'Script'}

---

## Summary
{st.session_state.script_output[:500]}...

## Full Results
```
{st.session_state.script_output}
```

## Analysis
[Add your analysis here]

## Key Takeaways
- Point 1
- Point 2
- Point 3

---
*Report generated automatically and edited manually*
"""
        
        # Editor
        edited = st.text_area(
            "Edit your output:",
            value=st.session_state.edited_output,
            height=500,
            help="Edit the output to create your perfect report"
        )
        st.session_state.edited_output = edited
        
        # Save options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Save as text
            st.download_button(
                "💾 Save as Text",
                st.session_state.edited_output,
                f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                use_container_width=True
            )
        
        with col2:
            # Save as markdown
            st.download_button(
                "📝 Save as Markdown",
                st.session_state.edited_output,
                f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                use_container_width=True
            )
        
        with col3:
            # Save as HTML
            html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
        pre {{ background: #f4f4f4; padding: 15px; border-radius: 5px; overflow-x: auto; }}
    </style>
</head>
<body>
<pre>{st.session_state.edited_output}</pre>
</body>
</html>"""
            st.download_button(
                "🌐 Save as HTML",
                html_content,
                f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                mime="text/html",
                use_container_width=True
            )
    else:
        st.info("👈 Run a script first to edit its output")

with tab3:
    st.markdown("### 📚 Script Library")
    st.markdown("Quick templates for common research scripts")
    
    # Script templates
    templates = {
        "Web Scraper": '''"""Web scraping script"""
import requests
from bs4 import BeautifulSoup
import sys

url = sys.argv[1] if len(sys.argv) > 1 else "https://example.com"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

print(f"Title: {soup.title.string}")
print(f"\\nText content:\\n{soup.get_text()[:1000]}")
''',
        "Data Analyzer": '''"""Data analysis script"""
import pandas as pd
import sys

# Your analysis code here
data = {"metric": [1, 2, 3], "value": [10, 20, 30]}
df = pd.DataFrame(data)

print("Data Analysis Results")
print("=" * 40)
print(df.describe())
print("\\nCorrelation Matrix:")
print(df.corr())
''',
        "API Caller": '''"""API calling script"""
import requests
import json
import sys

endpoint = sys.argv[1] if len(sys.argv) > 1 else "https://api.example.com"

# Your API code here
print(f"Calling API: {endpoint}")
# response = requests.get(endpoint)
# print(json.dumps(response.json(), indent=2))
print("API call completed")
''',
        "Research Script": '''"""Research automation script"""
import sys
from datetime import datetime

topic = sys.argv[1] if len(sys.argv) > 1 else "AI"

print(f"Researching: {topic}")
print(f"Date: {datetime.now()}")
print("=" * 50)

# Your research code here
print(f"\\n1. Searching for {topic}...")
print(f"2. Analyzing data...")
print(f"3. Generating insights...")

print(f"\\nResearch on {topic} completed!")
'''
    }
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        selected_template = st.selectbox(
            "Choose a template:",
            list(templates.keys())
        )
        
        script_name = st.text_input(
            "Script name:",
            value=f"{selected_template.lower().replace(' ', '_')}.py"
        )
        
        if st.button("💾 Save Template as Script"):
            script_path = os.path.join(st.session_state.get('script_dir', './my_scripts'), script_name)
            os.makedirs(os.path.dirname(script_path), exist_ok=True)
            
            with open(script_path, 'w') as f:
                f.write(templates[selected_template])
            
            st.success(f"✅ Saved to {script_path}")
            st.balloons()
    
    with col2:
        st.markdown("### Template Code")
        st.code(templates[selected_template], language="python")
        
        st.info("💡 Save this template, then modify it in your favorite editor!")

with tab4:
    st.markdown("### 📜 Run History")
    
    if st.session_state.history:
        for i, item in enumerate(reversed(st.session_state.history[-10:])):  # Show last 10
            with st.expander(f"{item['script']} - {item['timestamp']}"):
                st.markdown(f"**Parameters:** {item['params']}")
                st.code(item['output'][:500] + "..." if len(item['output']) > 500 else item['output'])
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"Load Output", key=f"load_{i}"):
                        st.session_state.script_output = item['output']
                        st.session_state.edited_output = item['output']
                        st.success("Loaded!")
                with col2:
                    st.download_button(
                        "Download",
                        item['output'],
                        f"history_{i}.txt",
                        key=f"dl_{i}"
                    )
        
        if st.button("🗑️ Clear History"):
            st.session_state.history = []
            st.rerun()
    else:
        st.info("No history yet. Run some scripts to see them here!")

# Sidebar
with st.sidebar:
    st.markdown("## 🎯 Quick Guide")
    st.markdown("""
    ### How to use:
    1. **Add your scripts** to the folder
    2. **Select a script** from the dropdown
    3. **Enter parameters** (if needed)
    4. **Run the script**
    5. **Edit the output** to create reports
    6. **Save** in your preferred format
    
    ### Parameter formats:
    - **Simple:** `apple 2024 analysis`
    - **Arguments:** `topic=apple year=2024`
    - **JSON:** `{"topic": "apple"}`
    
    ### Tips:
    - Scripts run with 5-minute timeout
    - Output is auto-saved to history
    - Use templates for quick formatting
    - Edit output before saving
    """)
    
    st.divider()
    
    st.markdown("### 📂 Your Scripts Folder")
    st.code(st.session_state.get('script_dir', './my_scripts'))
    
    st.markdown("### 🔧 Add Scripts")
    st.markdown("""
    Drop your `.py` files in the scripts folder.
    They should accept parameters via:
    - `sys.argv` for simple args
    - `argparse` for named args
    - `--json` for JSON input
    """)
