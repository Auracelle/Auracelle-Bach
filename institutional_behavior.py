
import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# Note: st.set_page_config is called in app.py, not in pages

# =============================================================================
# PASSWORD PROTECTION
# =============================================================================

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔐 Auracelle Bach - Institutional Behavior Modules")
    password = st.text_input("Enter password:", type="password")
    if st.button("Login"):
        if password == "charlie2025":
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Incorrect password")
    st.stop()

# =============================================================================
# PAGE HEADER
# =============================================================================

st.title("🏛️ Institutional Behavior Modules")
st.markdown("""
<div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
    <h3 style='color: white; margin: 0;'>Human-Inspired Organizational Cognition</h3>
    <p style='color: white; margin: 5px 0 0 0; font-size: 14px;'>
        Modeling real institutional decision-making patterns
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
### 🎯 Module Overview

This page demonstrates three key institutional behavior modules that capture how real
organizations make decisions under constraints, biases, and resistance to change.

**Modules:**
1. **🧠 Bounded Rationality Engine** - Herbert Simon's satisficing theory
2. **🎭 Cognitive Bias System** - 6 organizational biases
3. **⚙️ Organizational Inertia Modeling** - Change resistance patterns
""")

# =============================================================================
# MODULE 1: BOUNDED RATIONALITY ENGINE
# =============================================================================

st.markdown("---")
st.header("1. 🧠 Bounded Rationality Engine")

st.markdown("""
**Theoretical Foundation:** Herbert Simon's satisficing theory

Organizations don't optimize—they **satisfice** (satisfy + suffice). They search for
"good enough" solutions within cognitive and resource constraints.
""")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Parameters")

    aspiration_level = st.slider(
        "Aspiration Level (minimum acceptable)",
        0.0, 1.0, 0.7, 0.05,
        help="Minimum performance threshold for acceptance"
    )

    search_depth = st.slider(
        "Search Depth (alternatives considered)",
        1, 20, 5, 1,
        help="Number of alternatives to evaluate before stopping"
    )

    cognitive_load = st.slider(
        "Cognitive Load (processing constraints)",
        0.0, 1.0, 0.5, 0.05,
        help="Higher values = more limited processing capacity"
    )

with col2:
    st.markdown("#### Decision Simulation")

    # Simulate bounded rationality decision-making
    np.random.seed(42)

    alternatives = []
    for i in range(search_depth):
        # Quality decreases with cognitive load
        base_quality = np.random.beta(2, 2)
        adjusted_quality = base_quality * (1 - cognitive_load * 0.5)

        alternatives.append({
            'Alternative': f'Option {i+1}',
            'Quality': adjusted_quality,
            'Meets Aspiration': adjusted_quality >= aspiration_level
        })

    df_alternatives = pd.DataFrame(alternatives)

    # Find first satisficing option
    satisficing_idx = df_alternatives[df_alternatives['Meets Aspiration']].index

    if len(satisficing_idx) > 0:
        selected = satisficing_idx[0]
        optimal = df_alternatives['Quality'].idxmax()

        st.success(f"✅ Selected: {df_alternatives.iloc[selected]['Alternative']} " +
                  f"(Quality: {df_alternatives.iloc[selected]['Quality']:.2f})")

        if selected != optimal:
            st.warning(f"⚠️ Not optimal! Best option was {df_alternatives.iloc[optimal]['Alternative']} " +
                      f"(Quality: {df_alternatives.iloc[optimal]['Quality']:.2f})")
        else:
            st.info("🎯 Satisficing solution is also optimal!")
    else:
        st.error("❌ No alternatives meet aspiration level - search continues or threshold lowers")

# Visualization
fig = go.Figure()

fig.add_trace(go.Bar(
    x=df_alternatives['Alternative'],
    y=df_alternatives['Quality'],
    marker_color=['green' if m else 'red' for m in df_alternatives['Meets Aspiration']],
    text=[f"{q:.2f}" for q in df_alternatives['Quality']],
    textposition='auto',
))

fig.add_hline(y=aspiration_level, line_dash="dash", line_color="blue",
              annotation_text="Aspiration Level", annotation_position="right")

