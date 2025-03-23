import os
from together import Together

class TogetherAI:
    def __init__(self):
        self.client = Together()

    def generate(self, prompt: str, model: str="meta-llama/Llama-3.3-70B-Instruct-Turbo", temperature: float=0) -> str:
        response = self.client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt},],
            temperature=temperature,
        )
        return response.choices[0].message.content


# if __name__ == "__main__":
#     ai = TogetherAI()
#     print(ai.generate("Hello, world!"))