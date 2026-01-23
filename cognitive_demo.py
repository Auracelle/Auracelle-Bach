import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from moral_foundations import (
    MoralFoundations, PolicyFeatures, MoralEvaluator,
    MoralExplainer, STAKEHOLDER_PROFILES
)
from trust_dynamics import (
    TrustState, TrustDynamicsEngine, CoalitionManager,
    TrustBasedPolicyNegotiation, InteractionRecord, InteractionType
)

# Note: st.set_page_config is called in app.py, not in pages

# Password protection
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    password = st.text_input("Enter password:", type="password")
    if st.button("Login"):
        if password == "charlie2025":
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Incorrect password")
    st.stop()

# Header
st.title("🧠 Cognitive Architecture Demonstration")
st.markdown("""
This module demonstrates **human-inspired reasoning** in AI governance simulations through:
- 🎯 **Moral Foundations**: Computational ethics based on Haidt's theory
- 🤝 **Trust Dynamics**: Cooperation mechanisms from Ostrom/Axelrod research
- 🔄 **Value-Weighted Decisions**: Combining strategy, ethics, and social relationships
""")

# Tabs for different demonstrations
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Moral Foundations",
    "🤝 Trust Dynamics",
    "🎯 Integrated Agents",
    "📈 Simulation Results"
])

# =============================================================================
# TAB 1: MORAL FOUNDATIONS DEMO
# =============================================================================

with tab1:
    st.header("Moral Foundations Analysis")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Define Policy")

        policy_name = st.text_input("Policy Name", "GDPR-Style Privacy Regulation")

        st.markdown("### Policy Attributes (0-1 scale)")

        # Care/Harm dimensions
        with st.expander("🏥 Care/Harm Dimensions", expanded=True):
            safety_req = st.slider("Safety Requirements", 0.0, 1.0, 0.85, 0.05)
            privacy_safe = st.slider("Privacy Safeguards", 0.0, 1.0, 0.90, 0.05)
            vulnerable_prot = st.slider("Vulnerable Protection", 0.0, 1.0, 0.80, 0.05)

        # Fairness dimensions
        with st.expander("⚖️ Fairness Dimensions"):
            equity_prov = st.slider("Equity Provisions", 0.0, 1.0, 0.75, 0.05)
            proc_fair = st.slider("Procedural Fairness", 0.0, 1.0, 0.80, 0.05)
            small_burden = st.slider("Small Actor Burden", 0.0, 1.0, 0.65, 0.05)

        # Authority dimensions
        with st.expander("🏛️ Authority Dimensions"):
            inst_clarity = st.slider("Institutional Clarity", 0.0, 1.0, 0.85, 0.05)
            reg_strength = st.slider("Regulatory Strength", 0.0, 1.0, 0.90, 0.05)

        # Sanctity dimensions
        with st.expander("✨ Sanctity Dimensions"):
            human_dig = st.slider("Human Dignity", 0.0, 1.0, 0.90, 0.05)
            priv_sanct = st.slider("Privacy Sanctity", 0.0, 1.0, 0.95, 0.05)

        policy = PolicyFeatures(
            policy_id="DEMO",
            policy_name=policy_name,
            policy_type="regulation",
            safety_requirements=safety_req,
            privacy_safeguards=privacy_safe,
            vulnerable_protection=vulnerable_prot,
            equity_provisions=equity_prov,
            procedural_fairness=proc_fair,
            small_actor_burden=small_burden,
            institutional_clarity=inst_clarity,
            regulatory_strength=reg_strength,
            human_dignity=human_dig,
            privacy_sanctity=priv_sanct
        )

    with col2:
        st.subheader("Stakeholder Evaluations")

        evaluator = MoralEvaluator(scenario_context="data_privacy")
        explainer = MoralExplainer(evaluator)

        # Select stakeholders to compare
        selected_stakeholders = st.multiselect(
            "Compare Stakeholders",
            options=list(STAKEHOLDER_PROFILES.keys()),
            default=["consumer_advocacy_ngo", "tech_industry_association",
                    "progressive_government", "academic_ethics_board"]
        )

        if selected_stakeholders:
            # Compute moral values
            results = []
            for stakeholder_key in selected_stakeholders:
                foundations = STAKEHOLDER_PROFILES[stakeholder_key]
                moral_value = evaluator.compute_moral_value(policy, foundations)
                results.append({
                    'Stakeholder': stakeholder_key.replace('_', ' ').title(),
                    'Moral Value': moral_value,
                    'Stance': 'Support' if moral_value > 0 else 'Oppose'
                })

            results_df = pd.DataFrame(results)

            # Visualization
            fig = px.bar(
                results_df,
                x='Stakeholder',
                y='Moral Value',
                color='Moral Value',
                color_continuous_scale='RdYlGn',
                range_color=[-1, 1],
                title="Moral Evaluation by Stakeholder"
            )
            fig.add_hline(y=0, line_dash="dash", line_color="gray")
            st.plotly_chart(fig, use_container_width=True)

            # Detailed explanations
            st.markdown("### Detailed Reasoning")

            selected_for_detail = st.selectbox(
                "View detailed explanation for:",
                options=selected_stakeholders,
                format_func=lambda x: x.replace('_', ' ').title()
            )

            if selected_for_detail:
                foundations = STAKEHOLDER_PROFILES[selected_for_detail]
                explanation = explainer.explain_evaluation(
                    policy,
                    foundations,
                    agent_name=selected_for_detail.replace('_', ' ').title()
                )
                st.code(explanation, language="text")