fig.update_layout(
    title="Bounded Rationality: Search Process",
    xaxis_title="Alternatives (evaluated in order)",
    yaxis_title="Quality Score",
    yaxis_range=[0, 1],
    height=400
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("""
**Key Insights:**
- Organizations stop searching when they find "good enough" (green bars)
- Cognitive load reduces perceived quality of alternatives
- Satisficing ≠ optimizing (may miss better options evaluated later)
""")

# =============================================================================
# MODULE 2: COGNITIVE BIAS SYSTEM
# =============================================================================

st.markdown("---")
st.header("2. 🎭 Cognitive Bias System")

st.markdown("""
**Six Organizational Biases:**

Organizations systematically deviate from rational decision-making due to cognitive biases.
""")

# Bias definitions
biases = {
    "Status Quo Bias": {
        "description": "Preference for current state; resistance to change",
        "impact": "Underweights benefits of new policies",
        "example": "Keeping legacy AI governance despite better alternatives"
    },
    "Confirmation Bias": {
        "description": "Seeking information that confirms existing beliefs",
        "impact": "Ignores contradictory evidence",
        "example": "Only reviewing studies supporting current approach"
    },
    "Availability Bias": {
        "description": "Overweighting easily recalled information",
        "impact": "Recent/dramatic events dominate decisions",
        "example": "Overreacting to recent AI incident"
    },
    "Anchoring Bias": {
        "description": "Over-relying on first piece of information",
        "impact": "Initial proposals constrain negotiation range",
        "example": "First country's proposal sets agenda"
    },
    "Loss Aversion": {
        "description": "Losses loom larger than equivalent gains",
        "impact": "Risk-averse decision-making",
        "example": "Rejecting beneficial but uncertain AI policy"
    },
    "Groupthink": {
        "description": "Conformity pressure suppresses dissent",
        "impact": "Poor decisions due to consensus pressure",
        "example": "Committee adopts flawed policy to maintain harmony"
    }
}

# Interactive bias selector
selected_bias = st.selectbox("Select Bias to Explore:", list(biases.keys()))

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown(f"#### {selected_bias}")
    st.markdown(f"**Definition:** {biases[selected_bias]['description']}")
    st.markdown(f"**Impact:** {biases[selected_bias]['impact']}")
    st.markdown(f"**Example:** {biases[selected_bias]['example']}")

with col2:
    st.markdown("#### Bias Strength Simulation")

    bias_strength = st.slider(
        "Bias Intensity",
        0.0, 1.0, 0.5, 0.05,
        help="How strongly this bias affects decisions"
    )

    # Simulate bias impact on decision quality
    rational_score = 0.8  # Unbiased decision quality
    biased_score = rational_score * (1 - bias_strength * 0.4)

    st.metric("Rational Decision Quality", f"{rational_score:.2f}")
    st.metric("Biased Decision Quality", f"{biased_score:.2f}",
              delta=f"{biased_score - rational_score:.2f}")

    # Show bias adjustment
    st.markdown(f"""
    **Adjustment:** Decision quality reduced by {(rational_score - biased_score)*100:.1f}%
    """)

# Multi-bias interaction
st.markdown("#### Multi-Bias Interaction")

col1, col2, col3 = st.columns(3)

with col1:
    status_quo = st.slider("Status Quo", 0.0, 1.0, 0.3, 0.1, key='sq')
    confirmation = st.slider("Confirmation", 0.0, 1.0, 0.3, 0.1, key='cf')

with col2:
    availability = st.slider("Availability", 0.0, 1.0, 0.3, 0.1, key='av')
    anchoring = st.slider("Anchoring", 0.0, 1.0, 0.3, 0.1, key='an')

with col3:
    loss_aversion = st.slider("Loss Aversion", 0.0, 1.0, 0.3, 0.1, key='la')
    groupthink = st.slider("Groupthink", 0.0, 1.0, 0.3, 0.1, key='gt')

# Calculate combined bias effect
bias_values = [status_quo, confirmation, availability, anchoring, loss_aversion, groupthink]
combined_bias = 1 - np.prod([1 - b*0.15 for b in bias_values])

# Visualization
bias_df = pd.DataFrame({
    'Bias': ['Status Quo', 'Confirmation', 'Availability', 'Anchoring', 'Loss Aversion', 'Groupthink'],
    'Strength': bias_values
})

fig = px.bar(bias_df, x='Bias', y='Strength',
             title=f"Bias Profile (Combined Effect: {combined_bias:.2%} reduction)",
             color='Strength',
             color_continuous_scale='Reds')
fig.update_layout(height=400)
st.plotly_chart(fig, use_container_width=True)

st.markdown(f"""
**Combined Impact:** With these bias levels, organizational decision quality is reduced by
approximately **{combined_bias*100:.1f}%** from the rational baseline.
""")

# =============================================================================
# MODULE 3: ORGANIZATIONAL INERTIA MODELING
# =============================================================================

st.markdown("---")
st.header("3. ⚙️ Organizational Inertia Modeling")

st.markdown("""
**Theoretical Foundation:** Change resistance patterns

Organizations resist change due to:
- Structural inertia (established procedures, roles, systems)
- Cultural inertia (norms, values, identity)
- Political inertia (power structures, coalitions)
""")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Inertia Parameters")

    org_age = st.slider("Organization Age (years)", 1, 50, 15, 1,
                       help="Older organizations have stronger inertia")

    change_magnitude = st.slider("Change Magnitude", 0.0, 1.0, 0.5, 0.05,
                                 help="How radical is the proposed change")

    external_pressure = st.slider("External Pressure", 0.0, 1.0, 0.3, 0.05,
                                  help="Environmental forces demanding change")

    leadership_commitment = st.slider("Leadership Commitment", 0.0, 1.0, 0.6, 0.05,
                                     help="How committed leadership is to change")

with col2:
    st.markdown("#### Inertia Calculation")

    # Calculate inertia components
    structural_inertia = min(1.0, org_age / 30)  # Increases with age
    cultural_inertia = 0.7  # Relatively constant
    political_inertia = 0.6 * (1 - leadership_commitment)  # Decreases with leadership

    # Total inertia
    base_inertia = (structural_inertia + cultural_inertia + political_inertia) / 3

    # Change resistance increases with magnitude
    change_resistance = base_inertia * (1 + change_magnitude)

    # Success probability
    change_success_prob = external_pressure * leadership_commitment / (1 + change_resistance)

    st.metric("Structural Inertia", f"{structural_inertia:.2f}")
    st.metric("Cultural Inertia", f"{cultural_inertia:.2f}")
    st.metric("Political Inertia", f"{political_inertia:.2f}")
    st.markdown("---")
    st.metric("Total Change Resistance", f"{change_resistance:.2f}")
    st.metric("Change Success Probability", f"{change_success_prob:.2%}")

# Visualization: Inertia over time
st.markdown("#### Change Adoption Timeline")

time_periods = np.arange(0, 24, 1)  # 24 months
adoption_curve = []

for t in time_periods:
    # S-curve adoption with inertia delay
    time_adjusted = t - (change_resistance * 6)  # Inertia delays adoption
    if time_adjusted < 0:
        adoption = 0
    else:
        adoption = change_success_prob / (1 + np.exp(-0.4 * (time_adjusted - 8)))
    adoption_curve.append(adoption)

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=time_periods,
    y=adoption_curve,
    mode='lines',
    name='Adoption Rate',
    line=dict(color='blue', width=3)
))

