import streamlit as st
from pathlib import Path
from graph.proposal_graph import build_graph

st.set_page_config(page_title="AI Proposal Generator", layout="wide")

# -------------------------
# SIDEBAR
# -------------------------
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio("Go to", ["🧠 Generate Proposal", "📜 History"])

st.title("AI Proposal Generator & Evaluator")

# ============================
# 🧠 GENERATE PROPOSAL PAGE
# ============================
if page == "🧠 Generate Proposal":

    st.header("Generate a New Proposal")

    # Input Section
    col1, col2 = st.columns([2, 1])

    with col1:
        idea = st.text_area("💡 Enter your project idea", height=150)

    with col2:
        agency = st.selectbox(
            "🏢 Select Funding Agency",
            ["DST", "AICTE", "SERB"]
        )
        generate_btn = st.button("🚀 Generate Proposal", use_container_width=True)

    if generate_btn:
        if idea.strip() == "":
            st.warning("Please enter an idea")
        else:
            with st.spinner("Generating proposal..."):

                graph = build_graph()

                initial_state = {
                    "idea": idea,
                    "agency": agency,
                    "expanded_idea": None,
                    "guidelines": None,
                    "proposal": None,
                    "budget": None,
                    "proposal_id": None,
                    "rule_score": 0,
                    "llm_score": 0,
                    "final_score": 0,
                    "weak_sections": [],
                    "iteration_count": 0
                }

                result = graph.invoke(initial_state)

                # ✅ SAVE RESULT
                st.session_state["result"] = result

                # ✅ SAVE TO HISTORY
                if "history" not in st.session_state:
                    st.session_state["history"] = []

                st.session_state["history"].append({
                    "idea": idea,
                    "agency": agency,
                    "proposal": result.get("proposal", {}),
                    "budget": result.get("budget", {}),
                    "score": result.get("final_score", 0)
                })

            st.success("✅ Proposal Generated Successfully!")

    # ============================
    # DISPLAY RESULTS
    # ============================
    if "result" in st.session_state:

        res = st.session_state["result"]

        proposal = res.get("proposal", {})
        budget = res.get("budget", {})

        st.divider()

        tab1, tab2, tab3 = st.tabs([
            "📄 Document Content",
            "💰 Budget Breakdown",
            "📊 AI Evaluation"
        ])

        # -------- TAB 1: PROPOSAL --------
        with tab1:
            st.subheader(proposal.get("title", "Generated Proposal"))

            st.markdown("### Abstract")
            st.write(proposal.get("abstract", "N/A"))

            st.markdown("### Methodology")
            st.write(proposal.get("methodology", "N/A"))

            st.markdown("### Timeline")
            st.write(proposal.get("timeline", "N/A"))

        # -------- TAB 2: BUDGET --------
        with tab2:
            st.subheader("Financial Overview")

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Personnel", f"₹{budget.get('personnel_cost', 0)}")
            c2.metric("Equipment", f"₹{budget.get('equipment_cost', 0)}")
            c3.metric("Software", f"₹{budget.get('software_cost', 0)}")
            c4.metric("Misc", f"₹{budget.get('miscellaneous_cost', 0)}")

            st.metric(
                "Total Budget",
                f"₹{budget.get('total_budget', 0)}"
            )

        # -------- TAB 3: EVALUATION --------
        with tab3:
            st.subheader("AI Scoring")

            final_score = res.get("final_score", 0)

            st.progress(final_score / 100, text=f"Final Score: {final_score}%")

            col_a, col_b = st.columns(2)
            col_a.metric("Rule Score", res.get("rule_score", 0))
            col_b.metric("LLM Score", res.get("llm_score", 0))

            if res.get("weak_sections"):
                st.warning("⚠️ Areas for Improvement")
                for area in res.get("weak_sections"):
                    st.write(f"- {area}")

        # ✅ FILE FEATURE DISABLED
        st.divider()
        st.info("📄 Document download temporarily disabled.")


# ============================
# 📜 HISTORY PAGE (UPDATED)
# ============================
elif page == "📜 History":

    st.header("Saved Proposals")

    if "history" not in st.session_state or len(st.session_state["history"]) == 0:
        st.info("No proposals generated yet.")
    else:
        for i, item in enumerate(reversed(st.session_state["history"]), 1):

            with st.expander(f"📄 Proposal {i} - {item['agency']}"):

                st.write("💡 Idea:", item["idea"])
                st.write("🏢 Agency:", item["agency"])
                st.write("📊 Score:", item["score"])

                proposal = item.get("proposal", {})
                budget = item.get("budget", {})

                # -------- PROPOSAL --------
                st.markdown("### Title")
                st.write(proposal.get("title", "N/A"))

                st.markdown("### Abstract")
                st.write(proposal.get("abstract", "N/A"))

                st.markdown("### Methodology")
                st.write(proposal.get("methodology", "N/A"))

                st.markdown("### Timeline")
                st.write(proposal.get("timeline", "N/A"))

                # -------- BUDGET --------
                st.markdown("### 💰 Budget Breakdown")

                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Personnel", f"₹{budget.get('personnel_cost', 0)}")
                c2.metric("Equipment", f"₹{budget.get('equipment_cost', 0)}")
                c3.metric("Software", f"₹{budget.get('software_cost', 0)}")
                c4.metric("Misc", f"₹{budget.get('miscellaneous_cost', 0)}")

                st.metric(
                    "Total Budget",
                    f"₹{budget.get('total_budget', 0)}"
                )