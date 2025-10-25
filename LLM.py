from openai import OpenAI
import os

class OpenRouter:
    def __init__(self, api_key=None):
        if api_key is None:
            api_key = os.environ['OPENROUTER_API_KEY']

            if api_key is None:
                raise ValueError("API key must be set in environment variable OPENROUTER_API_KEY")
        
        self.client = OpenAI(api_key=api_key,
                             base_url="https://openrouter.ai/api/v1")


        self.api_key = api_key

    def generate_simple(self, prompt: str, model: str = None) -> str:
        if model is None:
            model = "deepseek/deepseek-r1" # change this to use another model
        conversation = self.create_conversation(prompt)

        response = self.client.chat.completions.create(messages=conversation, model=model)
        return response.choices[0].message.content

    def create_conversation(self, prompt : str) -> list[dict]:
        messages = []

        messages.append({"role": "assistant", "content": prompt})

        return messages