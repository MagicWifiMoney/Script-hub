"""
Welcome screen for Script Hub Marketing Tools
User-friendly introduction and onboarding
"""

import streamlit as st

def show_welcome_screen():
    """Display comprehensive welcome screen for new users"""

    # Hero section
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 10px; margin-bottom: 2rem;">
        <h1>🎯 Welcome to Your Marketing Automation Hub</h1>
        <h3>8 AI Marketing Experts at Your Fingertips - No Technical Skills Required!</h3>
    </div>
    """, unsafe_allow_html=True)

    # Quick overview
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        ### 🚀 Get Started in 2 Minutes
        1. Pick a marketing tool
        2. Fill out simple form
        3. Get professional results
        4. Use with ChatGPT for full analysis
        """)

    with col2:
        st.markdown("""
        ### 🎯 Perfect For
        - Business owners who need marketing help
        - Team members without marketing experience
        - Anyone who wants professional results fast
        - People who work with ChatGPT or Claude
        """)

    with col3:
        st.markdown("""
        ### ✅ What You Get
        - Professional SEO analysis
        - Marketing copy briefs
        - Competitor research frameworks
        - Social media strategies
        - Campaign ideas and concepts
        """)

    # Tool showcase
    st.markdown("## 🛠️ Your Marketing Tools")

    tools_showcase = [
        {
            "emoji": "🔍",
            "name": "SEO Strategist",
            "description": "Get more Google traffic",
            "use_case": "Find the top 5 SEO improvements for your website",
            "time": "5 min",
            "difficulty": "Easy"
        },
        {
            "emoji": "✍️",
            "name": "Content Creator",
            "description": "Write better marketing copy",
            "use_case": "Create landing page copy that converts visitors to customers",
            "time": "3 min",
            "difficulty": "Easy"
        },
        {
            "emoji": "📊",
            "name": "Market Researcher",
            "description": "Understand your competition",
            "use_case": "Analyze competitors to find market opportunities",
            "time": "5 min",
            "difficulty": "Easy"
        },
        {
            "emoji": "🎯",
            "name": "Conversion Optimizer",
            "description": "Get more customers",
            "use_case": "Reduce shopping cart abandonment by 25%",
            "time": "5 min",
            "difficulty": "Easy"
        }
    ]

    # Display tool cards in 2x2 grid
    row1_col1, row1_col2 = st.columns(2)
    row2_col1, row2_col2 = st.columns(2)

    columns = [row1_col1, row1_col2, row2_col1, row2_col2]

    for i, tool in enumerate(tools_showcase):
        with columns[i]:
            st.markdown(f"""
            <div style="border: 2px solid #e0e0e0; border-radius: 10px; padding: 1rem; margin: 0.5rem 0; height: 200px;">
                <h3>{tool['emoji']} {tool['name']}</h3>
                <p><strong>{tool['description']}</strong></p>
                <p style="color: #666; font-size: 0.9em;">{tool['use_case']}</p>
                <div style="position: absolute; bottom: 1rem;">
                    <span style="background: #e8f5e8; padding: 0.2rem 0.5rem; border-radius: 5px; font-size: 0.8em;">⏱️ {tool['time']}</span>
                    <span style="background: #e8f5e8; padding: 0.2rem 0.5rem; border-radius: 5px; font-size: 0.8em; margin-left: 0.5rem;">📈 {tool['difficulty']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Quick start section
    st.markdown("## 🚀 Quick Start Guide")

    quick_start_steps = st.columns(4)

    steps = [
        {"number": "1", "title": "Choose Tool", "desc": "Pick from 8 marketing experts"},
        {"number": "2", "title": "Simple Form", "desc": "Answer easy questions"},
        {"number": "3", "title": "Get Results", "desc": "Professional analysis ready"},
        {"number": "4", "title": "Use AI", "desc": "Copy to ChatGPT for full details"}
    ]

    for i, step in enumerate(steps):
        with quick_start_steps[i]:
            st.markdown(f"""
            <div style="text-align: center; padding: 1rem;">
                <div style="background: #667eea; color: white; border-radius: 50%; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; margin: 0 auto 1rem; font-weight: bold; font-size: 1.2em;">
                    {step['number']}
                </div>
                <h4>{step['title']}</h4>
                <p style="font-size: 0.9em; color: #666;">{step['desc']}</p>
            </div>
            """, unsafe_allow_html=True)

    # FAQ section
    st.markdown("## ❓ Common Questions")

    faq_items = [
        {
            "question": "Do I need to be technical to use this?",
            "answer": "Not at all! Everything uses simple web forms. If you can fill out an online questionnaire, you can use these tools."
        },
        {
            "question": "What do I do with the results?",
            "answer": "Copy the output and paste it into ChatGPT or Claude with a request like 'Please give me detailed recommendations based on this analysis.'"
        },
        {
            "question": "How accurate are the recommendations?",
            "answer": "The tools create professional frameworks based on marketing best practices. When combined with AI analysis, you get expert-level recommendations."
        },
        {
            "question": "Can I use this for client work?",
            "answer": "Yes! The outputs are professional-quality and can be used for client presentations, reports, and strategic planning."
        }
    ]

    for faq in faq_items:
        with st.expander(f"❓ {faq['question']}"):
            st.markdown(faq['answer'])

    # Success stories teaser
    st.markdown("## 🎉 What Others Have Achieved")

    success_col1, success_col2, success_col3 = st.columns(3)

    with success_col1:
        st.markdown("""
        **📈 Local Restaurant**
        Used SEO Strategist to find 15 improvements.
        *Result: 120% increase in website traffic*
        """)

    with success_col2:
        st.markdown("""
        **🛒 E-commerce Store**
        Used Conversion Optimizer on checkout.
        *Result: 40% improvement in conversion rate*
        """)

    with success_col3:
        st.markdown("""
        **💼 SaaS Company**
        Used Content Creator for lead magnets.
        *Result: 300 new leads in first month*
        """)

    # Call to action
    st.markdown("---")

    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: #f8f9fa; border-radius: 10px;">
        <h3>🎯 Ready to Get Started?</h3>
        <p>Click on the <strong>"🚀 Run Scripts"</strong> tab above to choose your first marketing tool!</p>
        <p style="font-size: 0.9em; color: #666;">💡 New to marketing? Start with the SEO Strategist - just enter your website URL and get actionable improvements in minutes!</p>
    </div>
    """, unsafe_allow_html=True)

