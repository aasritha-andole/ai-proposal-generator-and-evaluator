import json
from llm.groq_client import call_groq_llama
from utils.json_parser import parse_llm_json
from graph.state import ProposalState


def expand_idea(idea):

    prompt = f"""
You are an expert research ideation assistant.

Expand the research idea below into a detailed concept.

Idea:
{idea}

Return ONLY valid JSON.

JSON structure:

{{
"expanded_idea": "",
"key_research_components": [],
"possible_methodologies": [],
"potential_impact": ""
}}
"""

    response = call_groq_llama(prompt)

    expanded_json = parse_llm_json(response)

    return expanded_json


def idea_expansion_node(state: ProposalState):

    expanded = expand_idea(state["idea"])

    return {"expanded_idea": expanded}