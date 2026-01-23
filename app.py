import streamlit as st

st.set_page_config(page_title="Auracelle Bach | Login", layout="wide")

st.markdown('''
<style>
.stApp {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
</style>
''', unsafe_allow_html=True)

st.title("🎼 Auracelle Bach: E-AGPO-HT Complete Mathematical Intelligence")
st.subheader("9 Mathematical Enhancements for AI Governance")

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        st.markdown("#### 🎯 Purpose")
        st.info("Bach: Complete Mathematical Intelligence Suite for AI Governance - All 9 E-AGPO-HT Enhancements")

        st.markdown("**🔢 Active Enhancements:**")
        st.markdown('''
        1️⃣ Bayesian Uncertainty Quantification
        2️⃣ Convergence Prediction Modeling
        3️⃣ Hierarchical Capability Gap Analysis
        4️⃣ Multi-Objective Pareto Optimization
        5️⃣ Network Diffusion & Cascade Effects
        6️⃣ Historical Pattern Matching
        7️⃣ Maturity Trajectory Planning
        8️⃣ Kalman Filter Capability Tracking
        9️⃣ RL-Optimized Negotiation Strategies
        ''')

        submit = st.form_submit_button("🚀 Launch Bach")

    if submit:
        if password == "charlie2025":
            st.session_state["authenticated"] = True
            st.session_state["username"] = username
            st.success("✅ Authentication successful!")
            st.rerun()
        else:
            st.error("❌ Incorrect password. Access denied.")
            st.stop()
else:
    # Successfully authenticated - show navigation
    st.success(f"✅ Welcome, {st.session_state['username']}!")
    st.info("👈 Use the sidebar to navigate to different pages")
    
    st.markdown("### 🎼 Available Pages:")
    st.markdown("""
    - **📊 Simulation** - Main simulation with all 9 enhancements
    - **🧠 Cognitive Demo** - Cognitive architecture demonstration  
    - **🏛️ Institutional Behavior** - Institutional behavior modeling
    - **🌍 3D Visualization** - 3D governance visualization
    """)
    
    # Note: Streamlit automatically shows pages in sidebar when authenticated
    # Users can navigate using the sidebar menu