import json
import re


def parse_llm_json(response: str):

    try:
        return json.loads(response)

    except json.JSONDecodeError:

        # remove ```json ``` blocks
        cleaned = re.sub(r"```json", "", response)
        cleaned = re.sub(r"```", "", cleaned)

        # extract first json object
        match = re.search(r"\{.*\}", cleaned, re.DOTALL)

        if match:
            json_str = match.group()
            return json.loads(json_str)

        raise ValueError("No valid JSON found in LLM response")