#!/usr/bin/env python
# coding: utf-8

# # AI21 x Sundai
# ## Prerequisites
# login and get your API Key with your credentials to https://studio.ai21.com/

# In[1]:


get_ipython().system(' pip install ai21')


# In[5]:


from ai21 import AI21Client

api_key = ""

client = AI21Client(api_key=api_key)


# ## Examples

# In[6]:


run = client.beta.maestro.runs.create_and_poll(
    input="Write a poem about hackathons",
    requirements=[
        {
            "name": "length requirement",
            "description": "The length of the poem should be exactly 5 lines",
        },
    ]
)

print(run.result)


# In[13]:


import json

def parse_and_run_llm_output(json_output, client):
    """
    Parse the JSON output from an LLM and feed the extracted data to the maestro model.
    
    Parameters:
      json_output (str): JSON string output from the LLM.
      client: A client instance with access to client.beta.maestro.runs.create_and_poll.
      
    Returns:
      The result from the maestro model run.
      
    Raises:
      ValueError: If the JSON is invalid or required fields are missing.
    """
    try:
        # Parse the JSON string into a dictionary
        data = json.loads(json_output)
    except json.JSONDecodeError as e:
        raise ValueError("Invalid JSON output") from e

    # List of required fields that must be in the JSON
    required_fields = ["inpt", "name", "description", "text", "tool"]
    missing_fields = [field for field in required_fields if field not in data]
    
    if missing_fields:
        raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")
    
    # Extract the values from the JSON data
    inpt = data["inpt"]
    name = data["name"]
    description = data["description"]
    text = data["text"]
    tool = data["tool"]

    # Call the maestro model using the extracted values
    run = client.beta.maestro.runs.create_and_poll(
        input=inpt,
        requirements=[
            {
                "name": name,
                "description": description,
            }
        ],
        context={"text": text},
        tools=[{"type": tool}],
    )
    
    return run.result

# Example usage:
if __name__ == "__main__":
    # Sample JSON output from the LLM
    sample_json = """
    {
      "inpt": "Write a poem about hackathons",
      "name": "length requirement",
      "description": "The length of the poem should be exactly 5 lines",
      "text": "the hackathon is happening in MIT, so all of the people here are nerd",
      "tool": "web_search"
    }
    """
    
    # Assuming 'client' is an already authenticated client object that has the beta.maestro API
    try:
        result = parse_and_run_llm_output(sample_json, client)
        print("Maestro model result:", result)
    except Exception as e:
        print("Error:", e)


# In[7]:


run = client.beta.maestro.runs.create_and_poll(
    input="analyze the following text and determine who is the best pokemon ever",
    context={"text": "Psyduck is the best pokemon"},
)

print(run.result)


# In[8]:


run = client.beta.maestro.runs.create_and_poll(
    input="What's the weather in Boston?",
    tools=[{"type": "web_search"}],
)

print(run.result)


# In[ ]:


# you'll need to upload a file through AI21 Studio
run = client.beta.maestro.runs.create_and_poll(
    input="your question here",
    tools=[{"type": "file_search"}],
)

print(run.result)

