import os
from ai21 import AI21Client
import logging

logging.basicConfig(level=logging.INFO)

api_key = os.getenv("AI21_API_KEY")

client = AI21Client(api_key=api_key)


def execute_task(task):

    run = client.beta.maestro.runs.create_and_poll(
            input=task["input"],
            requirements=task["requirements"],
            tools=task["tools"],
        )
    logging.info(run.id)
    return run.result

