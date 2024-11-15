import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()
env = {
    'organization': os.getenv('OPENAI_ORGANIZATION'),
    'project': os.getenv('OPENAI_PROJECT'),
    'api_key': os.getenv('OPENAI_API_KEY')
}

client = OpenAI(
  organization=env['organization'],
  project=env['project'],
  api_key=env["api_key"]
)

def get_categories(input: str) -> list:
    messages = [
        {"role": "system", "content": "You will be given a math problem, and you must provide a comma-separated list (no whitespace) consisting of as many uniquely categorizing key terms of the problem as possible in order of relevance. The list should be no longer than 25 items. Output nothing else but the list."},
        {"role": "user", "content": input}
        ]
    
    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        stream=True,
        temperature=0,
        max_tokens=64
    )

    response = ""
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            response += chunk.choices[0].delta.content

    return response.split(',')


if __name__ == "__main__":
    # Example usage
    print(get_categories(input="x^2 + 1 = 0. Solve for x."))
