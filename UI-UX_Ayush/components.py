"""
components.py — VIDHI UI Components (Compact Viewport Edition)
================================================================
"""
import re
import math
import time
import streamlit as st

from mock_data import (
    DASHBOARD_METRICS,
    QUERY_SUGGESTIONS,
    STANDARDS_LIBRARY,
    RECENT_QUERIES,
    INDUSTRY_CATEGORIES,
    STANDARD_CATEGORIES,
    BIS_SERVICES,
    SAVED_STANDARDS,
)

# ─────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────

def _html(content: str):
    st.markdown(content, unsafe_allow_html=True)


def _badge(text: str, cls: str = "blue") -> str:
    return f'<span class="badge badge-{cls}">{text}</span>'


def _conf_color(pct: int):
    if pct >= 90:
        return "#81c784", "rgba(19,136,8,0.55)", "high", "High Confidence"
    elif pct >= 70:
        return "#64b5f6", "rgba(30,136,229,0.55)", "mod", "Moderate Confidence"
    return "#ffb74d", "rgba(255,153,51,0.55)", "low", "Low Confidence"


def _md_to_html(text: str) -> str:
    def inline(s: str) -> str:
        s = re.sub(r'\*\*(.*?)\*\*', r'<strong style="color:#e8f0fe;">\1</strong>', s)
        s = re.sub(r'\*(.*?)\*',     r'<em style="color:#8ba3c7;">\1</em>', s)
        return s

    lines = text.strip().split('\n')
    html, i = [], 0

    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue

        if re.match(r'^\d+\.\s', line):
            html.append('<ol style="margin:4px 0 8px 18px;padding:0;">')
            while i < len(lines) and re.match(r'^\d+\.\s', lines[i]):
                item = re.sub(r'^\d+\.\s', '', lines[i])
                html.append(f'<li style="margin-bottom:4px;font-size:12.5px;color:#8ba3c7;line-height:1.55;">{inline(item)}</li>')
                i += 1
            html.append('</ol>')
            continue

        if line.startswith('- '):
            html.append('<ul style="margin:4px 0 8px 18px;padding:0;">')
            while i < len(lines) and lines[i].startswith('- '):
                html.append(f'<li style="margin-bottom:4px;font-size:12.5px;color:#8ba3c7;line-height:1.55;">{inline(lines[i][2:])}</li>')
                i += 1
            html.append('</ul>')
            continue

        if re.match(r'^\*\*.+\*\*:?\s*$', line):
            html.append(f'<div style="font-size:11px;font-weight:700;color:#64b5f6;margin:8px 0 4px;text-transform:uppercase;letter-spacing:0.5px;">{inline(line)}</div>')
            i += 1
            continue

        html.append(f'<p style="font-size:13px;color:#8ba3c7;margin:4px 0;line-height:1.65;">{inline(line)}</p>')
        i += 1

    return ''.join(html)


# ─────────────────────────────────────────────────────────────────────
# Header / Navbar
# ─────────────────────────────────────────────────────────────────────

def render_header(role: str = ""):
    role_display = role or "Guest"
    initials = "".join(w[0].upper() for w in role_display.split()[:2]) or "U"

    _html(f"""
<div class="vidi-navbar animate-in">
    <div class="vidi-logo">
        <div class="vidi-logo-mark">V</div>
        <div>
            <div class="vidi-logo-name">VIDHI</div>
            <div class="vidi-logo-sub">AI Assistant for Indian Standards</div>
        </div>
    </div>
    <div class="vidi-navbar-right">
        <div class="vidi-nav-stat">Standards: <span>4,500+</span></div>
        <div class="vidi-nav-stat">Accuracy: <span>94%</span></div>
        <div class="vidi-user-badge">
            <div class="vidi-avatar">{initials}</div>
            <span class="vidi-role-pill">{role_display}</span>
        </div>
    </div>
</div>
""")


def render_demo_banner():
    _html("""
<div style="background:rgba(255,153,51,0.06);border:1px solid rgba(255,153,51,0.2);border-radius:6px;padding:4px 12px;font-size:11px;color:#ffb74d;display:flex;align-items:center;gap:6px;margin-bottom:6px;">
    <span>⚡</span>
    <strong>Demo Mode</strong> — Grounded responses from indexed Indian Standards.
</div>
""")


# ─────────────────────────────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────────────────────────────

