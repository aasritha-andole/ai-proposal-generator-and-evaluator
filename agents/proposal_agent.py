from llm.groq_client import call_groq_llama
from utils.json_parser import parse_llm_json


def generate_proposal(idea, expanded_idea, guidelines):

    prompt = f"""
You are an expert research proposal writer.

Write a structured research proposal.

Idea:
{idea}

Expanded Idea:
{expanded_idea}

Funding Guidelines:
{guidelines}

Return ONLY valid JSON.

JSON structure:

{{
"title": "",
"abstract": "",
"objectives": [],
"methodology": "",
"expected_results": "",
"timeline": ""
}}
"""

    response = call_groq_llama(prompt)

    proposal_json = parse_llm_json(response)

    return proposal_json

from database.repository import save_proposal