# =============================================================================
# TAB 2: TRUST DYNAMICS DEMO
# =============================================================================

with tab2:
    st.header("Trust Evolution Simulation")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Configure Interaction")

        agent_a = st.selectbox("Agent A", ["Government", "TechCorp", "ConsumerNGO", "StandardsBody"])
        agent_b = st.selectbox("Agent B", ["Government", "TechCorp", "ConsumerNGO", "StandardsBody"], index=1)

        interaction_type = st.select_slider(
            "Interaction Type",
            options=["Strong Defection", "Mild Defection", "Neutral", "Mild Cooperation", "Strong Cooperation"],
            value="Mild Cooperation"
        )

        # Map interaction type to numerical values
        type_map = {
            "Strong Defection": (0.2, -0.7),
            "Mild Defection": (0.4, -0.3),
            "Neutral": (0.5, 0.0),
            "Mild Cooperation": (0.7, 0.4),
            "Strong Cooperation": (0.9, 0.7)
        }

        cooperation_level, outcome = type_map[interaction_type]

        num_rounds = st.slider("Number of Rounds", 1, 20, 10)

        if st.button("Run Trust Simulation"):
            # Initialize trust states
            trust_states = {
                agent_a: TrustState(agent_id=agent_a, baseline_trust=0.5),
                agent_b: TrustState(agent_id=agent_b, baseline_trust=0.5)
            }

            engine = TrustDynamicsEngine()

            # Track trust evolution
            trust_history = []

            for round_num in range(num_rounds):
                # Create interaction
                interaction = InteractionRecord(
                    timestep=round_num,
                    agent_i=agent_a,
                    agent_j=agent_b,
                    interaction_type=InteractionType.NEGOTIATION,
                    outcome_for_i=outcome + np.random.normal(0, 0.1),
                    outcome_for_j=outcome + np.random.normal(0, 0.1),
                    cooperation_level=cooperation_level + np.random.normal(0, 0.05)
                )

                # Update trust
                new_trust_ab = engine.update_trust_from_interaction(
                    trust_states[agent_a], agent_b, interaction
                )

                new_trust_ba = engine.update_trust_from_interaction(
                    trust_states[agent_b], agent_a, interaction
                )

                # Apply decay
                engine.decay_trust_and_reciprocity(trust_states[agent_a])
                engine.decay_trust_and_reciprocity(trust_states[agent_b])

                trust_history.append({
                    'Round': round_num + 1,
                    f'{agent_a} → {agent_b}': new_trust_ab,
                    f'{agent_b} → {agent_a}': new_trust_ba
                })

            # Store in session state
            st.session_state.trust_history = trust_history
            st.session_state.trust_states = trust_states

    with col2:
        st.subheader("Trust Evolution Over Time")

        if 'trust_history' in st.session_state:
            trust_df = pd.DataFrame(st.session_state.trust_history)

            fig = go.Figure()

            fig.add_trace(go.Scatter(
                x=trust_df['Round'],
                y=trust_df[f'{agent_a} → {agent_b}'],
                mode='lines+markers',
                name=f'{agent_a} → {agent_b}'
            ))

            fig.add_trace(go.Scatter(
                x=trust_df['Round'],
                y=trust_df[f'{agent_b} → {agent_a}'],
                mode='lines+markers',
                name=f'{agent_b} → {agent_a}'
            ))

            fig.update_layout(
                title="Trust Level Evolution",
                xaxis_title="Round",
                yaxis_title="Trust Level",
                yaxis_range=[0, 1],
                hovermode='x unified'
            )

            st.plotly_chart(fig, use_container_width=True)

            # Final stats
            st.markdown("### Final Trust State")

            final_trust_ab = trust_df[f'{agent_a} → {agent_b}'].iloc[-1]
            final_trust_ba = trust_df[f'{agent_b} → {agent_a}'].iloc[-1]

            col_a, col_b = st.columns(2)

            with col_a:
                st.metric(
                    f"{agent_a} trusts {agent_b}",
                    f"{final_trust_ab:.2f}",
                    delta=f"{final_trust_ab - 0.5:+.2f} from baseline"
                )

            with col_b:
                st.metric(
                    f"{agent_b} trusts {agent_a}",
                    f"{final_trust_ba:.2f}",
                    delta=f"{final_trust_ba - 0.5:+.2f} from baseline"
                )