def render_sidebar():
    with st.sidebar:
        _html("""
<div style="display:flex;align-items:center;gap:8px;margin-bottom:12px;padding:2px;">
    <div class="vidi-logo-mark" style="width:26px;height:26px;font-size:13px;">V</div>
    <div>
        <div style="font-size:15px;font-weight:900;color:#e8f0fe;">VIDHI</div>
        <div style="font-size:8.5px;color:#4a6080;text-transform:uppercase;">AI for Indian Standards</div>
    </div>
</div>
<div class="tricolor-line" style="margin-bottom:12px;"></div>
""")
        if st.button("＋ New Query", key="new_q_sidebar", use_container_width=True):
            st.session_state.answer = None
            st.session_state.current_query = ""
            st.rerun()

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        _html('<div style="font-size:9.5px;font-weight:700;text-transform:uppercase;color:#4a6080;margin-bottom:6px;">Recent Questions</div>')

        queries = st.session_state.get("query_history", RECENT_QUERIES[:4])
        for q in queries[:6]:
            short = q[:36] + "…" if len(q) > 36 else q
            _html(f"""
            <div style="padding:4px 8px;border-radius:6px;font-size:11.5px;color:#8ba3c7;margin-bottom:2px;background:rgba(255,255,255,0.02);">
                🔍 {short}
            </div>
            """)

        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        demo_mode = st.toggle("Demo Mode", value=st.session_state.get("demo_mode", True), key="sb_demo")
        st.session_state.demo_mode = demo_mode


# ─────────────────────────────────────────────────────────────────────
# Role Selector (Compact)
# ─────────────────────────────────────────────────────────────────────

def render_role_selector() -> str:
    roles = [
        "Manufacturer", "Engineer", "Quality Control Professional",
        "Industry Representative", "Consumer", "Student / Researcher", "Other",
    ]
    current = st.session_state.get("user_role", "Engineer")
    idx = roles.index(current) if current in roles else 1
    selected = st.selectbox("I am a...", roles, index=idx, key="v4_role_select", label_visibility="collapsed")
    st.session_state.user_role = selected
    return selected


# ─────────────────────────────────────────────────────────────────────
# Compact Hero Strip (with 3D AI Orb)
# ─────────────────────────────────────────────────────────────────────

def render_welcome_compact():
    _html("""
<div class="hero-strip animate-in">
    <div style="display:flex;align-items:center;gap:14px;flex:1;">
        <div class="ai-orb-wrap">
            <div class="orb-float">
                <div class="orb-sphere"></div>
                <div class="orb-ring r1"></div>
                <div class="orb-ring r2"></div>
                <div class="orb-ring r3"></div>
            </div>
        </div>
        <div>
            <div class="hero-title">Ask VIDHI about Indian Standards</div>
            <div class="hero-sub">Evidence-backed answers with clause-level citations from BIS documentation.</div>
        </div>
    </div>
    <div class="hero-chips">
        <span class="hero-chip">✅ Evidence-Based</span>
        <span class="hero-chip">📌 Clause Grounded</span>
        <span class="hero-chip">🤖 AI-Assisted</span>
    </div>
</div>
""")


# ─────────────────────────────────────────────────────────────────────
# Compact Suggestion Chips
# ─────────────────────────────────────────────────────────────────────

def render_suggestion_chips() -> str | None:
    _html('<div style="font-size:9.5px;font-weight:700;text-transform:uppercase;letter-spacing:0.6px;color:#4a6080;margin-bottom:6px;">Try asking...</div>')
    suggestions = QUERY_SUGGESTIONS[:6]
    cols = st.columns(3)
    clicked = None
    for i, s in enumerate(suggestions):
        with cols[i % 3]:
            short = s[:46] + "…" if len(s) > 46 else s
            if st.button(f"💬 {short}", key=f"chip_v4_{i}", use_container_width=True, help=s):
                clicked = s
    return clicked


# ─────────────────────────────────────────────────────────────────────
# Processing Animation
# ─────────────────────────────────────────────────────────────────────

def render_processing():
    steps = [
        ("Understanding Query", "Detecting standard intent..."),
        ("Searching Standards", "Scanning 4,500+ Indian Standards..."),
        ("Validating Evidence", "Cross-referencing clause and pages..."),
        ("Generating Answer", "Formatting evidence-backed response..."),
    ]
    ph = st.empty()
    for current in range(len(steps) + 1):
        rows = "".join(f"<div style='font-size:12px;color:{'#81c784' if i<current else '#64b5f6' if i==current else '#4a6080'};padding:2px 0;'>{'✓' if i<current else '●' if i==current else '○'} {lbl}</div>" for i, (lbl, _) in enumerate(steps))
        ph.markdown(f"<div class='glass-card animate-in' style='padding:10px 14px;'><div style='font-size:10px;font-weight:700;color:#64b5f6;text-transform:uppercase;margin-bottom:4px;'>Processing Query</div>{rows}</div>", unsafe_allow_html=True)
        if current < len(steps):
            time.sleep(0.35)
    ph.empty()


