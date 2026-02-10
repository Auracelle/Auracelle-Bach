import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from scipy import stats

st.set_page_config(page_title="COGNITIVE DECISION SCIENCE", page_icon="🧮", layout="wide")

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
st.title("🧮 Cognitive Decision Science")
st.markdown("""
This module implements the **E-AGPO-HT Mathematical Framework** for decision-making under uncertainty
in AI governance scenarios. Based on formal mathematical formulations integrating Bayesian reasoning,
game theory, and multi-agent optimization.
""")

# Sidebar - Mathematical Framework Overview
with st.sidebar:
    st.markdown("---")
    st.markdown("### 📐 E-AGPO-HT Framework")
    st.markdown("""
    **Three-Stratum Architecture:**
    - **Stratum III:** g-GWC (Global Wargaming Coordinator)
    - **Stratum II:** 7 BGC Components
    - **Stratum I:** ~40 NOF (Numerical Observable Features)

    **Core Components:**
    - Bayesian Uncertainty Quantification
    - Nash Equilibrium Computation
    - Multi-Objective Optimization
    - Stage-Based Policy Development
    """)

# Main tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🎲 Decision Under Uncertainty",
    "🎯 Nash Equilibrium",
    "⚖️ Multi-Objective Optimization",
    "⏱️ Policy Development Timeline",
    "📊 Reliability Metrics"
])

# =============================================================================
# TAB 1: Decision Under Uncertainty
# =============================================================================

with tab1:
    st.header("Decision-Making Under Uncertainty")

    st.info("""
    **Mathematical Foundation:** Decision science combines game theory, behavioral economics, and
    organizational decision-making to model strategic choices by academic institutions and civil
    society organizations in AI governance.
    """)

    # Mathematical Formulation
    with st.expander("📐 Mathematical Formulation", expanded=True):
        st.latex(r"""
        U_i(a_i, a_{-i}) = \sum_{j \in \Omega} p_j(a) \times \left[r_{i,j} + \beta_i \times \sum_{k=1}^{\infty} \delta^k E[r_{i,t+k}]\right]
        """)

        st.markdown("""
        **Where:**
        - `U_i` = Utility for actor i (academic institution, civil society org)
        - `a_i` = Action choice for actor i
        - `a_{-i}` = Actions of all other actors
        - `p_j(a)` = Probability of outcome j given action profile a
        - `r_i,j` = Immediate reward for actor i in outcome j
        - `β_i` = Future orientation discount factor
        - `δ` = Temporal discount rate
        - `E[r_i,t+k]` = Expected future rewards k periods ahead
        - `Ω` = Outcome space
        """)

        st.markdown("---")
        st.markdown("#### Nash Equilibrium Condition")
        st.latex(r"""
        a^* = Nash(U_1, U_2, ..., U_n) \text{ where } \forall i: \frac{\partial U_i}{\partial a_i} = 0
        """)

    # Interactive Decision Scenario
    st.subheader("🎮 Interactive Decision Scenario")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### Scenario Parameters")

        num_actors = st.slider("Number of Actors", 2, 5, 3)
        time_horizon = st.slider("Time Horizon (periods)", 1, 10, 5)
        discount_rate = st.slider("Discount Rate (δ)", 0.0, 1.0, 0.9, 0.05)

        actor_types = []
        for i in range(num_actors):
            st.markdown(f"**Actor {i+1}:**")
            actor_type = st.selectbox(
                f"Type",
                ["Academic Institution", "Civil Society Org", "Government Agency", "Tech Company"],
                key=f"actor_type_{i}"
            )
            future_orientation = st.slider(
                f"Future Orientation (β)",
                0.0, 1.0, 0.7, 0.05,
                key=f"beta_{i}"
            )
            actor_types.append({
                'name': f"Actor {i+1}",
                'type': actor_type,
                'beta': future_orientation
            })

    with col2:
        st.markdown("### Decision Outcomes")

        # Simulate decision outcomes
        np.random.seed(42)

        outcomes = []
        for actor in actor_types:
            # Immediate reward
            immediate_reward = np.random.uniform(0.3, 0.8)

            # Future rewards with discount
            future_rewards = []
            for k in range(1, time_horizon + 1):
                expected_future = np.random.uniform(0.2, 0.7)
                discounted = (discount_rate ** k) * expected_future
                future_rewards.append(discounted)

            total_future = sum(future_rewards)

            # Total utility
            total_utility = immediate_reward + actor['beta'] * total_future

            outcomes.append({
                'Actor': actor['name'],
                'Type': actor['type'],
                'Immediate Reward': immediate_reward,
                'Future Value': total_future,
                'Total Utility': total_utility
            })

        df_outcomes = pd.DataFrame(outcomes)

        # Display results
        st.dataframe(df_outcomes.style.background_gradient(subset=['Total Utility'], cmap='Greens'))

        # Visualization
        fig = go.Figure()

        fig.add_trace(go.Bar(
            name='Immediate Reward',
            x=df_outcomes['Actor'],
            y=df_outcomes['Immediate Reward'],
            marker_color='#667eea'
        ))

        fig.add_trace(go.Bar(
            name='Future Value',
            x=df_outcomes['Actor'],
            y=df_outcomes['Future Value'],
            marker_color='#764ba2'
        ))

        fig.update_layout(
            barmode='stack',
            title="Utility Decomposition by Actor",
            xaxis_title="Actor",
            yaxis_title="Utility Value",
            height=400
        )

        st.plotly_chart(fig, use_container_width=True)

    # Strategic Insights
    st.markdown("---")
    st.subheader("💡 Strategic Insights")

    best_actor = df_outcomes.loc[df_outcomes['Total Utility'].idxmax()]
    worst_actor = df_outcomes.loc[df_outcomes['Total Utility'].idxmin()]

    col1, col2 = st.columns([1, 1])

    with col1:
        st.success(f"""
        **Highest Utility: {best_actor['Actor']}**

        - Type: {best_actor['Type']}
        - Total Utility: {best_actor['Total Utility']:.3f}
        - Immediate: {best_actor['Immediate Reward']:.3f}
        - Future: {best_actor['Future Value']:.3f}

        **Strategy:** This actor successfully balances short-term gains with long-term strategic positioning.
        """)

    with col2:
        st.warning(f"""
        **Needs Optimization: {worst_actor['Actor']}**

        - Type: {worst_actor['Type']}
        - Total Utility: {worst_actor['Total Utility']:.3f}
        - Immediate: {worst_actor['Immediate Reward']:.3f}
        - Future: {worst_actor['Future Value']:.3f}

        **Recommendation:** Increase future orientation (β) or identify higher-value strategic opportunities.
        """)

