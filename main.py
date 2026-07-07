from graph.proposal_graph import build_graph
from database.models import create_tables


def run_pipeline(idea, agency):

    create_tables()

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

    return result


# ✅ ONLY FOR LOCAL TESTING (won’t affect Streamlit)
if __name__ == "__main__":

    sample_idea = "AI system for early crop disease detection using drone imagery"
    sample_agency = "DST"

    result = run_pipeline(sample_idea, sample_agency)

    print("\nFINAL RESULT\n")
    print(result)