# ─────────────────────────────────────────────────────────────────────
# Answer Card
# ─────────────────────────────────────────────────────────────────────

def render_answer(answer_text: str):
    body = _md_to_html(answer_text)
    _html(f"""
<div class="answer-card animate-in">
    <div class="answer-card-header">
        <div class="answer-ai-dot"></div>
        <div>
            <div class="answer-label">VIDHI Answer</div>
            <div class="answer-sublabel">✓ Evidence-backed · Clause-cited</div>
        </div>
    </div>
    <div class="answer-card-body">{body}</div>
</div>
""")


# ─────────────────────────────────────────────────────────────────────
# Circular Confidence Meter
# ─────────────────────────────────────────────────────────────────────

def render_confidence(confidence: int, label: str):
    color, glow, badge_cls, label_text = _conf_color(confidence)
    if not label:
        label = label_text

    r = 38
    circ = round(2 * math.pi * r, 1)
    offset = round(circ * (1 - confidence / 100), 1)

    _html(f"""
<div class="glass-card animate-in">
    <div class="glass-card-header">
        <span class="glass-card-title">Answer Confidence</span>
        {_badge(label, badge_cls)}
    </div>
    <div style="display:flex;align-items:center;justify-content:space-around;">
        <svg width="90" height="90">
            <circle cx="45" cy="45" r="{r}" fill="none" stroke="rgba(255,255,255,0.06)" stroke-width="8"/>
            <circle cx="45" cy="45" r="{r}" fill="none" stroke="{color}" stroke-width="8" stroke-linecap="round" stroke-dasharray="{circ}" stroke-dashoffset="{offset}" transform="rotate(-90 45 45)" style="filter:drop-shadow(0 0 6px {color});"/>
            <text x="45" y="44" text-anchor="middle" font-family="Manrope,sans-serif" font-size="20" font-weight="900" fill="{color}">{confidence}%</text>
            <text x="45" y="58" text-anchor="middle" font-family="Manrope,sans-serif" font-size="8.5" font-weight="600" fill="#526c8e">{label.split()[0]}</text>
        </svg>
        <div style="font-size:11px;color:#8ba3c7;max-width:140px;line-height:1.4;">
            High correlation with indexed BIS clauses and normative references.
        </div>
    </div>
</div>
""")


# ─────────────────────────────────────────────────────────────────────
# Standard Card
# ─────────────────────────────────────────────────────────────────────

def render_standard_card(std: dict):
    _html(f"""
<div class="glass-card animate-in">
    <div class="glass-card-header">
        <span class="glass-card-title">Applicable Standard</span>
        <span class="badge badge-high">✓ Verified</span>
    </div>
    <div style="font-size:16px;font-weight:900;color:#fff;margin-bottom:2px;">{std['id']}</div>
    <div style="font-size:12px;color:#8ba3c7;margin-bottom:8px;line-height:1.35;">{std['title']}</div>
    <div style="display:flex;gap:12px;font-size:10.5px;color:#526c8e;">
        <div>Category: <strong style="color:#e8f0fe;">{std.get('category','—')}</strong></div>
        <div>Year: <strong style="color:#e8f0fe;">{std.get('year','—')}</strong></div>
    </div>
</div>
""")


# ─────────────────────────────────────────────────────────────────────
# Evidence Card
# ─────────────────────────────────────────────────────────────────────

def render_evidence_card(evidence_list: list, query_key: str = "default"):
    if not evidence_list:
        return
    ev = evidence_list[0]
    _html(f"""
<div class="glass-card animate-in">
    <div class="glass-card-header">
        <span class="glass-card-title">Clause Evidence</span>
        <span style="font-size:10px;color:#81c784;font-weight:700;">{ev['clause']} · Page {ev['page']}</span>
    </div>
    <div class="evidence-snippet">{ev['snippet']}</div>
</div>
""")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("📄 View Source Document", key=f"vsrc_c_{query_key}", use_container_width=True):
            st.info(f"📚 Source verified from {ev['standard']} official publication.")
    with c2:
        if st.button("📋 Copy Citation", key=f"ccit_c_{query_key}", use_container_width=True):
            st.code(f"BIS. {ev['standard']}, {ev['clause']}, Page {ev['page']}.", language="text")
            st.toast("Citation copied!", icon="📋")


