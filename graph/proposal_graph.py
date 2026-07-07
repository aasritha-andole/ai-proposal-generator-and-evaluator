from langgraph.graph import StateGraph, END
from document_generator.generate_doc import generate_document
from graph.state import ProposalState
# Import agents
from agents.idea_expansion_agent import expand_idea
from agents.guideline_agent import generate_guidelines
from agents.proposal_agent import generate_proposal
from agents.budget_agent import generate_budget
from agents.evaluation_agent import evaluate_proposal, rule_based_score
from agents.refinement_agent import refine_proposal
# Import database functions
from database.repository import save_proposal, save_budget, save_evaluation

# -------------------------
# NODE 1 — IDEA EXPANSION
# -------------------------
def idea_expansion_node(state: ProposalState):
    expanded = expand_idea(state["idea"])
    state["expanded_idea"] = expanded
    return state


# -------------------------
# NODE 2 — GUIDELINES
# -------------------------
def guideline_node(state: ProposalState):
    guidelines = generate_guidelines(state["agency"])
    state["guidelines"] = guidelines
    return state


# -------------------------
# NODE 3 — PROPOSAL
# -------------------------
def proposal_node(state: ProposalState):
    proposal = generate_proposal(
        state["idea"],
        state["expanded_idea"],
        state["guidelines"]
    )

    proposal_id = save_proposal(
        state["idea"],
        state["agency"],
        proposal
    )

    state["proposal"] = proposal
    state["proposal_id"] = proposal_id

    return state


# -------------------------
# NODE 4 — BUDGET
# -------------------------
def budget_node(state: ProposalState):
    budget = generate_budget(
        state["proposal"],
        state["agency"]
    )

    save_budget(
        state["proposal_id"],
        budget
    )

    state["budget"] = budget
    return state


# -------------------------
# NODE 5 — EVALUATION
# -------------------------
def evaluation_node(state: ProposalState):

    proposal = state["proposal"]
    guidelines = state["guidelines"]

    rule_score = rule_based_score(proposal)
    llm_result = evaluate_proposal(proposal, guidelines)

    llm_score = llm_result["llm_score"]
    final_score = (rule_score + llm_score) / 2

    evaluation_data = {
        "innovation": llm_result.get("innovation", 0),
        "feasibility": llm_result.get("feasibility", 0),
        "clarity": llm_result.get("clarity", 0),
        "final_score": final_score
    }

    save_evaluation(
        state["proposal_id"],
        evaluation_data
    )

    state.update({
        "rule_score": rule_score,
        "llm_score": llm_score,
        "final_score": final_score,
        "weak_sections": llm_result["weak_sections"],
        "innovation": llm_result.get("innovation", 0),
        "feasibility": llm_result.get("feasibility", 0),
        "clarity": llm_result.get("clarity", 0)
    })

    return state


# -------------------------
# NODE 6 — REFINEMENT
# -------------------------
def refinement_node(state: ProposalState):

    refined = refine_proposal(
        state["proposal"],
        state["weak_sections"]
    )

    state["proposal"] = refined
    state["iteration_count"] += 1

    return state


# -------------------------
# DECISION LOGIC
# -------------------------
def should_refine(state: ProposalState):

    if state["final_score"] >= 70:
        return "accept"

    if state["iteration_count"] >= 2:
        return "accept"

    return "refine"


# -------------------------
# BUILD GRAPH
# -------------------------
def build_graph():

    builder = StateGraph(ProposalState)

    # Nodes
    builder.add_node("expand_idea", idea_expansion_node)
    builder.add_node("guidelines", guideline_node)
    builder.add_node("proposal", proposal_node)
    builder.add_node("budget", budget_node)
    builder.add_node("evaluate", evaluation_node)
    builder.add_node("refine", refinement_node)
    builder.add_node("generate_document", generate_document)

    # Entry
    builder.set_entry_point("expand_idea")

    # Flow
    builder.add_edge("expand_idea", "guidelines")
    builder.add_edge("guidelines", "proposal")
    builder.add_edge("proposal", "budget")
    builder.add_edge("budget", "evaluate")

    builder.add_conditional_edges(
        "evaluate",
        should_refine,
        {
            "refine": "refine",
            "accept": "generate_document"
        }
    )

    builder.add_edge("refine", "evaluate")

    builder.set_finish_point("generate_document")

    return builder.compile()