# Add resistance threshold
fig.add_hline(y=0.5, line_dash="dash", line_color="red",
              annotation_text="50% Adoption", annotation_position="right")

fig.update_layout(
    title="Organizational Change Adoption Over Time",
    xaxis_title="Months",
    yaxis_title="Adoption Rate",
    yaxis_range=[0, 1],
    height=400
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("""
**Key Insights:**
- High inertia delays change adoption (flat initial curve)
- External pressure and leadership commitment can overcome inertia
- S-curve pattern: slow start → rapid adoption → plateau
""")

# =============================================================================
# INTEGRATED DEMONSTRATION
# =============================================================================

st.markdown("---")
st.header("🎯 Integrated Demonstration")

st.markdown("""
### Real-World Scenario: EU AI Act Implementation

Watch how all three modules interact when an organization faces implementing the EU AI Act.
""")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**🧠 Bounded Rationality**")
    st.markdown("Organization searches for compliance approach")
    st.markdown("- Aspiration: 'Good enough' compliance")
    st.markdown("- Stops at first acceptable option")
    st.markdown("- Misses optimal solution")

with col2:
    st.markdown("**🎭 Cognitive Biases**")
    st.markdown("Multiple biases distort decision")
    st.markdown("- Status quo: Prefer minimal change")
    st.markdown("- Anchoring: First proposal dominates")
    st.markdown("- Loss aversion: Focus on costs")

with col3:
    st.markdown("**⚙️ Organizational Inertia**")
    st.markdown("Resistance slows implementation")
    st.markdown("- Structural: Existing processes")
    st.markdown("- Cultural: 'We've always done it this way'")
    st.markdown("- Political: Department conflicts")

# Simulation results
st.markdown("#### Simulation Results")

# Simulate combined effect
rational_timeline = 6  # months
rational_quality = 0.9

# Bounded rationality effect
satisficing_quality = 0.7  # Good enough, not optimal

# Bias effect
biased_quality = satisficing_quality * (1 - combined_bias)

# Inertia effect
actual_timeline = rational_timeline * (1 + change_resistance)

col1, col2 = st.columns(2)

with col1:
    st.metric("Rational Approach",
             f"Quality: {rational_quality:.2f} | Time: {rational_timeline} months")
    st.metric("Actual Approach",
             f"Quality: {biased_quality:.2f} | Time: {actual_timeline:.1f} months",
             delta=f"-{(rational_quality - biased_quality)*100:.0f}% quality")

with col2:
    # Show breakdown
    st.markdown("**Quality Degradation:**")
    st.markdown(f"1. Satisficing: {rational_quality:.2f} → {satisficing_quality:.2f}")
    st.markdown(f"2. Biases: {satisficing_quality:.2f} → {biased_quality:.2f}")
    st.markdown(f"3. Inertia: Delays by {(actual_timeline - rational_timeline):.1f} months")

# =============================================================================
# FOOTER
# =============================================================================

st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 20px;'>
    <h3>🏛️ Auracelle Bach | Institutional Behavior Modules</h3>
    <p><strong>Human-Inspired Organizational Cognition</strong></p>
    <p style='font-size: 12px;'>Bounded Rationality • Cognitive Biases • Organizational Inertia</p>
    <p style='font-size: 10px; color: #666;'>
        Based on: Simon (1956) • Kahneman & Tversky (1979) • Hannan & Freeman (1984)
    </p>
</div>
""", unsafe_allow_html=True)