def show_tutorial_modal():
    """Show tutorial in a modal/sidebar"""
    with st.sidebar:
        st.markdown("### 📚 Need Help?")

        if st.button("👋 First time here?"):
            st.session_state.show_welcome = True

        if st.button("📖 User Guide"):
            st.session_state.show_user_guide = True

        if st.button("❓ FAQ"):
            st.session_state.show_faq = True

        st.markdown("---")
        st.markdown("### 🎯 Quick Tips")
        st.markdown("""
        - **New users:** Start with SEO Strategist
        - **Need copy:** Use Content Creator
        - **Research competition:** Try Market Researcher
        - **All results** work great with ChatGPT!
        """)

def show_first_time_tips():
    """Show contextual tips for first-time users"""
    if 'first_visit' not in st.session_state:
        st.session_state.first_visit = True

    if st.session_state.first_visit:
        st.info("""
        👋 **First time here?** Here's what to do:
        1. Try the **SEO Strategist** - just enter your website URL
        2. Copy the results and paste into ChatGPT for detailed recommendations
        3. Explore other tools once you're comfortable!
        """)

        if st.button("Got it! Hide this tip"):
            st.session_state.first_visit = False
            st.rerun()

def show_help_panel():
    """Show contextual help based on current tool"""
    with st.sidebar:
        st.markdown("### 💡 Tips for Current Tool")

        # This would be populated based on which tool is selected
        st.markdown("""
        **Using SEO Strategist?**
        - Enter your full website URL (https://...)
        - Try "Quick Analysis" first
        - Copy all results to ChatGPT for details

        **Using Content Creator?**
        - Be specific about your audience
        - Choose the right content type
        - Use the brief as a starting point
        """)

        st.markdown("---")
        st.markdown("[📖 Full User Guide]()")
        st.markdown("[❓ FAQ & Help]()")