# =============================================================================
# TAB 3: INTEGRATED AGENTS
# =============================================================================

with tab3:
    st.header("Integrated Cognitive Agents")
    st.markdown("""
    This demonstrates how cognitive architecture combines:
    1. **Strategic Value** (game-theoretic payoffs)
    2. **Moral Value** (ethical alignment)
    3. **Social Value** (trust and reciprocity)
    """)

    # Agent configuration
    st.subheader("Agent Configuration")

    col1, col2 = st.columns(2)

    with col1:
        agent_profile = st.selectbox(
            "Select Stakeholder Profile",
            options=list(STAKEHOLDER_PROFILES.keys()),
            format_func=lambda x: x.replace('_', ' ').title()
        )

        # Show moral foundations profile
        st.markdown("#### Moral Foundations Profile")

        foundations = STAKEHOLDER_PROFILES[agent_profile]
        found_dict = foundations.to_dict()

        fig = go.Figure()

        fig.add_trace(go.Scatterpolar(
            r=list(found_dict.values()),
            theta=[k.replace('_', '/').title() for k in found_dict.keys()],
            fill='toself',
            name=agent_profile.replace('_', ' ').title()
        ))

        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 0.5])),
            showlegend=False,
            height=400
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### Decision Weight Configuration")

        instrumental_w = st.slider("Instrumental Weight", 0.0, 1.0, 0.6, 0.05)
        moral_w = st.slider("Moral Weight", 0.0, 1.0, 0.3, 0.05)
        social_w = st.slider("Social Weight", 0.0, 1.0, 0.1, 0.05)

        # Normalize
        total = instrumental_w + moral_w + social_w
        if total > 0:
            instrumental_w /= total
            moral_w /= total
            social_w /= total

        st.markdown(f"""
        **Normalized Weights:**
        - Instrumental: {instrumental_w:.2f}
        - Moral: {moral_w:.2f}
        - Social: {social_w:.2f}
        """)

# =============================================================================
# TAB 4: SIMULATION RESULTS
# =============================================================================

with tab4:
    st.header("Simulation Results")

    st.info("🚧 Run a full multi-agent simulation from the main Simulation page to see results here.")

    st.markdown("""
    ### What Gets Tracked:
    - **Policy Consensus**: How much agents agree on policies over time
    - **Trust Network Evolution**: Changes in trust relationships
    - **Coalition Formation**: When agents form alliances
    - **Moral Polarization**: Diversity of values in the network
    - **Decision Explanations**: Natural language justifications for choices
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 20px;'>
    <h3>🧠 Auracelle Bach | Cognitive Architecture Module</h3>
    <p><strong>Human-Inspired Governance Simulation</strong></p>
    <p style='font-size: 12px;'>Moral Foundations • Trust Dynamics • Value-Weighted Decisions</p>
</div>
""", unsafe_allow_html=True)
