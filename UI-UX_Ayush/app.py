"""
app.py — VIDHI UI (Compact Zero-Scroll Viewport Edition)
==========================================================
Smart India Hackathon 2026 Prototype
Run: python run.py
"""
import streamlit as st

st.set_page_config(
    page_title="VIDHI — AI Assistant for Indian Standards",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded",
)

from styles import get_global_css
from components import (
    render_header,
    render_demo_banner,
    render_sidebar,
    render_role_selector,
    render_welcome_compact,
    render_suggestion_chips,
    render_processing,
    render_answer,
    render_confidence,
    render_standard_card,
    render_evidence_card,
    render_warning,
    render_transparency,
    render_related_standards,
    render_context_panel,
    render_dashboard,
    render_standards_explorer,
    render_bis_services,
    render_about_section,
    render_footer,
)
from mock_data import get_demo_response, RECENT_QUERIES

st.markdown(get_global_css(), unsafe_allow_html=True)


# ── Session State ──────────────────────────────────────────────────────
def init_session_state():
    defaults = {
        "demo_mode": True,
        "user_role": "Engineer",
        "current_query": "",
        "answer": None,
        "query_history": RECENT_QUERIES[:5],
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_session_state()

# ── Sidebar ────────────────────────────────────────────────────────────
render_sidebar()

# ── Compact Top Bar ───────────────────────────────────────────────────
render_header(role=st.session_state.user_role)

if st.session_state.demo_mode:
    render_demo_banner()

# ── Main Navigation via st.tabs() ─────────────────────────────────────
tab_ask, tab_home, tab_standards, tab_bis, tab_about = st.tabs(
    ["  🤖  Ask VIDHI  ", "  🏠  Dashboard  ", "  📚  Standards Explorer  ", "  🏛️  BIS Services  ", "  ℹ️  About  "]
)

# ══════════════════════════════════════════════════════════════════════
# TAB 1 — ASK VIDHI (Zero-Scroll Viewport Layout)
# ══════════════════════════════════════════════════════════════════════
with tab_ask:

    # ── Top row: Role Selector (Left) | Context Panel (Right) ─────────
    top_left, top_right = st.columns([3, 1], gap="small")
    with top_left:
        role = render_role_selector()
    with top_right:
        render_context_panel(
            response=st.session_state.answer,
            role=st.session_state.user_role,
            query=st.session_state.current_query,
        )

    # ── Main Content Area ─────────────────────────────────────────────
    main_col, right_col = st.columns([3, 1], gap="small")

    with main_col:
        # Compact Hero with 3D Orb (Only shown before first query)
        if st.session_state.answer is None:
            render_welcome_compact()

        # Suggestion Chips
        clicked_suggestion = render_suggestion_chips()

        # Chat Message History
        if st.session_state.current_query:
            with st.chat_message("user"):
                st.markdown(f"**{st.session_state.current_query}**")

        # Response Rendering
        if st.session_state.answer:
            resp = st.session_state.answer
            conf = resp.get("confidence", 0)
            qkey = str(abs(hash(st.session_state.current_query)))

            if resp.get("answer") is None:
                render_warning(conf, query_key=qkey)
            else:
                render_answer(resp["answer"])

                c1, c2 = st.columns(2, gap="small")
                with c1:
                    render_confidence(conf, resp.get("confidence_label", ""))
                with c2:
                    if resp.get("standard"):
                        render_standard_card(resp["standard"])

                render_evidence_card(resp.get("evidence", []), query_key=qkey)
                render_transparency(resp)
                render_related_standards(resp.get("related_standards", []))

    # ── Right Column: Grounded Evidence Chain Visual ──────────────────
    with right_col:
        st.markdown("""
<div class="evidence-chain-panel">
    <div class="ecp-title">Evidence Chain</div>
    <div class="ecp-node ecp-node-q">📝 User Query</div>
    <div class="ecp-arrow">↓</div>
    <div class="ecp-node">🤖 AI Analysis</div>
    <div class="ecp-arrow">↓</div>
    <div class="ecp-node">📚 IS Standard</div>
    <div class="ecp-arrow">↓</div>
    <div class="ecp-node">📌 Clause Match</div>
    <div class="ecp-arrow">↓</div>
    <div class="ecp-node">📎 Evidence Citation</div>
    <div class="ecp-arrow">↓</div>
    <div class="ecp-node ecp-node-ok">✓ Confidence Score</div>
</div>
""", unsafe_allow_html=True)

    # ── Primary Chat Input ─────────────────────────────────────────────
    query = st.chat_input(
        "Ask about an Indian Standard, clause, requirement, product, or BIS service...",
        key="main_chat_input_v4",
    )

    final_query = query or clicked_suggestion

    if final_query:
        st.session_state.current_query = final_query
        short_q = final_query[:50] + ("…" if len(final_query) > 50 else "")
        history = st.session_state.get("query_history", [])
        if short_q not in history:
            history.insert(0, short_q)
            st.session_state.query_history = history[:8]

        response = get_demo_response(final_query, st.session_state.user_role)
        st.session_state.answer = response
        st.rerun()

# ══════════════════════════════════════════════════════════════════════
# TAB 2 — DASHBOARD
# ══════════════════════════════════════════════════════════════════════
with tab_home:
    render_dashboard()

# ══════════════════════════════════════════════════════════════════════
# TAB 3 — STANDARDS EXPLORER
# ══════════════════════════════════════════════════════════════════════
with tab_standards:
    render_standards_explorer()

# ══════════════════════════════════════════════════════════════════════
# TAB 4 — BIS SERVICES
# ══════════════════════════════════════════════════════════════════════
with tab_bis:
    render_bis_services()

# ══════════════════════════════════════════════════════════════════════
# TAB 5 — ABOUT
# ══════════════════════════════════════════════════════════════════════
with tab_about:
    render_about_section()

# ── Footer ─────────────────────────────────────────────────────────────
render_footer()