# =============================================================================
# TAB 2: Nash Equilibrium
# =============================================================================

with tab2:
    st.header("Nash Equilibrium Computation")

    st.info("""
    **Nash Equilibrium:** A stable state where no actor can improve their utility by unilaterally
    changing their strategy, given the strategies of other actors.
    """)

    # Mathematical formulation
    with st.expander("📐 Nash Equilibrium Conditions", expanded=True):
        st.latex(r"""
        a^* \in NE \Leftrightarrow \forall i, \forall a_i': U_i(a^*_i, a^*_{-i}) \geq U_i(a'_i, a^*_{-i})
        """)

        st.markdown("""
        **Interpretation:**
        - Strategy profile `a*` is a Nash Equilibrium if no player i can improve by deviating
        - Each player's strategy is a best response to others' strategies
        - Multiple equilibria may exist
        """)

    # 2x2 Game Matrix Example
    st.subheader("🎮 2-Player Governance Game")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### Game Configuration")

        player1_name = st.text_input("Player 1 (Academic Institution)", "University Research Lab")
        player2_name = st.text_input("Player 2 (Civil Society)", "AI Ethics NGO")

        st.markdown("**Player 1 Strategies:**")
        p1_s1 = st.text_input("Strategy A", "Publish immediately", key="p1s1")
        p1_s2 = st.text_input("Strategy B", "Coordinate disclosure", key="p1s2")

        st.markdown("**Player 2 Strategies:**")
        p2_s1 = st.text_input("Strategy A", "Launch campaign now", key="p2s1")
        p2_s2 = st.text_input("Strategy B", "Wait for research", key="p2s2")

    with col2:
        st.markdown("### Payoff Matrix")
        st.markdown("*Enter payoffs as (Player 1, Player 2)*")

        # Payoff matrix inputs
        col_a, col_b = st.columns(2)

        with col_a:
            st.markdown(f"**{player2_name}: {p2_s1}**")
            aa = st.text_input("If both choose A", "6, 5", key="aa")
            ba = st.text_input(f"If P1:{p1_s2}, P2:{p2_s1}", "4, 7", key="ba")

        with col_b:
            st.markdown(f"**{player2_name}: {p2_s2}**")
            ab = st.text_input(f"If P1:{p1_s1}, P2:{p2_s2}", "7, 4", key="ab")
            bb = st.text_input("If both choose B", "9, 8", key="bb")

        # Parse payoffs
        try:
            aa_p1, aa_p2 = map(float, aa.split(','))
            ab_p1, ab_p2 = map(float, ab.split(','))
            ba_p1, ba_p2 = map(float, ba.split(','))
            bb_p1, bb_p2 = map(float, bb.split(','))

            # Create payoff matrix visualization
            matrix_data = [
                [f"({aa_p1:.0f}, {aa_p2:.0f})", f"({ab_p1:.0f}, {ab_p2:.0f})"],
                [f"({ba_p1:.0f}, {ba_p2:.0f})", f"({bb_p1:.0f}, {bb_p2:.0f})"]
            ]

            df_matrix = pd.DataFrame(
                matrix_data,
                columns=[f"{player2_name}:<br>{p2_s1}", f"{player2_name}:<br>{p2_s2}"],
                index=[f"{player1_name}:<br>{p1_s1}", f"{player1_name}:<br>{p1_s2}"]
            )

            st.markdown("**Payoff Matrix:**")
            st.dataframe(df_matrix, use_container_width=True)

        except:
            st.error("Invalid payoff format. Use: number, number")

    # Nash Equilibrium Analysis
    st.markdown("---")
    st.subheader("🎯 Nash Equilibrium Analysis")

    try:
        # Check for Nash Equilibria
        equilibria = []

        # Check (A, A)
        if aa_p1 >= ba_p1 and aa_p2 >= ab_p2:
            equilibria.append("(A, A) - Both act immediately")

        # Check (A, B)
        if ab_p1 >= bb_p1 and ab_p2 >= aa_p2:
            equilibria.append("(A, B) - Mixed strategies")

        # Check (B, A)
        if ba_p1 >= aa_p1 and ba_p2 >= bb_p2:
            equilibria.append("(B, A) - Mixed strategies")

        # Check (B, B)
        if bb_p1 >= ab_p1 and bb_p2 >= ba_p2:
            equilibria.append("(B, B) - Both coordinate")

        if equilibria:
            st.success(f"""
            **Found {len(equilibria)} Nash Equilibrium/Equilibria:**

            """ + "\n".join([f"- {eq}" for eq in equilibria]))

            # Determine socially optimal outcome
            total_payoffs = {
                "(A, A)": aa_p1 + aa_p2,
                "(A, B)": ab_p1 + ab_p2,
                "(B, A)": ba_p1 + ba_p2,
                "(B, B)": bb_p1 + bb_p2
            }

            best_outcome = max(total_payoffs, key=total_payoffs.get)

            st.info(f"""
            **Socially Optimal Outcome:** {best_outcome}

            Total Payoff: {total_payoffs[best_outcome]:.1f}

            {"✅ This outcome is also a Nash Equilibrium!" if best_outcome.replace("(", "").replace(")", "").replace(", ", ", ") in [e.split(" - ")[0] for e in equilibria] else "⚠️ Warning: Social optimum may not be an equilibrium (coordination problem)"}
            """)
        else:
            st.warning("No pure strategy Nash Equilibrium found. Mixed strategy equilibrium may exist.")

    except:
        pass

