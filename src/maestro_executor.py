import os
from ai21 import AI21Client

api_key = os.getenv("AI21_API_KEY")

client = AI21Client(api_key=api_key)


def execute_task(task):

    run = client.beta.maestro.runs.create_and_poll(
            input=task["input"],
            requirements=task["requirements"],
            tools=task["tools"],
        )
    
    return run

# sample_input = {
#   "input": "Plan a 3-day trip to Paris, focusing on art museums and local cuisine",
#   "requirements": [
#     {
#       "name": "trip duration",
#       "description": "The trip should be exactly 3 days long"
#     },
#     {
#       "name": "location",
#       "description": "The trip should take place in Paris, France"
#     },
#     {
#       "name": "activities",
#       "description": "The trip should include visits to at least 2 art museums"
#     },
#     {
#       "name": "cuisine",
#       "description": "The trip should include trying local French cuisine"
#     },
#   ],
#   "tools": [
#     {
#       "type": "web_search"
#     },]
# }

# print(execute_task(sample_input))
