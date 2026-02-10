# Repository Structure — Auracelle Bach

**Version:** 3.0.0 | **Date:** 2026-02-09

---

## Directory Tree

```
auracelle-bach/
│
├── 📓 CHIA_PERFECT_02_09_26_AURACELLE_BACH_3_D_BEHAVIOR_AND_COGNITIVE_INTEGRATED.ipynb
│       ↳ One-click Google Colab deployment notebook
│         Generates all application files at runtime
│         Launches Streamlit via pyngrok tunnel
│
├── 🐍 app.py
│       ↳ Streamlit application entry point
│         Password authentication (session state)
│         Displays all 10 E-AGPO-HT enhancements on login screen
│         Routes authenticated users to pages/simulation.py
│
├── 🐍 bach_api_utils.py
│       ↳ Core mathematical intelligence engine (911 lines)
│         Phase 2 API integration: OECD · Privacy International · ParlaMint
│         All 10 mathematical enhancements as callable functions
│         Static fallback datasets for offline operation
│         LRU caching for performance
│
├── 🐍 moral_foundations.py
│       ↳ Cognitive architecture: Haidt's Moral Foundations Theory (729 lines)
│         Five foundations: Care · Fairness · Loyalty · Authority · Sanctity
│         Cultural calibration per stakeholder nation
│         Value-weighted policy scoring
│
├── 🐍 trust_dynamics.py
│       ↳ Cognitive architecture: Ostrom/Axelrod cooperation models (781 lines)
│         Institutional trust evolution and decay functions
│         Reputation scoring and iterated game theory
│         Multi-round negotiation simulation
│
├── 📋 requirements.txt
│       ↳ Python dependencies with minimum version constraints
│
├── 📁 pages/
│   │
│   ├── 🐍 simulation.py            [1,387 lines]
│   │       ↳ PRIMARY SIMULATION INTERFACE
│   │         10 tabbed enhancement panels (E1–E10)
│   │         12 international policy frameworks (7 binding + 5 voluntary)
│   │         Multi-stakeholder country selection (15+ nations)
│   │         Plotly interactive visualisations
│   │
│   ├── 🐍 visual_3d.py             [869 lines]
│   │       ↳ 3D POLICY COORDINATION VISUALISATION
│   │         Interactive 3D Plotly policy space
│   │         Four scenario pathways: Fragmented · Convergence · Resistance · Optimal
│   │         Real-time convergence animation
│   │         15-country + IO multi-stakeholder network
│   │
│   ├── 🐍 cognitive_demo.py        [391 lines]
│   │       ↳ COGNITIVE ARCHITECTURE DEMONSTRATION
│   │         Interactive Moral Foundations profile builder
│   │         Trust Dynamics scenario explorer
│   │         Value-weighted decision output
│   │
│   ├── 🐍 cognitive_decision_science.py  [805 lines]
│   │       ↳ FORMAL DECISION SCIENCE MODULE
│   │         Decision-making under uncertainty (Bayesian)
│   │         Reliability Coefficient (ρ_XX') calculation
│   │         Standard Error of Measurement (SEM) analysis
│   │         Confidence interval construction for governance scores
│   │
│   └── 🐍 institutional_behavior.py  [466 lines]
│           ↳ INSTITUTIONAL BEHAVIOR ENGINE
│             Bounded Rationality (Simon's satisficing)
│             6 Cognitive Biases: status quo · confirmation · availability
│                                  anchoring · loss aversion · groupthink
│             Organisational Inertia Modelling
│
├── 📁 .devcontainer/
│   └── devcontainer.json           ↳ VS Code Dev Container config
│
├── 📁 .github/
│   ├── workflows/
│   │   └── ci.yml                  ↳ CI/CD: lint, test, dependency audit
│   └── ISSUE_TEMPLATE/
│       ├── bug_report.md           ↳ Bug report template
│       └── feature_request.md     ↳ Feature request template
│
└── 📄 Documentation
    ├── README.md                   ↳ Primary project documentation
    ├── CHANGELOG.md                ↳ Version history (v1.0.0 → v3.0.0)
    ├── CITATION.cff                ↳ Academic citation metadata
    ├── LICENSE                     ↳ MIT License
    ├── CODE_OF_CONDUCT.md          ↳ Community standards
    ├── CONTRIBUTING.md             ↳ Contribution guidelines
    ├── SECURITY.md                 ↳ Security policy
    ├── INSTALLATION.md             ↳ Setup instructions
    ├── GITHUB_SETUP.md             ↳ Repository setup guide
    ├── SETUP_CHECKLIST.md          ↳ Deployment checklist
    ├── MASTER_FILE_LIST.md         ↳ Complete file inventory
    ├── REPOSITORY_STRUCTURE.md    ↳ This file
    ├── PULL_REQUEST_TEMPLATE.md    ↳ PR template
    ├── bug_report.md               ↳ Issue template (root copy)
    └── feature_request.md         ↳ Issue template (root copy)
```

---

## Data Flow Architecture

```
Google Colab Notebook
        │
        ▼
[pyngrok tunnel] ──────────────────────────────────────────────
        │                                                       │
        ▼                                                       ▼
  app.py                                              External APIs
  (Authentication)                              OECD · Privacy Int'l · ParlaMint
        │                                                       │
        ▼                                                       ▼
  pages/simulation.py ◄──────────────────── bach_api_utils.py
  (10 Enhancements)                         (Math Engine + API Cache)
        │                                          │
        ├──► moral_foundations.py                  │
        ├──► trust_dynamics.py                     │
        │                                          │
        ▼                                          │
  pages/visual_3d.py ◄───────────────────────────┘
  pages/cognitive_demo.py
  pages/cognitive_decision_science.py
  pages/institutional_behavior.py
```

---

## E-AGPO-HT Stratum Mapping

| Stratum | Files | Components |
|---------|-------|------------|
| **III — g-GWC** | `pages/simulation.py` (Tab 10) | Cognitive Foresight & Strategic Analysis |
| **II — BGC** | `bach_api_utils.py` (E1–E9) | STI · SAD · ESI · NDM · SRA · IIC · ASI |
| **II — ACC AI** | `moral_foundations.py`, `trust_dynamics.py` | Cognitive architecture layer |
| **I — NOF** | `pages/simulation.py` (E1–E9 tabs) | ~40 Narrow Operational Factors |

---

*© 2026 Auracelle AI Governance Labs / Grace A. Evans. E-AGPO-HT is proprietary IP.*
