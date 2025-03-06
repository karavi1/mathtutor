import os
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI
import json

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Step 1: Problem Decomposition
class SolutionStep(BaseModel):
    explanation: str
    output: str
    difficulty: int  # Numeric difficulty score from 1-5

class MathSolution(BaseModel):
    steps: List[SolutionStep]
    final_answer: str
    
def generate_solution_steps(problem: str) -> MathSolution:
  """Generates a step-by-step solution for a given math problem."""
  prompt = f"""
  Solve the following math problem step by step.
  Respond **only** with a valid JSON object matching this format:
  
  {{
      "steps": [
          {{"explanation": "Step description", "output": "Equation or result", "difficulty": 2}}
      ],
      "final_answer": "The final solution"
  }}

  Problem: {problem}
  """

  completion = client.chat.completions.create(
      model="gpt-4o",
      messages=[{"role": "system", "content": prompt}]
  )

  response_content = completion.choices[0].message.content.strip()

  try:
      return MathSolution.model_validate_json(response_content)
  except Exception as e:
      print(f"Error parsing OpenAI response: {response_content}")
      raise e



# Step 2: Solution Classification
class StepCategory(str, Enum):
    TOPIC = "TOPIC"
    METHOD = "METHOD"

class ClassifiedStep(BaseModel):
    step_number: int
    category: StepCategory
    tags: List[str]
    difficulty: int  # Difficulty score from 1-5

class SolutionClassification(BaseModel):
    classified_steps: List[ClassifiedStep]

def classify_solution_steps(solution: MathSolution) -> SolutionClassification:
    """Classifies solution steps into topic/method and assigns difficulty."""
    
    prompt = f"""
    Classify the following solution steps by topic and method, and assign a difficulty score from 1 to 5.
    Respond ONLY with a valid JSON object that follows this exact format:
    
    {{
        "classified_steps": [
            {{"step_number": 1, "category": "TOPIC", "tags": ["Algebra", "Equation Solving"], "difficulty": 2}},
            {{"step_number": 2, "category": "METHOD", "tags": ["Division"], "difficulty": 3}}
        ]
    }}
    
    Here are the solution steps:
    {solution.model_dump_json()}
    """
    
    classification_response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": prompt}]
    )
    
    response_content = classification_response.choices[0].message.content.strip()
    
    # Remove possible markdown JSON formatting
    if response_content.startswith("```json"):
        response_content = response_content[7:-3].strip()
    
    try:
        parsed_json = json.loads(response_content)  # Ensure it's valid JSON
        return SolutionClassification.model_validate(parsed_json)  # Validate against Pydantic model
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {response_content}")
        raise e
    except Exception as e:
        print(f"Error parsing OpenAI response: {response_content}")
        raise e


# Step 3: Obstacle Identification
def get_obstacle_steps(solution: MathSolution) -> List[int]:
    """Prompts the student to indicate which solution steps were difficult."""
    print("Take a look at your solution steps. Which step(s) were challenging for you?")
    for i, step in enumerate(solution.steps, start=1):
        print(f"{i}. {step.explanation} -> {step.output}")
    
    user_input = input("Enter the step numbers where you struggled (comma-separated), or press Enter if all steps were clear: ")
    difficult_steps = list(map(int, user_input.split(','))) if user_input else []
    
    if not difficult_steps:
        print("Awesome job! You understood everything. Keep up the good work!")
    
    return difficult_steps


# Step 4: Problem Suggestion
def generate_new_problem(classification: SolutionClassification, difficult_steps: List[int]) -> Optional[str]:
    """Suggests a new math problem based on student struggles and classification."""
    if not difficult_steps:
        return None
    
    prompt = f"""
    You are an AI tutor. Given the classified steps of a math solution, suggest a new problem that reinforces similar concepts but introduces a slight challenge.
    
    Steps:
    {classification.model_dump_json()}
    
    The student struggled with these steps: {difficult_steps}
    
    Suggested New Problem:
    """
    
    suggestion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": prompt}
        ]
    )
    
    return suggestion.choices[0].message.content.strip()


# Example Usage
if __name__ == "__main__":
    example_problems = [
        "how can I solve 8x + 7 = -23",
        "solve for x: 3(x - 5) + 2 = 14",
        "find the roots of x^2 - 4x + 4 = 0"
    ]
    
    for problem in example_problems:
        print(f"\nLet's solve this problem together: {problem}")
        solution = generate_solution_steps(problem)
        difficult_steps = get_obstacle_steps(solution)
        classification = classify_solution_steps(solution)
        
        new_problem = generate_new_problem(classification, difficult_steps)
        if new_problem:
            print("Here's a new problem to help reinforce your learning:", new_problem)
