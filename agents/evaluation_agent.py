from llm.groq_client import call_groq_llama
from utils.json_parser import parse_llm_json


def evaluate_proposal(proposal, guidelines):

    prompt = f"""
You are an expert research proposal reviewer.

Evaluate the proposal according to the funding guidelines.

Proposal:
{proposal}

Guidelines:
{guidelines}

Return ONLY JSON.

JSON structure:

{{
"llm_score": 0-100,
"weak_sections": [],
"review_comments": ""
}}
"""

    response = call_groq_llama(prompt)

    llm_result = parse_llm_json(response)

    return llm_result


def rule_based_score(proposal):

    score = 0

    if proposal.get("abstract"):
        score += 15

    if proposal.get("objectives"):
        score += 20

    if proposal.get("methodology"):
        score += 20

    if proposal.get("expected_results"):
        score += 15

    if proposal.get("timeline"):
        score += 15

    return score