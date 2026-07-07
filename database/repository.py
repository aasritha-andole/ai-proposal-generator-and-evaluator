from database.db import get_connection
import json
from retrieval.embedder import get_embedding
from database.db import get_connection

def save_proposal(idea, agency, proposal):

    conn = get_connection()
    cursor = conn.cursor()

    # Generate embedding for similarity search
    embedding = get_embedding(idea)

    cursor.execute("""
    INSERT INTO proposals (
        idea,
        agency,
        title,
        abstract,
        methodology,
        timeline,
        embedding
    )
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        idea,
        agency,
        proposal["title"],
        proposal["abstract"],
        proposal["methodology"],
        proposal["timeline"],
        json.dumps(embedding)
    ))

    proposal_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return proposal_id


def save_budget(proposal_id, budget):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO budgets (
        proposal_id,
        personnel_cost,
        equipment_cost,
        software_cost,
        misc_cost,
        total_budget
    )
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        proposal_id,
        budget["personnel_cost"],
        budget["equipment_cost"],
        budget["software_cost"],
        budget["miscellaneous_cost"],
        budget["total_budget"]
    ))

    conn.commit()
    conn.close()


def save_evaluation(proposal_id, evaluation):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO evaluations (
        proposal_id,
        innovation_score,
        feasibility_score,
        clarity_score,
        final_score
    )
    VALUES (?, ?, ?, ?, ?)
    """, (
        proposal_id,
        evaluation["innovation"],
        evaluation["feasibility"],
        evaluation["clarity"],
        evaluation["final_score"]
    ))

    conn.commit()
    conn.close()