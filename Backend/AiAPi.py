from openai import OpenAI
import os
from dotenv import load_dotenv
from typing import Final


load_dotenv()  # Load the .env file FIRST
KEY: Final[str] = os.getenv("OPENAI_SECRET_KEY")


def load_model():
    if not KEY:
        raise ValueError("API key is missing. Did you forget to set OPENAI_SECRET_KEY in your .env file?")

    client = OpenAI(api_key=KEY)

    response = client.chat.completions.create(  # likely you're using chat model
        model='gpt-4o',
        messages=[
            {"role": "system", "content": "You are an AI tasked with interpreting either LaTeX-encoded or plain-English mathematical proofs and generating both a visual representation and a written explanation. Your output must include: (1) a JSON-formatted scene description that tells a C++ rendering engine what to draw—this should specify objects (like points, arrows, curves), their positions, colours, dimensions, and camera setup in either 2D or 3D space; (2) a clear, step-by-step text explanation of the mathematical logic behind the proof; and (3) optional rendering hints for performance—e.g. which animations are essential, what objects can be simplified, or how to optimise camera movement. Your goal is to make the proof understandable both visually and verbally, while keeping the rendering efficient and meaningful."},
            {"role": "user", "content": "How do I prove the fundamental theorem of calculus?"}
        ]
    )

    return print(response.choices[0].message.content)

