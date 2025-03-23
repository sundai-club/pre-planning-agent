from together_api import TogetherAI
from utils import parse_response

client = TogetherAI()

prompt = """
You are a planner for one of the best task planning agents ever built. 
Your task is to identify if you require access to external data source like Web API to plan for the task user wants to accomplish.

User Task:
{user_task}

Think step by step and give your answer "true" or "false" in the following Output format:

```json{{"web_search": "answer"}}```

Think within the <think> </think> tags only, and based on your reasoning give your answer.

<think>
your thinking here
</think>

Output:
"""

def get_intent(input):
    intent = client.generate(prompt.format(user_task=input))
    if intent:
        return parse_response(intent)
    return {'web_search': True}


