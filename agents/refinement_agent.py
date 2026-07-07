from llm.groq_client import call_groq_llama
from utils.json_parser import parse_llm_json


def refine_proposal(proposal, weak_sections):

    prompt = f"""
You are an expert research proposal editor.

Improve ONLY the weak sections of the proposal.

Weak Sections:
{weak_sections}

Proposal:
{proposal}

Return ONLY JSON with the improved sections.

JSON structure:

{{
"improved_sections": {{}}
}}
"""

    response = call_groq_llama(prompt)

    refined_json = parse_llm_json(response)

    return refined_json