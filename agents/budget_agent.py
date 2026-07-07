from llm.groq_client import call_groq_llama
from utils.json_parser import parse_llm_json


def generate_budget(proposal, agency):

    prompt = f"""
You are an expert research grant financial planner.

Generate a research project budget.

Proposal:
{proposal}

Agency:
{agency}

Return ONLY valid JSON.

JSON structure:

{{
"personnel_cost": "",
"equipment_cost": "",
"software_cost": "",
"miscellaneous_cost": "",
"total_budget": ""
}}
"""

    response = call_groq_llama(prompt)

    budget_json = parse_llm_json(response)

    return budget_json