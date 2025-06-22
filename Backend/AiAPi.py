import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import Final
import google.generativeai as genai

load_dotenv()

class ModelLoader:
    def __init__(self):
        self.key_openai: Final[str] = os.getenv("OPENAI_SECRET_KEY")
        self.key_google: Final[str] = os.getenv("GOOGLE_GEMINI_API_KEY")

        if not self.key_openai:
            raise ValueError("Missing OPENAI_SECRET_KEY in .env file.")
        if not self.key_google:
            raise ValueError("Missing GOOGLE_GEMINI_API_KEY in .env file.")

        self.openai_client = OpenAI(api_key=self.key_openai)
        genai.configure(api_key=self.key_google)

    def load_model_openai(self, proof: str) -> str:
        response = self.openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": (
                    "You are an AI tasked with interpreting either LaTeX-encoded or "
                    "plain-English mathematical proofs and generating both a visual "
                    "representation and a written explanation. Your output must include: "
                    "(1) a JSON-formatted scene description for a C++ rendering engine, "
                    "(2) a step-by-step explanation of the logic, and (3) performance hints.")},
                {"role": "user", "content": proof}
            ]
        )
        return response.choices[0].message.content

    def load_model_google_gemini(self, proof: str) -> str:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(proof)
        return response.text