import os
from openai import OpenAI

class LlmEngine:
    def __init__(self):
        api_key = os.getenv("API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY environment variable missing!")

        self.client = OpenAI(api_key=api_key)

    def analyze_image(self, jpeg_bytes: bytes, prompt: str):
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",   # cheap/light model for testing
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "input_image", "image": jpeg_bytes},
                    ]
                }
            ]
        )

        return response.choices[0].message["content"]
