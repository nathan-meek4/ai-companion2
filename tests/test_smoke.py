import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("API_KEY"))

resp = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "user", "content": "Hello! Testing my API setup."}
    ]
)

print(resp.choices[0].message["content"])