# ─────────────────────────────────────────────────────────────────────
# Warning Card
# ─────────────────────────────────────────────────────────────────────

def render_warning(confidence: int, query_key: str = "default"):
    _html(f"""
<div class="glass-card animate-in" style="border-color:rgba(255,153,51,0.35);background:rgba(255,153,51,0.06);">
    <div class="glass-card-header">
        <span style="font-size:13px;font-weight:700;color:#ffb74d;">⚠️ Insufficient Evidence</span>
        {_badge(f"{confidence}% Low", "low")}
    </div>
    <p style="font-size:12.5px;color:#cbd5e1;line-height:1.5;margin:4px 0 8px;">
        VIDHI could not find enough authoritative evidence in available BIS documents to provide a reliable answer.
    </p>
</div>
""")
    if st.button("↩ Ask Another Question", key=f"again_{query_key}", use_container_width=True):
        st.session_state.answer = None
        st.session_state.current_query = ""
        st.rerun()


# ─────────────────────────────────────────────────────────────────────
# Transparency & Related Standards
# ─────────────────────────────────────────────────────────────────────

def render_transparency(response: dict):
    std = response.get("standard") or {}
    evidence = response.get("evidence", [])
    conf = response.get("confidence", 0)
    std_id = std.get("id", "—")
    cl_info = f"{evidence[0]['clause']}, Page {evidence[0]['page']}" if evidence else "—"

    _html(f"""
<div class="glass-card animate-in">
    <div class="glass-card-header">
        <span class="glass-card-title">Evidence Chain Grounding</span>
    </div>
    <div style="display:flex;gap:14px;font-size:11.5px;color:#8ba3c7;flex-wrap:wrap;">
        <div>Standard: <strong style="color:#e8f0fe;">{std_id}</strong></div>
        <div>Clause: <strong style="color:#e8f0fe;">{cl_info}</strong></div>
        <div>Match: <strong style="color:#81c784;">{'Strong' if conf>=80 else 'Moderate'}</strong></div>
    </div>
</div>
""")


def render_related_standards(related: list):
    if not related:
        return
    pills = "".join(f'<span class="hero-chip" style="margin-right:4px;">{r}</span>' for r in related)
    _html(f"""
<div style="margin-bottom:6px;">
    <span style="font-size:10px;font-weight:700;text-transform:uppercase;color:#4a6080;margin-right:8px;">Related Standards:</span>
    {pills}
</div>
""")


def render_context_panel(response: dict | None, role: str, query: str = ""):
    topic = response.get("topic", "—") if response else "—"
    conf = response.get("confidence", "—") if response else "—"
    conf_str = f"{conf}%" if isinstance(conf, int) else conf

    _html(f"""
<div class="ctx-panel animate-in">
    <div class="ctx-title">Query Context</div>
    <div class="ctx-item">
        <div class="ctx-label">Role</div>
        <div class="ctx-value">{role}</div>
    </div>
    <div class="ctx-item">
        <div class="ctx-label">Topic</div>
        <div class="ctx-value">{topic}</div>
    </div>
    <div class="ctx-item">
        <div class="ctx-label">Confidence</div>
        <div class="ctx-value" style="color:#64b5f6;">{conf_str}</div>
    </div>
</div>
""")


# ─────────────────────────────────────────────────────────────────────
# Other Tabs (Dashboard, Explorer, BIS Services, About)
# ─────────────────────────────────────────────────────────────────────

def render_dashboard():
    _html("""
<div style="margin-bottom:12px;">
    <h3 style="font-size:18px;font-weight:900;color:#e8f0fe;margin:0 0 2px;">VIDHI Dashboard</h3>
    <p style="font-size:11.5px;color:#526c8e;margin:0;">Real-time Indian Standards compliance metrics</p>
</div>
""")
    cols = st.columns(4)
    metrics = [
        ("📚", DASHBOARD_METRICS["standards_indexed"],   "Standards Indexed"),
        ("💬", DASHBOARD_METRICS["queries_answered"],    "Queries Answered"),
        ("✅", DASHBOARD_METRICS["evidence_backed_pct"], "Evidence Match Rate"),
        ("📊", DASHBOARD_METRICS["avg_confidence"],      "Avg Confidence"),
    ]
    for i, (icon, val, lbl) in enumerate(metrics):
        with cols[i]:
            _html(f"""
            <div class="metric-card">
                <div style="font-size:18px;margin-bottom:2px;">{icon}</div>
                <div class="metric-value">{val}</div>
                <div class="metric-label">{lbl}</div>
            </div>
            """)


