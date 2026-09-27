def render_home_page(app):
    from ui_components import apply_modern_styles, hero_section, feature_card
    import streamlit as st
    
    apply_modern_styles()
    
    # Hero Section
    hero_section(
        "Smart Resume AI",
        "Transform your career with AI-powered resume analysis and building. Get personalized insights and create professional resumes that stand out."
    )
    
    # Features Section
    st.markdown('<div class="feature-grid">', unsafe_allow_html=True)
    
    feature_card(
        "fas fa-robot",
        "AI-Powered Analysis",
        "Get instant feedback on your resume with advanced AI analysis that identifies strengths and areas for improvement."
    )
    
    feature_card(
        "fas fa-magic",
        "Smart Resume Builder",
        "Create professional resumes with our intelligent builder that suggests optimal content and formatting."
    )
    
    feature_card(
        "fas fa-chart-line",
        "Career Insights",
        "Access detailed analytics and personalized recommendations to enhance your career prospects."
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.toast("Check out these repositories: [AI-Nexus(AI/ML)](https://github.com/Hunterdii/AI-Nexus)", icon="ℹ️")

    # Call-to-Action with Streamlit navigation
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Get Started", key="get_started_btn", 
                    help="Click to start analyzing your resume",
                    type="primary",
                    use_container_width=True):
            cleaned_name = "🔍 RESUME ANALYZER".lower().replace(" ", "_").replace("🔍", "").strip()
            st.session_state.page = cleaned_name
            st.rerun()
