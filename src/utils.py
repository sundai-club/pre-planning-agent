import re
import ast

def parse_response(response):
    matches = re.findall(r'```json(.*?)```', response, flags=re.DOTALL)
    if not matches:
        return None
    return ast.literal_eval(matches[0])