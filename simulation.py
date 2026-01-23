import streamlit as st
import pandas as pd
import networkx as nx
import plotly.express as px
import plotly.graph_objects as go
from pyvis.network import Network
import streamlit.components.v1 as components
import numpy as np
from bach_api_utils import get_bach_api_client

st.set_page_config(layout="wide", page_title="Auracelle Bach - Complete Suite")

if not st.session_state.get("authenticated", False):
    st.warning("⚠️ Please log in first.")
    st.switch_page("app.py")

bach_api = get_bach_api_client()

st.markdown("""
<style>
.reportview-container {background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);}
.metric-card {background: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);}
.stTabs [data-baseweb="tab-list"] {gap: 8px;}
.stTabs [data-baseweb="tab"] {background-color: rgba(255,255,255,0.1); border-radius: 4px;}
</style>
""", unsafe_allow_html=True)

st.title("🎼 Auracelle Bach: Complete Mathematical Intelligence Suite")

# =============================================================================
# POLICY FRAMEWORKS SIDEBAR
# =============================================================================

with st.sidebar:
    st.markdown("---")
    st.markdown("### 📚 International Policy Frameworks")
    st.markdown("*Integrated into simulation logic*")

    with st.expander("🔒 Binding Frameworks (7)", expanded=False):
        st.markdown("""
        **1. EU AI Act**
        Comprehensive AI regulation with risk-based approach

        **2. GDPR**
        Data protection & privacy rights

        **3. NIS2 Directive**
        Network & information security

        **4. US Executive Order 14110**
        Safe, secure & trustworthy AI development

        **5. Council of Europe Convention**
        First international AI treaty (Sept 2024)

        **6. Digital Services Act (DSA)**
        Platform accountability & content moderation

        **7. UK AI Regulation**
        Sectoral regulation approach
        """)

    with st.expander("🤝 Voluntary Frameworks (5)", expanded=False):
        st.markdown("""
        **1. UNESCO Recommendation on AI Ethics**
        Global ethical AI principles (193 countries)

        **2. OECD AI Principles**
        Foundation for responsible AI policy

        **3. NATO Principles on Responsible Use**
        Defense & security AI ethics

        **4. ISO/IEC 42001**
        AI management system standard

        **5. UN AI Principles**
        Universal AI governance framework
        """)

    # Summary box
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 15px; border-radius: 8px; margin-top: 15px;'>
        <p style='color: white; margin: 0; font-size: 13px; text-align: center;'>
            <strong>12 Frameworks</strong><br>
            <span style='font-size: 11px;'>7 Binding • 5 Voluntary</span>
        </p>
    </div>
    """, unsafe_allow_html=True)


st.markdown("**9 Mathematical Enhancements from E-AGPO-HT Formalization**")

st.info("""
📊 **Data Sources**: This simulation integrates data from three authoritative APIs:
- **OECD AI Principles & Policy Observatory** - AI policies, principles, and incidents
- **Privacy International** - Surveillance scores and data protection laws
- **ParlaMint Parliamentary Debates** - Legislative discourse analysis

