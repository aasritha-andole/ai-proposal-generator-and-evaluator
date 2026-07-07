import cohere
from config import COHERE_API_KEY

co = cohere.Client(COHERE_API_KEY)

def call_cohere_refine(proposal_text, max_tokens=1500):
    response = co.chat(
        model="command-r-08-2024",  # ✅ correct current model
        message=f"Refine and professionally improve this research proposal:\n\n{proposal_text}",
        max_tokens=max_tokens,
        temperature=0.3,
    )

    return response.text