def render_standards_explorer():
    _html("""
<div style="margin-bottom:10px;">
    <h3 style="font-size:18px;font-weight:900;color:#e8f0fe;margin:0 0 2px;">Standards Explorer</h3>
    <p style="font-size:11.5px;color:#526c8e;margin:0;">Search over 4,500+ indexed Indian Standards</p>
</div>
""")
    fc1, fc2 = st.columns([3, 2])
    with fc1:
        search_term = st.text_input("Search", key="std_search_c", label_visibility="collapsed", placeholder="🔍 Search by IS number or keyword...")
    with fc2:
        cat_filter = st.selectbox("Category", ["All"] + STANDARD_CATEGORIES, key="std_cat_c", label_visibility="collapsed")

    filtered = STANDARDS_LIBRARY
    if search_term:
        q = search_term.lower()
        filtered = [s for s in filtered if q in s["id"].lower() or q in s["title"].lower()]
    if cat_filter != "All":
        filtered = [s for s in filtered if s.get("category") == cat_filter]

    st.markdown(f"<div style='font-size:11px;color:#526c8e;margin:4px 0 8px;'>Showing {len(filtered)} standards</div>", unsafe_allow_html=True)

    for row_start in range(0, len(filtered), 3):
        rcols = st.columns(3)
        for ci, s in enumerate(filtered[row_start:row_start + 3]):
            with rcols[ci]:
                _html(f"""
                <div class="glass-card" style="padding:10px;margin-bottom:6px;">
                    <div style="font-size:13px;font-weight:900;color:#fff;">{s['id']}</div>
                    <div style="font-size:11px;color:#8ba3c7;margin-bottom:4px;">{s['title']}</div>
                    <span class="badge badge-mod">{s['category']}</span>
                </div>
                """)


def render_bis_services():
    _html("""
<div style="margin-bottom:12px;">
    <h3 style="font-size:18px;font-weight:900;color:#e8f0fe;margin:0 0 2px;">🏛️ BIS Schemes &amp; Services</h3>
    <p style="font-size:11.5px;color:#526c8e;margin:0;">Bureau of Indian Standards certification and compliance frameworks</p>
</div>
""")
    for s in BIS_SERVICES:
        _html(f"""
<div class="glass-card" style="padding:12px;margin-bottom:8px;">
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:4px;">
        <div style="display:flex;align-items:center;gap:8px;">
            <span style="font-size:20px;">{s['icon']}</span>
            <div style="font-size:13.5px;font-weight:800;color:#fff;">{s['title']}</div>
        </div>
        <span class="badge badge-high">{s['badge']}</span>
    </div>
    <p style="font-size:11.5px;color:#cbd5e1;line-height:1.4;margin:2px 0 0;">{s['description']}</p>
</div>
""")


def render_about_section():
    _html("""
<div style="margin-bottom:10px;">
    <h3 style="font-size:18px;font-weight:900;color:#e8f0fe;margin:0 0 2px;">ℹ️ About VIDHI</h3>
    <p style="font-size:11.5px;color:#526c8e;margin:0;">Next-generation Indian Standards AI intelligence platform — SIH 2026</p>
</div>
<div class="glass-card" style="padding:14px;margin-bottom:8px;">
    <div style="font-size:13.5px;font-weight:800;color:#fff;margin-bottom:4px;">🎯 Mission &amp; Purpose</div>
    <p style="font-size:12px;color:#8ba3c7;line-height:1.6;margin:0;">
        VIDHI bridges the accessibility gap for over <strong>20,000+ Indian Standards (IS)</strong> published by the <strong>Bureau of Indian Standards (BIS)</strong>. Built with a multi-stage grounded RAG architecture, VIDHI delivers clause-cited, verified answers for MSMEs, engineers, and quality inspectors.
    </p>
</div>
""")


def render_footer():
    _html("""
<div class="vidi-footer">
    <div class="tricolor-line" style="margin-bottom:8px;max-width:180px;margin-left:auto;margin-right:auto;"></div>
    <strong style="color:#8ba3c7;">VIDHI</strong>
    <span style="color:#4a6080;"> — AI Assistant for Indian Standards · Smart India Hackathon 2026 Prototype · Not official BIS advice.</span>
</div>
""")
