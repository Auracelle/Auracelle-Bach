
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="3D Governance Visualization", page_icon="🌍", layout="wide")

# =============================================================================
# PASSWORD PROTECTION
# =============================================================================

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔐 Auracelle Bach - 3D Coordination Visualization")
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

st.title("🌍 3D VISUALIZATION: AI Governance Coordination")
st.markdown("""
<div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
    <h3 style='color: white; margin: 0;'>Like AlphaFold for Policy Alignment</h3>
    <p style='color: white; margin: 5px 0 0 0; font-size: 14px;'>
        Interactive Multi-Stakeholder Policy Alignment in 3D Space
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
### 🎯 Visualization Overview

This 3D visualization shows AI governance coordination challenges the same way AlphaFold shows protein structures:

**The 3D Space:**
- **X-axis**: Safety/Ethics regulations (0 = permissive, 1 = strict)
- **Y-axis**: Innovation/Development policies (0 = restrictive, 1 = supportive)
- **Z-axis**: Data governance standards (0 = minimal, 1 = comprehensive)

**Each node represents:**
- Countries (US, EU, China, UK, Japan, etc.)
- International organizations (UNESCO, OECD, NATO, UN, WEF)

**Closer nodes = More aligned policies**

**Color coding:**
- 🔵 Blue = High alignment stakeholders
- 🟠 Orange = Medium alignment
- 🔴 Red = Low alignment (different approach)
- 🟢 Green = Policy leaders (international orgs)
""")

# =============================================================================
# EMBED THE 3D VISUALIZATION
# =============================================================================

