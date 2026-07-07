from groq import Groq
from config import GROQ_API_KEY  # use config instead of loading .env again

client = Groq(api_key=GROQ_API_KEY)

def call_groq_llama(prompt, max_tokens=1500):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  # ✅ Working model
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=0.4,
    )
    return response.choices[0].message.content


# Temporarily using same model because Mixtral is removed
def call_groq_mixtral(prompt, max_tokens=700):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  # ✅ Same model for now
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=0.3,
    )
    return response.choices[0].message.content