# =============================================================================
# TAB 3: Multi-Objective Optimization
# =============================================================================

with tab3:
    st.header("Multi-Objective Optimization")

    st.info("""
    **Pareto Optimization:** Finding solutions where improving one objective cannot be done
    without worsening another. Critical for AI governance where multiple values compete.
    """)

    # Mathematical formulation
    with st.expander("📐 Pareto Optimality Conditions", expanded=True):
        st.latex(r"""
        x^* \text{ is Pareto optimal } \Leftrightarrow \nexists x: f_i(x) \geq f_i(x^*) \forall i \text{ and } f_j(x) > f_j(x^*) \text{ for some } j
        """)

        st.markdown("""
        **Multi-Objective Problem:**
        """)

        st.latex(r"""
        \begin{aligned}
        \text{maximize } & (f_1(x), f_2(x), ..., f_k(x)) \\
        \text{subject to } & g_i(x) \leq 0, \quad i = 1, ..., m \\
                            & h_j(x) = 0, \quad j = 1, ..., p
        \end{aligned}
        """)

    # Interactive Pareto Frontier
    st.subheader("📊 Pareto Frontier Visualization")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("### Objectives")

        obj1_name = st.text_input("Objective 1", "Innovation Speed")
        obj2_name = st.text_input("Objective 2", "Safety/Ethics")

        num_solutions = st.slider("Number of Candidate Solutions", 20, 100, 50)

        # Trade-off strength
        tradeoff = st.slider("Trade-off Intensity", 0.0, 1.0, 0.7, 0.1,
                            help="Higher = stronger trade-off between objectives")

    with col2:
        # Generate synthetic Pareto frontier
        np.random.seed(42)

        # Create candidate solutions
        obj1_values = np.random.uniform(0, 1, num_solutions)

        # Create trade-off (higher obj1 → lower obj2)
        noise = np.random.normal(0, 0.1, num_solutions)
        obj2_values = (1 - tradeoff * obj1_values) + noise
        obj2_values = np.clip(obj2_values, 0, 1)

        # Identify Pareto frontier
        pareto_mask = np.ones(num_solutions, dtype=bool)
        for i in range(num_solutions):
            for j in range(num_solutions):
                if i != j:
                    if (obj1_values[j] >= obj1_values[i] and obj2_values[j] >= obj2_values[i]) and                        (obj1_values[j] > obj1_values[i] or obj2_values[j] > obj2_values[i]):
                        pareto_mask[i] = False
                        break

        # Plot
        fig = go.Figure()

        # Non-Pareto points
        fig.add_trace(go.Scatter(
            x=obj1_values[~pareto_mask],
            y=obj2_values[~pareto_mask],
            mode='markers',
            name='Dominated Solutions',
            marker=dict(size=8, color='lightgray', opacity=0.5)
        ))

        # Pareto frontier
        pareto_x = obj1_values[pareto_mask]
        pareto_y = obj2_values[pareto_mask]
        sorted_indices = np.argsort(pareto_x)

        fig.add_trace(go.Scatter(
            x=pareto_x[sorted_indices],
            y=pareto_y[sorted_indices],
            mode='markers+lines',
            name='Pareto Frontier',
            marker=dict(size=12, color='#667eea'),
            line=dict(color='#667eea', width=2)
        ))

        fig.update_layout(
            title="Pareto Frontier: Innovation vs Safety Trade-off",
            xaxis_title=obj1_name,
            yaxis_title=obj2_name,
            height=500,
            hovermode='closest'
        )

        st.plotly_chart(fig, use_container_width=True)

    # Pareto solutions summary
    st.markdown("---")
    st.subheader("🎯 Pareto-Optimal Solutions")

    num_pareto = pareto_mask.sum()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Solutions", num_solutions)

    with col2:
        st.metric("Pareto-Optimal", num_pareto)

    with col3:
        efficiency = (num_pareto / num_solutions) * 100
        st.metric("Efficiency", f"{efficiency:.1f}%")

    st.info(f"""
    **Interpretation:**
    - {num_pareto} solutions lie on the Pareto frontier
    - These represent the best possible trade-offs between {obj1_name} and {obj2_name}
    - Decision-makers must choose based on value preferences
    - No solution on the frontier is objectively "better" than another
    """)