⚠️ Note: If live APIs are unavailable, the system automatically uses validated static fallback data.
""")

if "round" not in st.session_state:
    st.session_state["round"] = 1

# Sidebar Configuration
st.sidebar.header("🎯 Scenario Configuration")
scenario_type = st.sidebar.selectbox("Select Scenario Type", [
    "Bilateral Policy Negotiation",
    "Multilateral AI Governance Round (3+ Actors)",
    "Cross-Border Digital Shock Response",
    "Regulatory Divergence & Convergence Simulation",
    "Human-AI Joint Decision Making (Hybrid Governance Scenario)",
    "Cross-Border Data Governance Corridor Analysis"
])

country_to_iso = {
    "USA": "USA", "China": "CHN", "EU": "GBR", "India": "IND",
    "Japan": "JPN", "Russia": "CHN", "Brazil": "BRA", "UAE": "ARE"
}

# Expanded actor list (countries + regional blocs)
regional_actors = [
    "MENA",
    "APAC / Asia-Pacific",
    "African Union (AU)",
    "BRICS",
    "GCC",
    "ASEAN+",
    "Five Eyes (FVEY)"
]
all_actors = list(country_to_iso.keys()) + regional_actors

selected_policy = None
selected_country_a = None
selected_country_b = None

if "policies" not in st.session_state:
    st.session_state["policies"] = ["AI Ethics", "AI Safety", "Data Privacy", "Export Controls", "R&D Investment"]

policies = st.session_state["policies"]

if scenario_type == "Bilateral Policy Negotiation":
    st.sidebar.subheader("🌍 Bilateral Actors")
    selected_country_a = st.sidebar.selectbox("Select Actor A", all_actors, index=0)
    selected_country_b = st.sidebar.selectbox("Select Actor B", all_actors, index=1)

    st.sidebar.subheader("📋 Policy Focus")
    selected_policy = st.sidebar.selectbox("Select Policy Area", policies)

elif scenario_type == "Multilateral AI Governance Round (3+ Actors)":
    st.sidebar.subheader("🌐 Multilateral Actors (3+)")
    selected_actors = st.sidebar.multiselect(
        "Select Actors (minimum 3)",
        options=all_actors,
        default=[all_actors[0], all_actors[1], all_actors[2]] if len(all_actors) >= 3 else all_actors
    )
    if len(selected_actors) < 3:
        st.sidebar.warning("Select at least 3 actors to run a multilateral round.")
    # Store all selected actors for multilateral analysis
    if len(selected_actors) >= 2:
        selected_country_a = selected_actors[0]
        selected_country_b = selected_actors[1]
    # Make selected_actors available globally for tabs
    # Always update when actors change (not just when scenario type changes)
    if 'selected_actors' not in st.session_state or st.session_state.get('selected_actors') != selected_actors or st.session_state.get('scenario_type') != scenario_type:
        st.session_state['selected_actors'] = selected_actors
        st.session_state['scenario_type'] = scenario_type
        # Force refresh to update all modules
        if 'actors_changed' not in st.session_state:
            st.session_state['actors_changed'] = True
    st.sidebar.caption("Complexity factors: coalition shifts • institutional asymmetry • cognitive overload")
    # Add confirmation button for actor selection
    if st.sidebar.button("✅ Apply Actor Selection", help="Click to confirm your actor selection"):
        st.session_state['selected_actors'] = selected_actors
        st.session_state['actors_changed'] = True
        st.success(f"✅ Updated to {len(selected_actors)} actors: {', '.join(selected_actors)}")
        st.rerun()


    st.sidebar.subheader("📋 Policy Focus")
    selected_policy = st.sidebar.selectbox("Select Policy Area", policies)

elif scenario_type == "Cross-Border Digital Shock Response":
    st.sidebar.subheader("⚡ Shock Type")
    shock_type = st.sidebar.selectbox(
        "Select Shock",
        ["Cyber breach", "Disinformation wave", "Major AI system failure", "Data localization emergency", "Critical infrastructure attack"]
    )
    st.sidebar.subheader("🌍 Impacted Actors")
    selected_country_a = st.sidebar.selectbox("Primary Impacted Actor", all_actors, index=0)
    selected_country_b = st.sidebar.selectbox("Secondary Actor / Key Ally", all_actors, index=1)
    st.sidebar.caption("Shock modelling: rapid escalation • constrained information • time-to-comply pressure")
    st.sidebar.subheader("📋 Policy Focus")
    selected_policy = st.sidebar.selectbox("Select Policy Area", policies)

elif scenario_type == "Regulatory Divergence & Convergence Simulation":
    st.sidebar.subheader("🧭 Regulatory Relationship")
    selected_country_a = st.sidebar.selectbox("Actor A", all_actors, index=0)
    selected_country_b = st.sidebar.selectbox("Actor B", all_actors, index=1)
    st.sidebar.slider("Initial Alignment (0=Fragmented, 100=Aligned)", 0, 100, 50, key="reg_alignment")
    st.sidebar.checkbox("External Pressure Event (forces convergence)", value=False, key="reg_pressure")
    st.sidebar.caption("States: align • drift • fragment • oscillate • converge-under-pressure")
    st.sidebar.subheader("📋 Policy Focus")
    selected_policy = st.sidebar.selectbox("Select Policy Area", policies)

elif scenario_type == "Human-AI Joint Decision Making (Hybrid Governance Scenario)":
    st.sidebar.subheader("🤝 Hybrid Governance")
    selected_country_a = st.sidebar.selectbox("Human Institution / Actor", all_actors, index=0)
    selected_country_b = "AI System"
    st.sidebar.selectbox("AI Role", ["Adviser", "Co-decider", "Autonomous Executor", "Auditor/Assurance Agent"], key="hybrid_ai_role")
    st.sidebar.slider("Trust Calibration (0=Under-reliance, 100=Over-reliance)", 0, 100, 50, key="hybrid_trust")
    st.sidebar.caption("Models: HITL failures • explanation burden • over/under reliance • trust trajectories")
    st.sidebar.subheader("📋 Policy Focus")
    selected_policy = st.sidebar.selectbox("Select Policy Area", policies)

elif scenario_type == "Cross-Border Data Governance Corridor Analysis":
    st.sidebar.subheader("🛰️ Data Governance Corridor")
    corridor_nodes = ["MENA", "EU", "USA", "APAC / Asia-Pacific", "African Union (AU)", "GCC", "ASEAN+", "BRICS"]
    src_region = st.sidebar.selectbox("Source Region", corridor_nodes, index=0)
    dst_region = st.sidebar.selectbox("Destination Region", corridor_nodes, index=1 if len(corridor_nodes) > 1 else 0)
    selected_country_a = src_region
    selected_country_b = dst_region

    st.sidebar.subheader("🔍 Risk Lens")
    risk_lens = st.sidebar.radio(
        "Select Corridor Risk Lens",
        ["Cross-Border Compliance Risk (CBCR)", "Cross-Border Digital Policy Risk (CBDPR)"],
        index=0
    )
    st.sidebar.caption("CBCR: compliance mismatch • enforcement uncertainty • audit gaps • trust asymmetry")
    st.sidebar.caption("CBDPR: norms volatility • governance friction • market vs state models • traceability divergence")

    st.sidebar.subheader("📋 Policy Focus")
    selected_policy = st.sidebar.selectbox("Select Policy Area", policies)

st.sidebar.header("⚙️ Simulation Controls")
if st.sidebar.button("▶️ Start/Next Round"):
    st.session_state["round"] += 1
if st.sidebar.button("🔄 Reset"):
    for key in list(st.session_state.keys()):
        if key not in ["authenticated", "username"]:
            del st.session_state[key]
    st.rerun()

st.sidebar.info(f"**Round:** {st.session_state['round']}")
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Active Enhancements")
st.sidebar.markdown("""
1️⃣ Bayesian Uncertainty
2️⃣ Convergence Prediction
3️⃣ Capability Gap Analysis
4️⃣ Pareto Optimization
5️⃣ Network Diffusion
6️⃣ Historical Matching
7️⃣ Maturity Planning
8️⃣ Kalman Filtering
9️⃣ RL Strategy Optimization
""")

# Main Tabs - All 9 Enhancements
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
    "🎼 Bayesian", "🔮 Convergence", "🎯 Gap Analysis", "📈 Pareto",
    "🌐 Diffusion", "📚 Historical", "📊 Maturity", "🎯 Kalman", "🤖 RL Strategy"
])

iso_a = country_to_iso.get(selected_country_a, "USA")
iso_b = country_to_iso.get(selected_country_b, "CHN")

# TAB 1: Bayesian Uncertainty Quantification
with tab1:
    st.header("1️⃣ Bayesian Ethical Alignment with Uncertainty Quantification")
    st.markdown("*Quantifies uncertainty in ethical alignment scores using Bayesian posterior distributions*")

    # Get actors based on scenario type
    if scenario_type == "Multilateral AI Governance Round (3+ Actors)":
        display_actors = st.session_state.get('selected_actors', [selected_country_a, selected_country_b])
    else:
        display_actors = [selected_country_a, selected_country_b] if selected_country_b else [selected_country_a]

    # Handle AI System case
    display_actors = [a for a in display_actors if a != "AI System"]

    if not display_actors:
        st.warning("⚠️ Please select at least one actor")
    else:
        # Create dynamic columns based on number of actors
        num_cols = min(len(display_actors), 4)  # Max 4 columns for readability
        cols = st.columns(num_cols)

        bayesian_results = {}

        for idx, actor in enumerate(display_actors):
            col_idx = idx % num_cols
            iso_code = country_to_iso.get(actor, actor)

            with cols[col_idx]:
                st.subheader(f"🌍 {actor}")
                try:
                    bayesian = bach_api.calculate_ethical_alignment_bayesian(iso_code, selected_policy)
                    bayesian_results[actor] = bayesian

                    st.metric(
                        "Ethical Alignment Score",
                        f"{bayesian['score']:.3f}",
                        delta=f"±{bayesian['std_dev']:.3f}"
                    )
                    st.progress(bayesian['reliability'], text=f"Data Reliability: {bayesian['reliability']:.1%}")

                    with st.expander("📊 Details"):
                        st.write(f"**95% CI:** [{bayesian['ci_lower']:.3f}, {bayesian['ci_upper']:.3f}]")
                        st.write(f"**Std Dev:** {bayesian['std_dev']:.3f}")
                        st.write(f"**Reliability:** {bayesian['reliability']:.3f}")
                except Exception as e:
                    st.error(f"❌ Error fetching data: {str(e)}")

        # Visualization for all actors
        if bayesian_results:
            st.subheader("📊 Comparative Analysis")

            fig = go.Figure()
            for actor, result in bayesian_results.items():
                fig.add_trace(go.Bar(
                    name=actor,
                    x=['Ethical Alignment'],
                    y=[result['score']],
                    error_y=dict(type='data', array=[1.96*result['std_dev']]),
                    text=f"{result['score']:.3f}",
                    textposition='auto'
                ))

            fig.update_layout(
                title=f"Ethical Alignment Comparison with 95% CI - {selected_policy}",
                barmode='group',
                yaxis_title="Score",
                showlegend=True
            )
            st.plotly_chart(fig, use_container_width=True)

            # Summary table
            st.subheader("📋 Summary Table")
            summary_data = []
            for actor, result in bayesian_results.items():
                summary_data.append({
                    "Actor": actor,
                    "Score": f"{result['score']:.3f}",
                    "CI Lower": f"{result['ci_lower']:.3f}",
                    "CI Upper": f"{result['ci_upper']:.3f}",
                    "Std Dev": f"{result['std_dev']:.3f}",
                    "Reliability": f"{result['reliability']:.1%}"
                })
            st.dataframe(summary_data, use_container_width=True)

# TAB 2: Convergence Prediction
with tab2:
    st.header("2️⃣ Negotiation Convergence Prediction Model")
    st.markdown("*Predicts expected rounds and probability of successful convergence*")

    # Get actors
    if scenario_type == "Multilateral AI Governance Round (3+ Actors)":
        display_actors = st.session_state.get('selected_actors', [selected_country_a, selected_country_b])
    else:
        display_actors = [selected_country_a, selected_country_b] if selected_country_b else [selected_country_a]

    display_actors = [a for a in display_actors if a != "AI System"]

    if len(display_actors) < 2:
        st.warning("⚠️ Convergence prediction requires at least 2 actors")
    else:
        # For multilateral, show pairwise convergence
        if len(display_actors) > 2:
            st.info(f"📊 Analyzing {len(display_actors)} actors - showing key bilateral convergence paths")

            # Select comparison pairs
            col1, col2 = st.columns(2)
            with col1:
                actor1 = st.selectbox("Select First Actor", display_actors, key="conv_actor1")
            with col2:
                remaining = [a for a in display_actors if a != actor1]
                actor2 = st.selectbox("Select Second Actor", remaining, key="conv_actor2")

            iso1 = country_to_iso.get(actor1, actor1)
            iso2 = country_to_iso.get(actor2, actor2)
        else:
            actor1, actor2 = display_actors[0], display_actors[1]
            iso1 = country_to_iso.get(actor1, actor1)
            iso2 = country_to_iso.get(actor2, actor2)

        try:
            convergence = bach_api.predict_convergence_timeline(iso1, iso2, selected_policy)

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Expected Rounds to Convergence", convergence["expected_rounds"])
            with col2:
                st.metric("Success Probability", f"{convergence['probability_success']:.1%}")
            with col3:
                st.metric("Initial Ethical Gap", f"{convergence['initial_gap']:.3f}")

            if convergence["trajectory"]:
                traj_df = pd.DataFrame(convergence["trajectory"])
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=traj_df["round"],
                    y=traj_df["position_a"],
                    mode='lines+markers',
                    name=f"{actor1} Position",
                    line=dict(color='blue', width=3)
                ))
                fig.add_trace(go.Scatter(
                    x=traj_df["round"],
                    y=traj_df["position_b"],
                    mode='lines+markers',
                    name=f"{actor2} Position",
                    line=dict(color='red', width=3)
                ))
                fig.add_trace(go.Scatter(
                    x=traj_df["round"],
                    y=traj_df["gap"],
                    mode='lines+markers',
                    name="Remaining Gap",
                    line=dict(color='green', width=2, dash='dash')
                ))
                fig.update_layout(
                    title=f"Convergence Trajectory: {actor1} ↔ {actor2}",
                    xaxis_title="Negotiation Round",
                    yaxis_title="Position/Gap",
                    hovermode='x unified'
                )
                st.plotly_chart(fig, use_container_width=True)
                st.dataframe(traj_df, use_container_width=True)

            # For multilateral, show convergence matrix
            if len(display_actors) > 2:
                st.subheader("🔄 Multilateral Convergence Matrix")
                st.info("Pairwise convergence difficulty between all actors")

                matrix_data = []
                for a1 in display_actors:
                    row = {"Actor": a1}
                    for a2 in display_actors:
                        if a1 == a2:
                            row[a2] = "-"
                        else:
                            try:
                                iso_a1 = country_to_iso.get(a1, a1)
                                iso_a2 = country_to_iso.get(a2, a2)
                                conv = bach_api.predict_convergence_timeline(iso_a1, iso_a2, selected_policy)
                                row[a2] = f"{conv['expected_rounds']} rounds ({conv['probability_success']:.0%})"
                            except:
                                row[a2] = "N/A"
                    matrix_data.append(row)

                st.dataframe(matrix_data, use_container_width=True)

        except Exception as e:
            st.error(f"❌ Error predicting convergence: {str(e)}")

# TAB 3: Hierarchical Capability Gap Analysis
with tab3:
    st.header("3️⃣ Hierarchical Capability Gap Diagnosis")
    st.markdown("*Identifies specific capability bottlenecks blocking governance maturity*")

    target = st.slider("Target g-GWC (Global Governance Capability)", 0.5, 1.0, 0.8, 0.05)

    gap = bach_api.diagnose_capability_gap(iso_a, target)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Current g-GWC", f"{gap['current_gwc']:.3f}")
    with col2:
        st.metric("Capability Gap", f"{gap['gap']:.3f}", delta=f"-{gap['gap']:.1%}")

    st.info(f"**Status:** {gap['status']}")

    if gap['priorities']:
        st.subheader("🎯 Investment Priorities")

        for p in gap['priorities']:
            with st.expander(f"Priority #{p['investment_priority']}: {p['capability']} (Gap Contribution: {p['gap_contribution']:.1f}%)"):
                st.write(f"**Current Score:** {p['current_score']:.3f}")
                st.write("**Limiting Factors:**")
                for factor in p['limiting_factors']:
                    st.write(f"  - {factor['factor']}: {factor['score']:.3f}")

        # Visualization
        priority_data = pd.DataFrame(gap['priorities'])
        fig = px.bar(
            priority_data,
            x='capability',
            y='gap_contribution',
            title="Capability Gap Contributions",
            labels={'gap_contribution': 'Gap Contribution (%)', 'capability': 'Capability Domain'}
        )
        st.plotly_chart(fig, use_container_width=True)

# TAB 4: Multi-Objective Pareto Optimization
with tab4:
    st.header("4️⃣ Multi-Objective Pareto Optimization")
    st.markdown("*Identifies optimal policy scenarios across multiple competing objectives*")

    policy_options = ["AI Ethics", "AI Safety", "Data Privacy", "Export Controls", "R&D Investment"]

    with st.spinner("Computing Pareto frontier..."):
        pareto = bach_api.compute_pareto_scenarios(iso_a, iso_b, policy_options)

    all_df = pd.DataFrame(pareto["all_scenarios"])
    pareto_df = pd.DataFrame(pareto["pareto_optimal"])

    # 3D Scatter Plot
    fig = go.Figure()

    # Non-Pareto scenarios
    fig.add_trace(go.Scatter3d(
        x=all_df["ethical_alignment"],
        y=all_df["privacy_protection"],
        z=all_df["speed_to_agreement"],
        mode='markers',
        marker=dict(size=5, color='lightgray', opacity=0.5),
        text=all_df["policy"],
        name="All Scenarios"
    ))

    # Pareto-optimal scenarios
    fig.add_trace(go.Scatter3d(
        x=pareto_df["ethical_alignment"],
        y=pareto_df["privacy_protection"],
        z=pareto_df["speed_to_agreement"],
        mode='markers',
        marker=dict(size=10, color=pareto_df["composite_score"], colorscale='Viridis', showscale=True),
        text=pareto_df["policy"],
        name="Pareto Optimal"
    ))

    fig.update_layout(
        title="3D Pareto Frontier",
        scene=dict(
            xaxis_title="Ethical Alignment",
            yaxis_title="Privacy Protection",
            zaxis_title="Speed to Agreement"
        )
    )
    st.plotly_chart(fig, use_container_width=True)

    # Recommendation
    rec = pareto["recommendation"]
    st.success(f"🎯 **Recommended Policy:** {rec['policy']}")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Ethical Alignment", f"{rec['ethical_alignment']:.3f}")
    with col2:
        st.metric("Privacy Protection", f"{rec['privacy_protection']:.3f}")
    with col3:
        st.metric("Speed to Agreement", f"{rec['speed_to_agreement']:.3f}")
    with col4:
        st.metric("Innovation Potential", f"{rec['innovation_potential']:.3f}")

    st.dataframe(pareto_df, use_container_width=True)

# TAB 5: Network Diffusion Simulation
with tab5:
    st.header("5️⃣ Policy Diffusion & Network Cascade Effects")
    st.markdown("*Simulates how policies spread through international influence networks*")

    all_countries = ["USA", "GBR", "CHN", "JPN", "IND", "BRA", "ARE"]
    initial_adopters = st.multiselect(
        "Select Initial Policy Adopters",
        all_countries,
        default=[iso_a]
    )

    col1, col2 = st.columns(2)
    with col1:
        rounds = st.slider("Simulation Rounds", 5, 20, 10)
    with col2:
        influence = st.slider("Influence Strength", 0.1, 0.5, 0.3, 0.05)

    if st.button("🚀 Run Diffusion Simulation"):
        with st.spinner("Simulating policy diffusion..."):
            diffusion = bach_api.simulate_policy_diffusion(initial_adopters, selected_policy, rounds, influence)

        st.metric("Network Cascade Probability", f"{diffusion['cascade_probability']:.1%}")

        # Trajectory visualization
        traj_data = []
        for round_idx, state in enumerate(diffusion['trajectory']):
            for country, adoption in state.items():
                traj_data.append({
                    'Round': round_idx,
                    'Country': country,
                    'Adoption': adoption
                })

        traj_df = pd.DataFrame(traj_data)

        fig = px.line(
            traj_df,
            x='Round',
            y='Adoption',
            color='Country',
            title="Policy Adoption Diffusion Over Time"
        )
        st.plotly_chart(fig, use_container_width=True)

        # Final adoption state
        st.subheader("📊 Final Adoption State")
        final_df = pd.DataFrame([
            {"Country": k, "Adoption Rate": f"{v:.1%}", "Status": "Adopted" if v > 0.5 else "Pending"}
            for k, v in diffusion['final_adoption'].items()
        ]).sort_values('Adoption Rate', ascending=False)

        st.dataframe(final_df, use_container_width=True)

        # Tipping points
        if diffusion['tipping_rounds']:
            st.subheader("⚡ Tipping Points")
            tip_df = pd.DataFrame([
                {"Country": k, "Tipping Round": v}
                for k, v in diffusion['tipping_rounds'].items()
            ]).sort_values('Tipping Round')
            st.dataframe(tip_df)

# TAB 6: Historical Pattern Matching
with tab6:
    st.header("6️⃣ Historical Scenario Pattern Matching")
    st.markdown("*Learns from past negotiations to predict outcomes*")

    st.subheader("🔍 Current Negotiation Context")

    col1, col2, col3 = st.columns(3)
    with col1:
        power = st.slider("Power Asymmetry", 0.0, 1.0, 0.6, 0.05)
    with col2:
        salience = st.slider("Issue Salience", 0.0, 1.0, 0.8, 0.05)
    with col3:
        pressure = st.slider("Time Pressure", 0.0, 1.0, 0.7, 0.05)

    if st.button("🔎 Find Historical Matches"):
        matches = bach_api.match_historical_scenarios(
            [selected_country_a, selected_country_b],
            power,
            salience,
            pressure
        )

        st.subheader("📚 Top Historical Precedents")

        for i, match in enumerate(matches, 1):
            with st.expander(f"#{i}: {match['scenario']} (Relevance: {match['relevance']:.1%})"):
                col1, col2 = st.columns(2)

                with col1:
                    st.write(f"**Similarity Score:** {match['similarity']:.1%}")
                    st.write(f"**Actors Involved:** {', '.join(match['actors'])}")
                    st.write(f"**Outcome:** {match['outcome'].replace('_', ' ').title()}")

                with col2:
                    st.write(f"**Historical Success Rate:** {match['success_rate']:.1%}")
                    st.info(f"**Key Lesson:** {match['key_lesson']}")

        # Visualization
        match_df = pd.DataFrame(matches)
        fig = px.bar(
            match_df,
            x='scenario',
            y='relevance',
            color='success_rate',
            title="Historical Scenario Relevance",
            labels={'relevance': 'Relevance Score', 'scenario': 'Historical Scenario'}
        )
        st.plotly_chart(fig, use_container_width=True)

# TAB 7: Maturity Trajectory Planning
with tab7:
    st.header("7️⃣ Capability Maturity Trajectory Planning")
    st.markdown("*Projects governance maturity growth with resource investment models*")

    col1, col2 = st.columns(2)
    with col1:
        target_maturity = st.slider("Target Maturity Level", 1, 4, 3)
    with col2:
        investment = st.slider("Monthly Investment ($M)", 0.5, 5.0, 1.0, 0.5)

    months = st.slider("Planning Horizon (Months)", 12, 48, 24)

    if st.button("📊 Calculate Trajectory"):
        with st.spinner("Computing maturity trajectory..."):
            trajectory = bach_api.calculate_maturity_trajectory(
                iso_a,
                target_maturity,
                investment,
                months
            )

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Current Maturity", trajectory['current_maturity'])
        with col2:
            st.metric("Months to Target", trajectory['months_to_target'])
        with col3:
            st.metric("Total Investment", f"${trajectory['total_investment_required']:.1f}M")

        st.info(f"🎯 **Critical Milestone:** Month {trajectory['critical_milestone_month']}")

        # Trajectory visualization
        traj_df = pd.DataFrame(trajectory['trajectory'])

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=traj_df['month'],
            y=traj_df['maturity'],
            mode='lines+markers',
            name='Maturity Level',
            line=dict(color='blue', width=3)
        ))
        fig.add_hline(
            y=target_maturity,
            line_dash="dash",
            line_color="red",
            annotation_text="Target"
        )
        fig.update_layout(
            title=f"Maturity Growth Trajectory for {selected_country_a}",
            xaxis_title="Month",
            yaxis_title="Maturity Level"
        )
        st.plotly_chart(fig, use_container_width=True)

        st.dataframe(traj_df, use_container_width=True)

# TAB 8: Kalman Filter Tracking
with tab8:
    st.header("8️⃣ Kalman Filter Capability Tracking")
    st.markdown("*Real-time state estimation with uncertainty management*")

    if st.button("🎯 Initialize Kalman Filter"):
        bach_api.initialize_kalman_filter(iso_a)
        st.success(f"✅ Kalman filter initialized for {selected_country_a}")

    if iso_a in bach_api.kalman_states:
        st.subheader("📡 Current Filter State")
        state = bach_api.kalman_states[iso_a]

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Current Estimate", f"{state['x_hat']:.3f}")
        with col2:
            st.metric("Uncertainty (P)", f"{state['P']:.4f}")

        st.subheader("🔄 Update Filter")
        col1, col2 = st.columns(2)
        with col1:
            new_measurement = st.slider("New Capability Measurement", 0.0, 1.0, 0.7, 0.01)
        with col2:
            intervention = st.slider("Intervention Effect", 0.0, 0.5, 0.1, 0.01)

        if st.button("📊 Update Kalman Filter"):
            result = bach_api.kalman_update(iso_a, new_measurement, intervention)

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Smoothed Estimate", f"{result['smoothed_estimate']:.3f}")
            with col2:
                st.metric("Uncertainty", f"{result['uncertainty']:.4f}")
            with col3:
                st.metric("Confidence", f"{result['confidence']:.1f}%")

        # History visualization
        if len(state['history']) > 1:
            history_df = pd.DataFrame(state['history'], columns=['Step', 'Estimate', 'Uncertainty'])

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=history_df['Step'],
                y=history_df['Estimate'],
                mode='lines+markers',
                name='Capability Estimate',
                error_y=dict(
                    type='data',
                    array=history_df['Uncertainty'],
                    visible=True
                )
            ))
            fig.update_layout(
                title="Kalman Filter Tracking History",
                xaxis_title="Update Step",
                yaxis_title="Capability Estimate"
            )
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("👆 Click 'Initialize Kalman Filter' to begin tracking")

# TAB 9: RL Strategy Optimization
with tab9:
    st.header("9️⃣ Reinforcement Learning Strategy Optimization")
    st.markdown("*Q-learning based negotiation strategy discovery*")

    num_sims = st.slider("Number of Simulations", 50, 500, 100, 50)

    if st.button("🤖 Discover Optimal Strategy"):
        with st.spinner("Running RL simulations..."):
            strategy = bach_api.optimize_negotiation_strategy(
                iso_a,
                iso_b,
                selected_policy,
                num_sims
            )

        st.success(f"🎯 **Recommended First Move:** {strategy['recommended_first_move']}")
        st.info(f"💡 **Strategy Rationale:** {strategy['explanation']}")

        st.metric(
            "Expected Agreement Probability",
            f"{strategy['expected_agreement_probability']:.1%}"
        )

        st.subheader("📊 Action Value Estimates (Q-Values)")

        q_df = pd.DataFrame([
            {"Action": k, "Q-Value": v, "Rank": i+1}
            for i, (k, v) in enumerate(sorted(strategy['q_values'].items(), key=lambda x: x[1], reverse=True))
        ])

        fig = px.bar(
            q_df,
            x='Action',
            y='Q-Value',
            color='Q-Value',
            title="Negotiation Action Q-Values",
            color_continuous_scale='RdYlGn'
        )
        st.plotly_chart(fig, use_container_width=True)

        st.dataframe(q_df, use_container_width=True)

        st.subheader("🎲 Optimal Action Sequence")
        for i, action in enumerate(strategy['optimal_action_sequence'], 1):
            st.write(f"{i}. **{action.replace('_', ' ').title()}**")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 20px;'>
    <h3>🎼 Auracelle Bach | Complete E-AGPO-HT Mathematical Suite</h3>
    <p><strong>9 Mathematical Enhancements Active</strong></p>
    print("   🧠 Cognitive Architecture: Moral Foundations + Trust Dynamics")
    <p style='font-size: 12px;'>Bayesian • Convergence • Gap Analysis • Pareto • Diffusion • Historical • Maturity • Kalman • RL</p>
</div>
""", unsafe_allow_html=True)