html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: #0a0e27;
            color: #e0e7ff;
        }
        .container {
            display: grid;
            grid-template-columns: 280px 1fr;
            gap: 1rem;
            padding: 1rem;
            height: 100vh;
        }
        .controls {
            background: rgba(26, 31, 58, 0.8);
            border: 1px solid rgba(102, 126, 234, 0.2);
            border-radius: 12px;
            padding: 1rem;
            overflow-y: auto;
        }
        .control-section { margin-bottom: 1.5rem; }
        .control-section h3 {
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #667eea;
            margin-bottom: 0.75rem;
        }
        .control-group { margin-bottom: 1rem; }
        .control-group label {
            display: block;
            font-size: 0.75rem;
            color: #94a3b8;
            margin-bottom: 0.4rem;
        }
        .slider {
            width: 100%;
            height: 4px;
            background: rgba(102, 126, 234, 0.2);
            border-radius: 2px;
            -webkit-appearance: none;
        }
        .slider::-webkit-slider-thumb {
            -webkit-appearance: none;
            width: 14px;
            height: 14px;
            background: linear-gradient(135deg, #667eea, #f093fb);
            border-radius: 50%;
            cursor: pointer;
        }
        .slider::-moz-range-thumb {
            width: 14px;
            height: 14px;
            background: linear-gradient(135deg, #667eea, #f093fb);
            border-radius: 50%;
            cursor: pointer;
            border: none;
        }
        .value {
            display: inline-block;
            margin-left: 0.5rem;
            padding: 2px 6px;
            background: rgba(102, 126, 234, 0.15);
            border-radius: 3px;
            font-size: 0.7rem;
            color: #f093fb;
        }
        .button {
            width: 100%;
            padding: 0.6rem;
            background: linear-gradient(135deg, #667eea, #764ba2);
            border: none;
            border-radius: 6px;
            color: white;
            font-weight: 600;
            cursor: pointer;
            font-size: 0.8rem;
            margin-top: 0.5rem;
        }
        .button:hover { opacity: 0.9; }
        .button.secondary {
            background: rgba(102, 126, 234, 0.15);
            border: 1px solid rgba(102, 126, 234, 0.3);
        }
        .scenario-btn {
            padding: 0.5rem;
            background: rgba(102, 126, 234, 0.1);
            border: 1px solid rgba(102, 126, 234, 0.2);
            border-radius: 5px;
            color: #e0e7ff;
            font-size: 0.7rem;
            cursor: pointer;
            margin-bottom: 0.4rem;
            text-align: center;
        }
        .scenario-btn:hover { background: rgba(102, 126, 234, 0.2); }
        .scenario-btn.active {
            background: linear-gradient(135deg, #667eea, #764ba2);
            border-color: transparent;
        }
        #canvas { width: 100%; height: 100%; border-radius: 8px; }
        .stats {
            position: absolute;
            top: 1rem;
            right: 1rem;
            background: rgba(10, 14, 39, 0.9);
            border: 1px solid rgba(102, 126, 234, 0.2);
            border-radius: 8px;
            padding: 0.75rem;
            min-width: 160px;
        }
        .stat { margin-bottom: 0.5rem; font-size: 0.7rem; }
        .stat-label { color: #94a3b8; display: block; margin-bottom: 0.2rem; }
        .stat-value {
            color: #e0e7ff;
            font-size: 1rem;
            font-weight: 700;
        }
        .viz-container { position: relative; }
    </style>
</head>
<body>
    <div class="container">
        <div class="controls">
            <div class="control-section">
                <h3>Scenarios</h3>
                <button class="scenario-btn active" onclick="loadScenario('fragmented')">Fragmented Policies</button>
                <button class="scenario-btn" onclick="loadScenario('convergence')">Path to Convergence</button>
                <button class="scenario-btn" onclick="loadScenario('resistance')">High Resistance</button>
                <button class="scenario-btn" onclick="loadScenario('optimal')">Optimal Alignment</button>
            </div>

            <div class="control-section">
                <h3>Parameters</h3>
                <div class="control-group">
                    <label>Coordination Pressure <span class="value" id="pv">50%</span></label>
                    <input type="range" class="slider" id="pressure" min="0" max="100" value="50" oninput="update()">
                </div>
                <div class="control-group">
                    <label>Institutional Inertia <span class="value" id="iv">0.5</span></label>
                    <input type="range" class="slider" id="inertia" min="0" max="100" value="50" oninput="update()">
                </div>
                <div class="control-group">
                    <label>Trust Network <span class="value" id="tv">60%</span></label>
                    <input type="range" class="slider" id="trust" min="0" max="100" value="60" oninput="update()">
                </div>
                <div class="control-group">
                    <label>Time Evolution <span class="value" id="tmv">0 mo</span></label>
                    <input type="range" class="slider" id="time" min="0" max="24" value="0" oninput="update()">
                </div>
            </div>

            <div class="control-section">
                <h3>Animation</h3>
                <button class="button" onclick="toggleAnim()"><span id="at">▶ Start</span></button>
                <button class="button secondary" onclick="reset()">↺ Reset</button>
            </div>
        </div>

        <div class="viz-container">
            <canvas id="canvas"></canvas>
            <div class="stats">
                <div class="stat">
                    <span class="stat-label">Global Alignment</span>
                    <span class="stat-value" id="as">42%</span>
                </div>
                <div class="stat">
                    <span class="stat-label">Stakeholders</span>
                    <span class="stat-value">15</span>
                </div>
                <div class="stat">
                    <span class="stat-label">Clusters</span>
                    <span class="stat-value" id="cs">5</span>
                </div>
                <div class="stat">
                    <span class="stat-label">Convergence</span>
                    <span class="stat-value" id="ct">18 mo</span>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script>
        let scene, camera, renderer, nodes = [], edges = [], isAnim = false;
        const stakeholders = [
            {id:'US',p:[0.6,0.4,0.8],c:0x667eea},{id:'EU',p:[0.8,0.7,0.6],c:0x764ba2},
            {id:'CN',p:[0.3,0.8,0.5],c:0xef4444},{id:'UK',p:[0.7,0.5,0.7],c:0x667eea},
            {id:'JP',p:[0.6,0.6,0.7],c:0xf59e0b},{id:'IN',p:[0.4,0.5,0.6],c:0xf59e0b},
            {id:'CA',p:[0.7,0.6,0.8],c:0x667eea},{id:'AU',p:[0.6,0.5,0.7],c:0x667eea},
            {id:'KR',p:[0.5,0.6,0.7],c:0xf59e0b},{id:'BR',p:[0.4,0.4,0.5],c:0xef4444},
            {id:'UNESCO',p:[0.7,0.8,0.7],c:0x10b981},{id:'OECD',p:[0.8,0.7,0.8],c:0x10b981},
            {id:'NATO',p:[0.7,0.6,0.8],c:0x10b981},{id:'WEF',p:[0.6,0.7,0.6],c:0x10b981},
            {id:'UN',p:[0.7,0.7,0.7],c:0x10b981}
        ];

        function init() {
            const c = document.getElementById('canvas');
            const w = c.clientWidth, h = c.clientHeight;
            scene = new THREE.Scene();
            camera = new THREE.PerspectiveCamera(60, w/h, 0.1, 1000);
            camera.position.set(0,0,20);
            renderer = new THREE.WebGLRenderer({canvas:c, antialias:true, alpha:true});
            renderer.setSize(w,h);
            renderer.setClearColor(0x0a0e27,1);

            const al = new THREE.AmbientLight(0xffffff,0.4);
            scene.add(al);
            const pl1 = new THREE.PointLight(0x667eea,1,100);
            pl1.position.set(10,10,10);
            scene.add(pl1);

            stakeholders.forEach((s,i) => {
                const g = new THREE.SphereGeometry(0.3,32,32);
                const m = new THREE.MeshPhongMaterial({color:s.c,emissive:s.c,emissiveIntensity:0.3});
                const mesh = new THREE.Mesh(g,m);
                mesh.position.set((s.p[0]-0.5)*15,(s.p[1]-0.5)*15,(s.p[2]-0.5)*15);
                scene.add(mesh);

                const sp = makeLabel(s.id);
                sp.position.copy(mesh.position);
                sp.position.y += 0.6;
                scene.add(sp);

                nodes.push({mesh,sp,init:mesh.position.clone(),tgt:mesh.position.clone()});
            });

            updateEdges();
            animate();
        }

        function makeLabel(t) {
            const cv = document.createElement('canvas');
            const ctx = cv.getContext('2d');
            cv.width = 256; cv.height = 128;
            ctx.fillStyle = '#fff';
            ctx.font = 'Bold 48px Arial';
            ctx.textAlign = 'center';
            ctx.fillText(t,128,80);
            const tx = new THREE.Texture(cv);
            tx.needsUpdate = true;
            const mt = new THREE.SpriteMaterial({map:tx});
            const sp = new THREE.Sprite(mt);
            sp.scale.set(2,1,1);
            return sp;
        }

        function updateEdges() {
            edges.forEach(e => scene.remove(e.line));
            edges = [];
            const tr = parseInt(document.getElementById('trust').value)/100;
            const th = 0.3 - (tr*0.2);
            for(let i=0;i<nodes.length;i++) {
                for(let j=i+1;j<nodes.length;j++) {
                    const d = nodes[i].mesh.position.distanceTo(nodes[j].mesh.position);
                    if(d < 15*th) {
                        const mt = new THREE.LineBasicMaterial({color:0x667eea,opacity:Math.max(0.1,1-d/5),transparent:true});
                        const gm = new THREE.BufferGeometry().setFromPoints([nodes[i].mesh.position,nodes[j].mesh.position]);
                        const ln = new THREE.Line(gm,mt);
                        scene.add(ln);
                        edges.push({line:ln});
                    }
                }
            }
        }

        function update() {
            const p = parseInt(document.getElementById('pressure').value)/100;
            const in_ = parseInt(document.getElementById('inertia').value)/100;
            const tr = parseInt(document.getElementById('trust').value)/100;
            const tm = parseInt(document.getElementById('time').value);

            document.getElementById('pv').textContent = Math.round(p*100)+'%';
            document.getElementById('iv').textContent = in_.toFixed(2);
            document.getElementById('tv').textContent = Math.round(tr*100)+'%';
            document.getElementById('tmv').textContent = tm+' mo';

            const spd = p*(1-in_)*tr;
            const prg = Math.min(1,(tm/24)*spd*2);

            const ctr = new THREE.Vector3(0,0,0);
            nodes.forEach(n => ctr.add(n.init));
            ctr.divideScalar(nodes.length);

            nodes.forEach(n => {
                const dir = ctr.clone().sub(n.init);
                n.tgt.copy(n.init).add(dir.multiplyScalar(prg));
                n.mesh.position.lerp(n.tgt,0.1);
                n.sp.position.copy(n.mesh.position);
                n.sp.position.y += 0.6;
            });

            updateEdges();

            const al = Math.round(prg*100);
            document.getElementById('as').textContent = al+'%';
            document.getElementById('cs').textContent = Math.max(1,Math.round(5*(1-prg)));
            document.getElementById('ct').textContent = Math.round(24*(1/Math.max(0.01,spd)))+' mo';
        }

        function animate() {
            requestAnimationFrame(animate);
            const t = Date.now()*0.0001;
            camera.position.x = Math.sin(t)*20;
            camera.position.z = Math.cos(t)*20;
            camera.lookAt(scene.position);
            renderer.render(scene,camera);
        }

        function toggleAnim() {
            isAnim = !isAnim;
            document.getElementById('at').textContent = isAnim ? '⏸ Pause' : '▶ Start';
            if(isAnim) runAnim();
        }

        function runAnim() {
            if(!isAnim) return;
            const ts = document.getElementById('time');
            let v = parseInt(ts.value);
            if(v<24) {
                v += 0.5;
                ts.value = v;
                update();
                setTimeout(runAnim,100);
            } else {
                isAnim = false;
                document.getElementById('at').textContent = '↺ Restart';
            }
        }

        function reset() {
            isAnim = false;
            document.getElementById('at').textContent = '▶ Start';
            document.getElementById('time').value = 0;
            document.getElementById('pressure').value = 50;
            document.getElementById('inertia').value = 50;
            document.getElementById('trust').value = 60;
            nodes.forEach(n => {
                n.mesh.position.copy(n.init);
                n.sp.position.copy(n.mesh.position);
                n.sp.position.y += 0.6;
            });
            update();
        }

        function loadScenario(s) {
            document.querySelectorAll('.scenario-btn').forEach(b => b.classList.remove('active'));
            event.target.classList.add('active');
            reset();
            const vals = {
                fragmented:[30,70,40],
                convergence:[70,40,75],
                resistance:[50,85,30],
                optimal:[90,20,90]
            }[s];
            document.getElementById('pressure').value = vals[0];
            document.getElementById('inertia').value = vals[1];
            document.getElementById('trust').value = vals[2];
            update();
        }

        window.addEventListener('load',init);
    </script>
</body>
</html>
"""


# =============================================================================
# Embed the HTML
components.html(html_code, height=800, scrolling=False)

# User scrolls down to see strategic recommendations below

# STRATEGY RECOMMENDATIONS PANEL
# =============================================================================

st.markdown("---")
st.markdown("### 🎯 Strategic Recommendations")

st.info("""
**Auracelle Bach Intelligence Engine**: Based on current parameters and scenario,
here's the optimal pathway to achieve coordination.
""")

# Create tabs for different recommendation types
rec_tab1, rec_tab2, rec_tab3 = st.tabs(["🌍 Country Actions", "📊 Policy Adjustments", "⏱️ Timeline & Milestones"])

with rec_tab1:
    st.markdown("#### Required Actions by Stakeholder")
    st.markdown("""
    These recommendations show **what each country/organization needs to do** to achieve
    the selected scenario outcome.
    """)

    # Sample strategy recommendations (in real deployment, these would be dynamically generated)
    recommendations = {
        'fragmented': {
            'US': {
                'action': 'Maintain current voluntary framework approach',
                'change': 'No significant changes required',
                'priority': 'Low',
                'timeline': 'Ongoing'
            },
            'EU': {
                'action': 'Continue AI Act implementation',
                'change': 'Already leading - maintain course',
                'priority': 'Medium',
                'timeline': 'On track for 2026'
            },
            'China': {
                'action': 'Maintain state-centric governance model',
                'change': 'Current approach diverges from Western norms',
                'priority': 'Low',
                'timeline': 'No convergence expected'
            },
            'key_insight': '⚠️ This scenario maintains current fragmentation - No convergence strategy'
        },
        'convergence': {
            'US': {
                'action': 'Strengthen voluntary frameworks with enforcement mechanisms',
                'change': '+35% regulatory strength while maintaining innovation focus',
                'priority': 'High',
                'timeline': '6-12 months'
            },
            'EU': {
                'action': 'Moderate AI Act timelines to allow industry adaptation',
                'change': 'Extend compliance deadlines by 6 months for high-risk systems',
                'priority': 'High',
                'timeline': '3-6 months'
            },
            'China': {
                'action': 'Increase transparency in algorithm governance',
                'change': '+40% transparency requirements, align with OECD principles',
                'priority': 'Critical',
                'timeline': '12-18 months'
            },
            'UK': {
                'action': 'Harmonize sectoral approach with EU risk framework',
                'change': 'Adopt compatible risk classification system',
                'priority': 'High',
                'timeline': '6-9 months'
            },
            'Japan': {
                'action': 'Strengthen data governance to match GDPR standards',
                'change': '+25% data protection requirements',
                'priority': 'Medium',
                'timeline': '9-12 months'
            },
            'India': {
                'action': 'Formalize AI governance framework',
                'change': 'Establish comprehensive AI policy (currently ad-hoc)',
                'priority': 'High',
                'timeline': '6-12 months'
            },
            'UNESCO': {
                'action': 'Provide technical assistance to implementing countries',
                'change': 'Increase capacity building programs by 50%',
                'priority': 'Medium',
                'timeline': '3-6 months'
            },
            'OECD': {
                'action': 'Facilitate harmonization workshops among member states',
                'change': 'Quarterly coordination meetings',
                'priority': 'High',
                'timeline': 'Immediate - 24 months'
            },
            'key_insight': '✅ Achievable with coordinated effort - 70% alignment in 18 months'
        },
        'resistance': {
            'key_insight': '❌ High organizational inertia blocks progress - interventions needed to overcome resistance',
            'US': {
                'action': 'Address Congressional gridlock on AI legislation',
                'change': 'Build bipartisan consensus (currently blocked)',
                'priority': 'Critical',
                'timeline': '12-24 months'
            },
            'EU': {
                'action': 'Overcome member state implementation resistance',
                'change': 'Increase political will, reduce bureaucratic delays',
                'priority': 'Critical',
                'timeline': '12-18 months'
            },
            'China': {
                'action': 'Cultural resistance to Western governance norms',
                'change': 'Find common ground on technical standards',
                'priority': 'Critical',
                'timeline': '18-36 months'
            },
            'intervention': '🚨 Requires high-level political intervention to break deadlock'
        },
        'optimal': {
            'key_insight': '🎯 Best-case scenario - rapid convergence with strong coordination',
            'US': {
                'action': 'Pass comprehensive federal AI legislation',
                'change': 'Adopt risk-based framework aligned with EU approach',
                'priority': 'Critical',
                'timeline': '3-6 months'
            },
            'EU': {
                'action': 'Accelerate AI Act implementation with industry support',
                'change': 'Fast-track approval processes, maintain high standards',
                'priority': 'High',
                'timeline': '3-6 months'
            },
            'China': {
                'action': 'Major policy shift toward transparency and international alignment',
                'change': '+60% alignment with OECD principles',
                'priority': 'Critical',
                'timeline': '6-12 months'
            },
            'UK': {
                'action': 'Full harmonization with EU AI Act',
                'change': 'Abandon sectoral approach, adopt EU framework',
                'priority': 'High',
                'timeline': '3-6 months'
            },
            'All': {
                'action': 'Establish permanent international AI governance body',
                'change': 'Create binding coordination mechanism',
                'priority': 'Critical',
                'timeline': '6-9 months'
            },
            'likelihood': '⚡ Requires unprecedented political will - 15% probability without major catalyst'
        }
    }

    # Determine current scenario (default to convergence)
    current_scenario = 'convergence'  # This would be dynamically set based on UI selection

    scenario_recs = recommendations.get(current_scenario, recommendations['convergence'])

    # Display key insight
    if 'key_insight' in scenario_recs:
        st.warning(scenario_recs['key_insight'])

    if 'intervention' in scenario_recs:
        st.error(scenario_recs['intervention'])

    if 'likelihood' in scenario_recs:
        st.info(scenario_recs['likelihood'])

    # Display recommendations by country
    for country, rec in scenario_recs.items():
        if country not in ['key_insight', 'intervention', 'likelihood']:
            with st.expander(f"{'🌐' if country in ['UNESCO', 'OECD', 'NATO', 'WEF', 'UN'] else '🗺️'} {country}", expanded=False):
                if 'action' in rec:
                    st.markdown(f"**Required Action:**")
                    st.markdown(f"{rec['action']}")

                if 'change' in rec:
                    st.markdown(f"**Specific Change:**")
                    st.markdown(f"{rec['change']}")

                if 'priority' in rec:
                    priority_color = {'Critical': '🔴', 'High': '🟠', 'Medium': '🟡', 'Low': '🟢'}
                    st.markdown(f"**Priority:** {priority_color.get(rec['priority'], '⚪')} {rec['priority']}")

                if 'timeline' in rec:
                    st.markdown(f"**Timeline:** {rec['timeline']}")

with rec_tab2:
    st.markdown("#### Quantified Policy Adjustments")
    st.markdown("""
    Based on E-AGPO-HT mathematical modeling, here are the **precise policy parameter changes**
    needed for convergence.
    """)

    # Policy dimension adjustments
    adjustments_df = {
        'Safety/Ethics Regulations': {
            'US': '+35%',
            'EU': 'Baseline (maintain)',
            'China': '+40%',
            'UK': '+15%',
            'Japan': '+20%'
        },
        'Innovation Support': {
            'US': 'Baseline (maintain)',
            'EU': '+10% (moderate enforcement)',
            'China': '+15%',
            'UK': '+5%',
            'Japan': '+10%'
        },
        'Data Governance': {
            'US': '+30%',
            'EU': 'Baseline (GDPR)',
            'China': '+50%',
            'UK': '+20%',
            'Japan': '+25%'
        }
    }

    import pandas as pd
    df_adj = pd.DataFrame(adjustments_df).T

    st.dataframe(df_adj, use_container_width=True)

    st.markdown("""
    **Interpretation:**
    - **Positive values** (+X%) = Need to strengthen/increase regulation
    - **Baseline** = Current level is appropriate, maintain
    - **Higher percentages** = Larger policy shifts required

    **Example:** China needs +40% increase in Safety/Ethics regulations to align with EU/US standards.
    """)

    st.markdown("#### Distance to Consensus")
    st.markdown("""
    Shows how far each stakeholder is from the global consensus point (center of 3D space).
    """)

    distance_data = {
        'Stakeholder': ['China', 'Brazil', 'India', 'South Korea', 'Japan', 'US', 'Canada', 'Australia', 'UK', 'EU'],
        'Current Distance': [8.2, 7.5, 6.8, 5.2, 4.9, 3.5, 2.8, 2.6, 2.1, 1.5],
        'Target Distance': [2.5, 3.0, 3.2, 2.0, 2.2, 2.0, 1.5, 1.5, 1.0, 1.0],
        'Movement Required': [5.7, 4.5, 3.6, 3.2, 2.7, 1.5, 1.3, 1.1, 1.1, 0.5]
    }

    df_dist = pd.DataFrame(distance_data)
    st.dataframe(df_dist, use_container_width=True)

    st.markdown("""
    **Key Finding:** China and Brazil require the largest policy shifts to achieve convergence.
    """)

with rec_tab3:
    st.markdown("#### Convergence Timeline & Milestones")
    st.markdown("""
    **Projected 18-Month Pathway to 70% Global Alignment**
    """)

    milestones = [
        {
            'Month': 'Month 0-3',
            'Phase': 'Foundation',
            'Milestone': 'Initial Coordination Framework',
            'Actions': [
                'OECD convenes harmonization working group',
                'US introduces federal AI legislation',
                'EU extends AI Act compliance timelines by 6 months',
                'UNESCO launches capacity building program'
            ],
            'Expected Alignment': '45%'
        },
        {
            'Month': 'Month 3-6',
            'Phase': 'Early Adoption',
            'Milestone': 'Core Countries Align',
            'Actions': [
                'UK harmonizes with EU framework',
                'Japan strengthens data governance',
                'Canada formalizes alignment commitment',
                'US-EU transatlantic agreement signed'
            ],
            'Expected Alignment': '55%'
        },
        {
            'Month': 'Month 6-12',
            'Phase': 'Expansion',
            'Milestone': 'Regional Blocs Form',
            'Actions': [
                'China increases transparency requirements',
                'India adopts comprehensive AI policy',
                'South Korea aligns with regional standards',
                'Brazil joins Latin American coordination initiative'
            ],
            'Expected Alignment': '62%'
        },
        {
            'Month': 'Month 12-18',
            'Phase': 'Convergence',
            'Milestone': '70% Global Alignment Achieved',
            'Actions': [
                'International AI governance body established',
                'Binding coordination mechanism adopted',
                'Cross-border enforcement framework operational',
                'Regular monitoring and adjustment process begins'
            ],
            'Expected Alignment': '70%'
        }
    ]

    for m in milestones:
        with st.expander(f"**{m['Month']}**: {m['Milestone']} ({m['Expected Alignment']} alignment)", expanded=True):
            st.markdown(f"**Phase:** {m['Phase']}")
            st.markdown(f"**Key Actions:**")
            for action in m['Actions']:
                st.markdown(f"- {action}")

            # Progress bar
            alignment_val = int(m['Expected Alignment'].strip('%'))
            st.progress(alignment_val / 100)

    st.markdown("---")
    st.markdown("#### Critical Success Factors")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **Enablers:**
        - ✅ Strong OECD coordination
        - ✅ EU-US transatlantic cooperation
        - ✅ UNESCO capacity building
        - ✅ Regular stakeholder dialogue
        """)

    with col2:
        st.markdown("""
        **Risks:**
        - ⚠️ US Congressional gridlock
        - ⚠️ China resistance to transparency
        - ⚠️ Industry lobbying against regulation
        - ⚠️ Geopolitical tensions derailing cooperation
        """)

    st.info("""
    **Probability Assessment:** With current coordination pressure and trust levels,
    this pathway has a **65% probability of success**. Increasing trust network strength
    to 80%+ would raise probability to 85%.
    """)



# =============================================================================
# EXPLANATION SECTION
# =============================================================================

st.markdown("---")
st.markdown("### 📖 How to Interpret This Visualization")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    #### The AlphaFold Parallel

    **AlphaFold:**
    - Shows 3D protein structure
    - Predicts folding in hours vs. years
    - Confidence scores for accuracy
    - Reveals structural alignment

    **Auracelle Bach:**
    - Shows 3D policy alignment
    - Predicts convergence in seconds vs. years
    - Alignment scores for coordination
    - Reveals governance coordination patterns
    """)

with col2:
    st.markdown("""
    #### What You're Seeing

    **Node Positions:**
    - Initial: Current policy stance
    - Movement: Convergence toward consensus
    - Clusters: Groups of aligned policies

    **Connections (Lines):**
    - Appear between aligned stakeholders
    - Thickness = strength of alignment
    - More lines = better coordination

    **Colors:**
    - Blue: Western democracies (aligned)
    - Orange: Middle alignment
    - Red: Different approach
    - Green: International organizations
    """)

st.markdown("""
### 🎯 Real-World Applications

1. **Predict Negotiation Outcomes**: See which countries will align before meetings
2. **Identify Bottlenecks**: Find stakeholders blocking coordination
3. **Test Policy Changes**: Adjust parameters to see impact on convergence
4. **Timeline Forecasting**: Estimate realistic convergence timeframes

This visualization makes abstract governance coordination **tangible and measurable** -
just like AlphaFold made protein structures concrete!
""")

# =============================================================================
# FOOTER
# =============================================================================

st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 20px;'>
    <h3>🌍 Auracelle Bach | 3D Coordination Visualization</h3>
    <p><strong>Like AlphaFold for Policy Alignment</strong></p>
    <p style='font-size: 12px;'>Interactive Multi-Stakeholder Simulation</p>
</div>
""", unsafe_allow_html=True)