# =============================================================================
# TAB 4: Policy Development Timeline
# =============================================================================

with tab4:
    st.header("Policy Development Timeline (8-Stage Model)")

    st.info("""
    **E-AGPO-HT Stage Model:** Policy development proceeds through 8 distinct stages, each with
    baseline time and acceleration factors from g-GWC coordination.
    """)

    # Mathematical formulation
    with st.expander("📐 Stage-Specific Acceleration Formula", expanded=True):
        st.latex(r"""
        T_{AGPO}(stage_i) = T_{baseline}(stage_i) \cdot (1 - \alpha_i \cdot g\text{-}GWC)
        """)

        st.markdown("""
        **Where:**
        - `T_AGPO(stage_i)` = Accelerated time for stage i
        - `T_baseline(stage_i)` = Baseline time without coordination
        - `α_i` = Acceleration coefficient for stage i (see table below)
        - `g-GWC` = Global Wargaming Coordinator effectiveness (0-1)
        """)

        # Acceleration coefficients table
        stage_data = {
            'Stage': ['Identify', 'Secure', 'Investigate/Explore', 'Collaborate/Negotiate',
                     'Reason', 'Govern', 'Scale', 'Monitor/Measure'],
            'α (Acceleration)': [0.40, 0.35, 0.50, 0.45, 0.30, 0.25, 0.40, 0.35],
            'Typical Baseline (months)': [2, 3, 6, 8, 4, 12, 6, 'Ongoing']
        }

        df_stages = pd.DataFrame(stage_data)
        st.dataframe(df_stages, use_container_width=True)

    # Interactive timeline calculator
    st.subheader("⏱️ Timeline Calculator")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### Configuration")

        gwc_effectiveness = st.slider("g-GWC Effectiveness", 0.0, 1.0, 0.7, 0.05,
                                     help="Coordination effectiveness: 0 = no coordination, 1 = perfect")

        baseline_times = {}
        st.markdown("### Baseline Times (months)")
        for stage in stage_data['Stage'][:-1]:  # Exclude "Ongoing"
            idx = stage_data['Stage'].index(stage)
            default = stage_data['Typical Baseline (months)'][idx]
            baseline_times[stage] = st.number_input(
                stage,
                min_value=1,
                max_value=24,
                value=int(default),
                key=f"baseline_{stage}"
            )

    with col2:
        st.markdown("### Timeline Results")

        results = []
        total_baseline = 0
        total_agpo = 0

        for stage in baseline_times:
            idx = stage_data['Stage'].index(stage)
            alpha = stage_data['α (Acceleration)'][idx]

            baseline = baseline_times[stage]
            agpo_time = baseline * (1 - alpha * gwc_effectiveness)
            time_saved = baseline - agpo_time

            total_baseline += baseline
            total_agpo += agpo_time

            results.append({
                'Stage': stage,
                'Baseline': baseline,
                'AGPO Time': agpo_time,
                'Time Saved': time_saved,
                'Acceleration %': (time_saved / baseline) * 100
            })

        df_results = pd.DataFrame(results)

        # Display results
        st.dataframe(
            df_results.style.format({
                'Baseline': '{:.1f}',
                'AGPO Time': '{:.1f}',
                'Time Saved': '{:.1f}',
                'Acceleration %': '{:.1f}%'
            }).background_gradient(subset=['Acceleration %'], cmap='Greens'),
            use_container_width=True
        )

        # Total timeline comparison
        st.markdown("---")

        col_a, col_b, col_c = st.columns(3)

        with col_a:
            st.metric("Baseline Total", f"{total_baseline:.1f} mo")

        with col_b:
            st.metric("AGPO Total", f"{total_agpo:.1f} mo")

        with col_c:
            total_saved = total_baseline - total_agpo
            st.metric("Time Saved", f"{total_saved:.1f} mo",
                     delta=f"-{(total_saved/total_baseline)*100:.1f}%")

    # Visualization
    st.markdown("---")
    st.subheader("📊 Timeline Comparison")

    fig = go.Figure()

    fig.add_trace(go.Bar(
        name='Baseline',
        x=df_results['Stage'],
        y=df_results['Baseline'],
        marker_color='lightcoral'
    ))

    fig.add_trace(go.Bar(
        name='AGPO Accelerated',
        x=df_results['Stage'],
        y=df_results['AGPO Time'],
        marker_color='#667eea'
    ))

    fig.update_layout(
        barmode='group',
        title=f"Policy Development Timeline (g-GWC Effectiveness: {gwc_effectiveness:.0%})",
        xaxis_title="Stage",
        yaxis_title="Time (months)",
        height=400
    )

    st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# TAB 5: Reliability Metrics
