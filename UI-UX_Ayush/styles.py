"""
styles.py — VIDHI Cinematic 3D Dark AI Theme
==============================================
Apple Vision Pro / Modern AI SaaS aesthetic for Indian Standards
Deep navy & midnight indigo palette + layered 3D depth & cinematic lighting
"""


def get_global_css() -> str:
    return """
<style>
/* ── Google Fonts: Manrope (Primary) & JetBrains Mono (Tech) ──────── */
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
    /* ── Dark Premium Palette ── */
    --bg-0:      #070A12; /* Near black foundation */
    --bg-1:      #0B1020; /* Deep navy */
    --bg-2:      #10172A; /* Midnight blue */
    --bg-3:      #171633; /* Dark indigo */
    --bg-surface:#0e1528; /* Glass card base */
    
    /* ── Glass Layers ── */
    --glass-base:    rgba(11, 16, 32, 0.72);
    --glass-card:    rgba(14, 21, 40, 0.78);
    --glass-elevated:rgba(18, 27, 54, 0.85);
    --glass-input:   rgba(10, 15, 30, 0.92);
    
    /* ── Cinematic Accents ── */
    --electric-blue: #1e88e5;
    --blue-bright:   #38bdf8;
    --cyan-glow:     #00b4d8;
    --cyan-subtle:   #06b6d4;
    --violet-glow:   #8b5cf6;
    --indigo-soft:   #6366f1;
    
    /* ── Subtle Indian Identity Accents ── */
    --saffron-gold:  #FF9933;
    --saffron-glow:  rgba(255, 153, 51, 0.35);
    --emerald-green: #10b981;
    --green-glow:    rgba(16, 185, 129, 0.35);
    --pure-white:    #FFFFFF;
    
    /* ── Typography Colors ── */
    --tx-title:   #f8fafc; /* Crisp blue-white */
    --tx-primary: #e2e8f0; /* Clear text */
    --tx-muted:   #94a3b8; /* Soft blue-gray */
    --tx-dim:     #475569; /* Subtle labels */
    
    /* ── Borders & Precision Edges ── */
    --border-subtle: rgba(255, 255, 255, 0.07);
    --border-glass:  rgba(255, 255, 255, 0.12);
    --border-glow:   rgba(56, 189, 248, 0.28);
    --border-active: rgba(0, 180, 216, 0.55);
    
    /* ── 3D Shadows & Volumetric Glows ── */
    --sh-3d-card:
        0 12px 36px rgba(0, 0, 0, 0.65),
        0 4px 12px rgba(0, 0, 0, 0.45),
        inset 0 1px 0 rgba(255, 255, 255, 0.12);
    --sh-3d-elevated:
        0 20px 48px rgba(0, 0, 0, 0.75),
        0 8px 20px rgba(0, 0, 0, 0.5),
        0 0 32px rgba(30, 136, 229, 0.14),
        inset 0 1px 0 rgba(255, 255, 255, 0.16);
    --sh-glow-blue: 0 0 24px rgba(30, 136, 229, 0.25), 0 0 48px rgba(30, 136, 229, 0.1);
    
    /* ── Radii ── */
    --r-sm: 8px;
    --r-md: 12px;
    --r-lg: 16px;
    --r-xl: 22px;
    
    --font-main: 'Manrope', -apple-system, BlinkMacSystemFont, sans-serif;
    --font-mono: 'JetBrains Mono', monospace;
}

/* ── Reset & Core App Background ─────────────────────────────────── */
html, body, [class*="css"] {
    font-family: var(--font-main) !important;
    color: var(--tx-primary);
    background-color: var(--bg-0) !important;
}

.stApp, .main, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background: var(--bg-0) !important;
}

[data-testid="stHeader"] { display: none !important; }

.block-container {
    background: transparent !important;
    padding-top: 0.4rem !important;
    padding-bottom: 1.2rem !important;
    padding-left: 1.2rem !important;
    padding-right: 1.2rem !important;
    max-width: 1400px !important;
    position: relative;
    z-index: 2;
}

/* ── 3D Multi-Layer Background (Deep Cinematic Atmosphere) ──────── */

/* Layer 1 & 2: Dynamic Radial Spotlights & Ambient Glow Clouds */
.stApp::before {
    content: '';
    position: fixed; inset: 0;
    background:
        /* Top-center spotlight on AI Command Core */
        radial-gradient(ellipse 65% 45% at 50% 0%, rgba(30, 136, 229, 0.14) 0%, transparent 70%),
        /* Left ambient blue-cyan aura */
        radial-gradient(circle 500px at 10% 35%, rgba(0, 180, 216, 0.08) 0%, transparent 60%),
        /* Right violet/indigo aura */
        radial-gradient(circle 550px at 90% 40%, rgba(139, 92, 246, 0.07) 0%, transparent 60%),
        /* Bottom subtle saffron warm reflection */
        radial-gradient(ellipse 45% 30% at 75% 95%, rgba(255, 153, 51, 0.04) 0%, transparent 55%),
        /* Deep navy foundation gradient */
        linear-gradient(180deg, #070A12 0%, #0B1020 40%, #070A12 100%);
    pointer-events: none;
    z-index: 0;
}

/* Layer 3 & 4: 3D Engineering Grid + Ambient Micro Floating Geometry */
.stApp::after {
    content: '';
    position: fixed; inset: 0;
    background-image:
        /* High-precision 40px engineering grid */
        linear-gradient(rgba(56, 189, 248, 0.022) 1px, transparent 1px),
        linear-gradient(90deg, rgba(56, 189, 248, 0.022) 1px, transparent 1px);
    background-size: 48px 48px;
    background-position: center center;
    mask-image: radial-gradient(ellipse 85% 75% at 50% 50%, #000 30%, transparent 95%);
    -webkit-mask-image: radial-gradient(ellipse 85% 75% at 50% 50%, #000 30%, transparent 95%);
    pointer-events: none;
    z-index: 0;
}

/* ── Custom Sleek Scrollbars ─────────────────────────────────────── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: rgba(7, 10, 18, 0.4); }
::-webkit-scrollbar-thumb {
    background: rgba(56, 189, 248, 0.28);
    border-radius: 4px;
    border: 1px solid rgba(255, 255, 255, 0.05);
}
::-webkit-scrollbar-thumb:hover { background: rgba(56, 189, 248, 0.65); }

/* ── Cinematic Navbar ────────────────────────────────────────────── */
.vidi-navbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 7px 18px;
    background: var(--glass-card);
    border: 1px solid var(--border-glass);
    border-radius: var(--r-md);
    box-shadow: var(--sh-3d-card);
    backdrop-filter: blur(28px);
    -webkit-backdrop-filter: blur(28px);
    margin-bottom: 7px;
    position: relative;
    overflow: hidden;
}
.vidi-navbar::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(56, 189, 248, 0.4), rgba(139, 92, 246, 0.3), transparent);
}
.vidi-logo { display: flex; align-items: center; gap: 10px; }
.vidi-logo-mark {
    width: 30px; height: 30px;
    background: linear-gradient(135deg, #1e88e5 0%, #0d47a1 60%, #171633 100%);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 15px; font-weight: 900; color: #fff;
    box-shadow: 0 0 16px rgba(30, 136, 229, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.3);
}
.vidi-logo-name {
    font-size: 17px; font-weight: 900;
    color: var(--tx-title);
    letter-spacing: -0.4px; line-height: 1;
}
.vidi-logo-sub {
    font-size: 8.5px; font-weight: 600;
    color: var(--tx-muted);
    text-transform: uppercase; letter-spacing: 0.7px; margin-top: 1px;
}

.vidi-user-badge {
    display: flex; align-items: center; gap: 7px;
    padding: 3px 12px 3px 5px;
    background: rgba(18, 27, 54, 0.6);
    border: 1px solid var(--border-glass);
    border-radius: 20px;
    backdrop-filter: blur(12px);
}
.vidi-avatar {
    width: 22px; height: 22px;
    background: linear-gradient(135deg, var(--electric-blue), var(--violet-glow));
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 10px; font-weight: 800; color: white;
    box-shadow: 0 0 10px rgba(30, 136, 229, 0.5);
}
.vidi-role-pill { font-size: 11.5px; font-weight: 600; color: var(--tx-primary); }
.vidi-navbar-right { display: flex; align-items: center; gap: 14px; }
.vidi-nav-stat { font-size: 11px; font-weight: 600; color: var(--tx-muted); }
.vidi-nav-stat span { color: var(--blue-bright); font-weight: 700; }

/* ── Dark Glass Tabs Navigation ──────────────────────────────────── */
div[data-baseweb="tab-list"] {
    background: var(--glass-base) !important;
    border-bottom: 1px solid var(--border-glass) !important;
    border-radius: var(--r-md) var(--r-md) 0 0 !important;
    padding: 3px 8px 0 !important;
    margin-bottom: 8px !important;
    backdrop-filter: blur(24px) !important;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4) !important;
}
button[data-baseweb="tab"] {
    font-family: var(--font-main) !important;
    font-weight: 600 !important; font-size: 12px !important;
    color: var(--tx-muted) !important;
    background: transparent !important;
    padding: 7px 16px !important;
    border-radius: var(--r-sm) var(--r-sm) 0 0 !important;
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
    border: none !important;
}
button[data-baseweb="tab"]:hover {
    color: var(--tx-title) !important;
    background: rgba(30, 136, 229, 0.1) !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: #fff !important; font-weight: 800 !important;
    background: rgba(30, 136, 229, 0.18) !important;
    border-bottom: 2px solid var(--blue-bright) !important;
    text-shadow: 0 0 12px rgba(56, 189, 248, 0.5) !important;
}
div[data-baseweb="tab-highlight"], div[data-baseweb="tab-border"] { display: none !important; }
div[data-baseweb="tab-panel"] { padding: 0 !important; }

/* ── 3D Hero Strip (Atmospheric AI Core & Spotlight) ─────────────── */
.hero-strip {
    background: linear-gradient(135deg, rgba(14, 21, 40, 0.92) 0%, rgba(23, 22, 51, 0.65) 50%, rgba(11, 16, 32, 0.92) 100%);
    border: 1px solid var(--border-glow);
    border-radius: var(--r-lg);
    padding: 12px 20px;
    display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 8px; position: relative; overflow: hidden;
    backdrop-filter: blur(28px);
    box-shadow: var(--sh-3d-elevated);
}
.hero-strip::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, var(--saffron-gold) 0%, var(--blue-bright) 50%, var(--emerald-green) 100%);
    opacity: 0.8;
}
.hero-strip::after {
    content: ''; position: absolute; bottom: -30px; left: 20%;
    width: 220px; height: 60px;
    background: radial-gradient(ellipse, rgba(56, 189, 248, 0.15), transparent 70%);
    filter: blur(20px); pointer-events: none;
}
.hero-title {
    font-size: 17px; font-weight: 900;
    color: var(--tx-title);
    letter-spacing: -0.4px; line-height: 1.15;
    text-shadow: 0 2px 10px rgba(0, 0, 0, 0.6);
}
.hero-sub {
    font-size: 11px; color: var(--tx-muted); margin-top: 2px;
}
.hero-chips { display: flex; gap: 6px; flex-wrap: wrap; flex-shrink: 0; }
.hero-chip {
    font-size: 9.5px; font-weight: 700; color: rgba(255, 255, 255, 0.9);
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.14);
    border-radius: 12px; padding: 4px 9px;
    backdrop-filter: blur(8px);
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.15);
}

/* ── Upgraded 3D AI Intelligence Sphere ──────────────────────────── */
.ai-orb-wrap {
    width: 52px; height: 52px;
    position: relative; flex-shrink: 0;
    perspective: 800px;
}
.orb-float {
    width: 100%; height: 100%; position: relative;
    animation: orbFloating 4s ease-in-out infinite;
    transform-style: preserve-3d;
}
.orb-sphere {
    width: 32px; height: 32px;
    background: radial-gradient(circle at 32% 28%, #a5f3fc 0%, #38bdf8 25%, #1e88e5 50%, #0f172a 85%, #070a12 100%);
    border-radius: 50%;
    position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
    box-shadow:
        0 0 18px rgba(56, 189, 248, 0.9),
        0 0 36px rgba(30, 136, 229, 0.5),
        inset 0 0 12px rgba(255, 255, 255, 0.6),
        inset -4px -4px 10px rgba(0, 0, 0, 0.7);
    z-index: 3;
}
.orb-ring {
    position: absolute; border-radius: 50%; top: 50%; left: 50%;
    transform-style: preserve-3d;
}
.orb-ring.r1 {
    width: 44px; height: 44px; margin: -22px 0 0 -22px;
    border: 1.5px solid rgba(255, 153, 51, 0.7);
    box-shadow: 0 0 10px var(--saffron-glow);
    animation: orbGimbalA 7s linear infinite;
}
.orb-ring.r2 {
    width: 52px; height: 52px; margin: -26px 0 0 -26px;
    border: 1.2px dashed rgba(16, 185, 129, 0.65);
    box-shadow: 0 0 10px var(--green-glow);
    animation: orbGimbalB 9s linear infinite;
}
.orb-ring.r3 {
    width: 40px; height: 40px; margin: -20px 0 0 -20px;
    border: 1px solid rgba(139, 92, 246, 0.6);
    animation: orbGimbalC 5s linear infinite;
}

@keyframes orbFloating {
    0%, 100% { transform: translateY(0) scale(1); }
    50%      { transform: translateY(-5px) scale(1.03); }
}
@keyframes orbGimbalA {
    from { transform: rotateX(65deg) rotateY(0deg) rotateZ(0deg); }
    to   { transform: rotateX(65deg) rotateY(360deg) rotateZ(360deg); }
}
@keyframes orbGimbalB {
    from { transform: rotateX(-50deg) rotateY(0deg) rotateZ(0deg); }
    to   { transform: rotateX(-50deg) rotateY(-360deg) rotateZ(360deg); }
}
@keyframes orbGimbalC {
    from { transform: rotateX(20deg) rotateY(0deg) rotateZ(0deg); }
    to   { transform: rotateX(20deg) rotateY(360deg) rotateZ(0deg); }
}

/* ── 3D Suggestion Chips ─────────────────────────────────────────── */
div[data-testid="column"] .stButton > button {
    background: rgba(14, 21, 40, 0.65) !important;
    border: 1px solid var(--border-glass) !important;
    border-radius: var(--r-sm) !important;
    color: var(--tx-primary) !important;
    font-size: 11.5px !important; font-weight: 600 !important;
    padding: 6px 12px !important; text-align: left !important;
    white-space: normal !important; line-height: 1.3 !important;
    min-height: 38px !important;
    backdrop-filter: blur(16px) !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.35), inset 0 1px 0 rgba(255, 255, 255, 0.08) !important;
    transition: all 0.22s cubic-bezier(0.16, 1, 0.3, 1) !important;
}
div[data-testid="column"] .stButton > button:hover {
    background: rgba(30, 136, 229, 0.2) !important;
    border-color: var(--border-active) !important;
    color: #fff !important;
    transform: translateY(-2px) !important;
    box-shadow:
        0 8px 24px rgba(0, 0, 0, 0.5),
        0 0 16px rgba(56, 189, 248, 0.3),
        inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
}
div[data-testid="column"] .stButton > button:active {
    transform: translateY(1px) !important;
}

/* ── 3D Glass Cards (High-Precision Depth) ───────────────────────── */
.glass-card {
    background: var(--glass-card);
    border: 1px solid var(--border-glass);
    border-radius: var(--r-md);
    padding: 14px 16px;
    box-shadow: var(--sh-3d-card);
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    margin-bottom: 8px;
    position: relative;
    overflow: hidden;
    transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}
.glass-card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.15), transparent);
}
.glass-card:hover {
    border-color: var(--border-glow);
    box-shadow: var(--sh-3d-elevated);
    transform: translateY(-2px);
}
.glass-card-header {
    display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 8px; padding-bottom: 6px;
    border-bottom: 1px solid var(--border-subtle);
}
.glass-card-title {
    font-size: 10px; font-weight: 800; color: var(--tx-muted);
    text-transform: uppercase; letter-spacing: 0.9px;
}

/* ── Structured Answer Card (Command Console Output) ─────────────── */
.answer-card {
    background: linear-gradient(180deg, rgba(16, 24, 48, 0.88) 0%, rgba(11, 16, 32, 0.92) 100%);
    border: 1px solid var(--border-glow);
    border-radius: var(--r-md);
    overflow: hidden;
    box-shadow: var(--sh-3d-elevated);
    margin-bottom: 8px;
    backdrop-filter: blur(28px);
    position: relative;
}
.answer-card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, var(--saffron-gold), var(--blue-bright), var(--emerald-green));
}
.answer-card-header {
    display: flex; align-items: center; gap: 8px;
    padding: 10px 14px;
    background: rgba(30, 136, 229, 0.09);
    border-bottom: 1px solid var(--border-subtle);
}
.answer-ai-dot {
    width: 8px; height: 8px; border-radius: 50%;
    background: var(--blue-bright);
    box-shadow: 0 0 10px var(--blue-bright), 0 0 20px rgba(56, 189, 248, 0.8);
    animation: aiDotPulse 2s ease-in-out infinite;
    flex-shrink: 0;
}
@keyframes aiDotPulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%      { opacity: 0.5; transform: scale(1.3); }
}
.answer-label { font-size: 13px; font-weight: 800; color: var(--tx-title); }
.answer-sublabel { font-size: 10.5px; color: rgba(56, 189, 248, 0.85); }
.answer-card-body {
    padding: 12px 14px;
    font-size: 13px; line-height: 1.75; color: var(--tx-primary);
}
.answer-card-body strong { color: #fff; font-weight: 700; }
.answer-card-body ul, .answer-card-body ol { margin: 4px 0 8px 16px; padding: 0; }
.answer-card-body li { margin-bottom: 4px; font-size: 12.5px; }

/* ── Evidence Snippet (Dark Glass Blockquote) ────────────────────── */
.evidence-snippet {
    background: rgba(30, 136, 229, 0.06);
    border-left: 3px solid var(--blue-bright);
    border-radius: 0 var(--r-sm) var(--r-sm) 0;
    padding: 10px 14px;
    font-size: 12.5px; color: #cbd5e1; line-height: 1.6;
    margin: 8px 0; font-style: italic;
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.05);
}

/* ── Precision Badges ────────────────────────────────────────────── */
.badge {
    font-size: 9.5px; font-weight: 800; padding: 2px 8px;
    border-radius: 6px; letter-spacing: 0.4px;
}
.badge-high {
    background: rgba(16, 185, 129, 0.18);
    color: #6ee7b7;
    border: 1px solid rgba(16, 185, 129, 0.4);
    box-shadow: 0 0 10px rgba(16, 185, 129, 0.2);
}
.badge-mod {
    background: rgba(56, 189, 248, 0.18);
    color: #7dd3fc;
    border: 1px solid rgba(56, 189, 248, 0.4);
    box-shadow: 0 0 10px rgba(56, 189, 248, 0.2);
}
.badge-low, .badge-amber {
    background: rgba(255, 153, 51, 0.18);
    color: #fdba74;
    border: 1px solid rgba(255, 153, 51, 0.4);
    box-shadow: 0 0 10px rgba(255, 153, 51, 0.2);
}

/* ── Precision Selectbox & Input Fields ──────────────────────────── */
.stSelectbox label {
    font-size: 9.5px !important; font-weight: 800 !important;
    text-transform: uppercase !important; letter-spacing: 0.6px !important;
    color: var(--tx-muted) !important;
}
.stSelectbox > div > div {
    background: var(--glass-card) !important;
    border: 1px solid var(--border-glass) !important;
    color: var(--tx-title) !important;
    border-radius: var(--r-sm) !important;
    min-height: 36px !important;
    box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.5) !important;
}

/* ── Primary AI Chat Input (Command Console Bar) ──────────────────── */
[data-testid="stChatInput"] {
    background: var(--glass-input) !important;
    border: 1px solid var(--border-active) !important;
    border-radius: var(--r-md) !important;
    box-shadow:
        0 12px 32px rgba(0, 0, 0, 0.6),
        0 0 24px rgba(0, 180, 216, 0.2),
        inset 0 1px 0 rgba(255, 255, 255, 0.15) !important;
    backdrop-filter: blur(28px) !important;
    transition: all 0.25s ease !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: var(--blue-bright) !important;
    box-shadow:
        0 16px 40px rgba(0, 0, 0, 0.7),
        0 0 32px rgba(56, 189, 248, 0.35),
        inset 0 1px 0 rgba(255, 255, 255, 0.25) !important;
}
[data-testid="stChatInput"] textarea {
    color: var(--tx-title) !important;
    font-size: 13px !important;
    font-family: var(--font-main) !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: var(--tx-dim) !important;
}

/* ── 3D Metric Cards ─────────────────────────────────────────────── */
.metric-card {
    background: var(--glass-card);
    border: 1px solid var(--border-glass);
    border-radius: var(--r-md);
    padding: 14px 12px;
    text-align: center;
    box-shadow: var(--sh-3d-card);
    position: relative; overflow: hidden;
    backdrop-filter: blur(20px);
    transition: all 0.25s ease;
}
.metric-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, var(--electric-blue), var(--cyan-glow));
}
.metric-card:hover {
    transform: translateY(-3px);
    box-shadow: var(--sh-3d-elevated);
    border-color: var(--border-glow);
}
.metric-value {
    font-size: 26px; font-weight: 900;
    color: var(--tx-title); line-height: 1.1; margin-bottom: 2px;
    text-shadow: 0 0 20px rgba(56, 189, 248, 0.4);
}
.metric-label {
    font-size: 9.5px; font-weight: 800;
    text-transform: uppercase; letter-spacing: 0.6px;
    color: var(--tx-muted);
}

/* ── Evidence Chain & Context ────────────────────────────────────── */
.ctx-panel, .evidence-chain-panel {
    background: var(--glass-card);
    border: 1px solid var(--border-glass);
    border-radius: var(--r-md);
    padding: 12px 14px;
    box-shadow: var(--sh-3d-card);
    backdrop-filter: blur(20px);
}
.ctx-title, .ecp-title {
    font-size: 9.5px; font-weight: 800; text-transform: uppercase;
    letter-spacing: 0.8px; color: var(--tx-muted); margin-bottom: 8px;
    padding-bottom: 4px; border-bottom: 1px solid var(--border-subtle);
}
.ctx-item { margin-bottom: 6px; }
.ctx-label { font-size: 9.5px; font-weight: 700; text-transform: uppercase; color: var(--tx-dim); }
.ctx-value { font-size: 12px; font-weight: 600; color: var(--tx-title); }

.ecp-node {
    font-size: 10.5px; font-weight: 600; color: var(--tx-primary);
    text-align: center; background: rgba(255, 255, 255, 0.03);
    border: 1px solid var(--border-glass);
    border-radius: 6px; padding: 5px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}
.ecp-node-q  { border-color: rgba(56, 189, 248, 0.4); color: #7dd3fc; }
.ecp-node-ok { background: rgba(16, 185, 129, 0.12); border-color: rgba(16, 185, 129, 0.4); color: #6ee7b7; }
.ecp-arrow   { text-align: center; color: rgba(56, 189, 248, 0.5); font-size: 11px; margin: 1px 0; }

/* ── Tricolor Ambient Accent ─────────────────────────────────────── */
.tricolor-line {
    height: 2px;
    background: linear-gradient(90deg, var(--saffron-gold) 33%, rgba(255, 255, 255, 0.8) 33% 66%, var(--emerald-green) 66%);
    border-radius: 1px; opacity: 0.6;
}

/* ── Footer ──────────────────────────────────────────────────────── */
.vidi-footer {
    text-align: center; padding: 14px;
    border-top: 1px solid var(--border-subtle);
    margin-top: 20px; font-size: 10.5px; color: var(--tx-dim);
}
</style>
"""
