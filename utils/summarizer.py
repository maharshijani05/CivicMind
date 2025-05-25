from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def summarize_policy(text):
    prompt = f"Summarize the following policy in 3-5 bullet points:\n\n{text}"
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()