# =============================================================================

with tab5:
    st.header("Measurement Error and Reliability")

    st.info("""
    **Reliability Analysis:** Quantifying consistency and measurement error in AGPO assessments
    to ensure decision-making confidence.
    """)

    # Mathematical formulations
    with st.expander("📐 Reliability Formulas", expanded=True):
        st.markdown("### Reliability Coefficient")
        st.latex(r"""
        \rho_{XX'} = \frac{\sigma^2_{true}}{\sigma^2_{observed}} = \frac{\sigma^2_{true}}{\sigma^2_{true} + \sigma^2_{error}}
        """)

        st.markdown("### Standard Error of Measurement")
        st.latex(r"""
        SEM = \sigma_{observed} \sqrt{1 - \rho_{XX'}}
        """)

        st.markdown("""
        **Where:**
        - `ρ_XX'` = Reliability coefficient (0-1)
        - `σ²_true` = True score variance
        - `σ²_observed` = Observed score variance
        - `σ²_error` = Measurement error variance
        - `SEM` = Standard error of measurement
        """)

    # Interactive reliability calculator
    st.subheader("🎯 Reliability Calculator")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### Input Parameters")

        observed_variance = st.number_input(
            "Observed Score Variance (σ²_observed)",
            min_value=0.1,
            max_value=10.0,
            value=2.5,
            step=0.1
        )

        error_variance = st.number_input(
            "Error Variance (σ²_error)",
            min_value=0.01,
            max_value=5.0,
            value=0.5,
            step=0.1
        )

        # Calculate true variance
        true_variance = observed_variance - error_variance

        if true_variance <= 0:
            st.error("Error: Error variance cannot exceed observed variance!")
        else:
            # Calculate reliability
            reliability = true_variance / observed_variance

            # Calculate SEM
            sem = np.sqrt(observed_variance) * np.sqrt(1 - reliability)

            st.markdown("---")
            st.markdown("### Calculated Values")
            st.metric("True Score Variance", f"{true_variance:.3f}")

    with col2:
        if true_variance > 0:
            st.markdown("### Reliability Metrics")

            # Display reliability
            col_a, col_b = st.columns(2)

            with col_a:
                st.metric("Reliability (ρ_XX')", f"{reliability:.3f}")

                if reliability >= 0.9:
                    st.success("Excellent reliability")
                elif reliability >= 0.8:
                    st.info("Good reliability")
                elif reliability >= 0.7:
                    st.warning("Acceptable reliability")
                else:
                    st.error("Poor reliability")

            with col_b:
                st.metric("SEM", f"{sem:.3f}")

                # Confidence intervals
                st.markdown("### 95% Confidence Interval")
                st.latex(r"""
                CI_{95} = \pm 1.96 \times SEM
                """)

                ci_95 = 1.96 * sem
                st.metric("Margin of Error", f"±{ci_95:.3f}")

            # Visualization
            st.markdown("---")
            st.markdown("### Variance Decomposition")

            fig = go.Figure()

            fig.add_trace(go.Pie(
                labels=['True Score Variance', 'Error Variance'],
                values=[true_variance, error_variance],
                marker=dict(colors=['#667eea', '#ff6b6b']),
                hole=0.4
            ))

            fig.update_layout(
                title=f"Reliability = {reliability:.3f}",
                height=400
            )

            st.plotly_chart(fig, use_container_width=True)

    # Interpretation guide
    st.markdown("---")
    st.subheader("📖 Interpretation Guide")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        ### Reliability Coefficient (ρ_XX')

        **Interpretation:**
        - **0.90 - 1.00:** Excellent - High confidence in measurements
        - **0.80 - 0.89:** Good - Suitable for most decisions
        - **0.70 - 0.79:** Acceptable - Use with caution
        - **< 0.70:** Poor - Not suitable for critical decisions

        **What it means:**
        Proportion of observed variance that is "true" variance vs. measurement error.
        """)

    with col2:
        st.markdown("""
        ### Standard Error of Measurement (SEM)

        **Interpretation:**
        - Lower SEM = more precise measurements
        - Use for constructing confidence intervals
        - 95% CI ≈ ± 2 × SEM

        **Example:**
        If observed score = 0.75 and SEM = 0.05:
        - 95% confident true score is between 0.65 - 0.85
        - Decision confidence depends on SEM relative to decision threshold
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 20px;'>
    <h3>🧮 Cognitive Decision Science Module</h3>
    <p><strong>E-AGPO-HT Mathematical Framework Implementation</strong></p>
    <p style='font-size: 12px;'>Formal decision-making under uncertainty for AI governance</p>
</div>
""", unsafe_allow_html=True)
