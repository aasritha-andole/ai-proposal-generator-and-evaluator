from llm.groq_client import call_groq_llama
from utils.json_parser import parse_llm_json
from graph.state import ProposalState


def generate_guidelines(agency):

    prompt = f"""
You are an expert research funding advisor.

Provide proposal writing guidelines for submitting a research proposal to {agency}.

Return ONLY valid JSON.

JSON structure:

{{
"agency_name": "",
"focus_areas": [],
"proposal_expectations": [],
"evaluation_criteria": [],
"important_tips": []
}}
"""

    response = call_groq_llama(prompt)

    guidelines_json = parse_llm_json(response)

    return guidelines_json


