import streamlit as st
from typing import List, Dict
import requests

st.set_page_config(page_title="Pre-Planning Agent", layout="wide")


if 'stage' not in st.session_state:
    st.session_state.stage = "input"  
if 'user_task' not in st.session_state:
    st.session_state.user_task = ""
if 'plans' not in st.session_state:
    st.session_state.plans = []
if 'selected_plan' not in st.session_state:
    st.session_state.selected_plan = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'final_response' not in st.session_state:
    st.session_state.final_response = ""

def generate_initial_plans(task: str) -> List[Dict]:

    plans = requests.post("http://localhost:8000/get_plan", json={"user_intent": task})
    plan1 = plans.json()['plan_option_1']
    plan2 = plans.json()['plan_option_2']
    
    return [plan1, plan2]

def process_chat_message(message: str, plan: Dict) -> Dict:

    updated_plan = requests.post("http://localhost:8000/refine_plan", json={"current_plan": plan, "suggestion": message})
    return updated_plan.json()["updated_plan"]

def execute_plan(plan: Dict) -> str:
    execution_result = requests.post("http://localhost:8000/execute_plan", json={"plan": plan})
    return execution_result.json()["result"]

st.title("Pre-Planning Agent")

if st.session_state.stage == "input":
    st.header("Step 1: Enter Your Task")
    
    task_input = st.text_area("Describe your task in detail:", height=150)
    
    if st.button("Generate Plans"):
        if task_input.strip():
            st.session_state.user_task = task_input
            st.session_state.plans = generate_initial_plans(task_input)
            st.session_state.stage = "plan_selection"
            st.rerun()
        else:
            st.error("Please enter a task description.")

elif st.session_state.stage == "plan_selection":
    st.header("Step 2: Select a Plan")
    
    st.write(f"Task: {st.session_state.user_task}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("Plan A")
        st.write(st.session_state.plans[0])
        if st.button("Select Plan A"):
            st.session_state.selected_plan = st.session_state.plans[0]
            st.session_state.stage = "refinement"
            st.rerun()
    
    with col2:
        st.write("Plan B")
        st.write(st.session_state.plans[1])
        
        if st.button("Select Plan B"):
            st.session_state.selected_plan = st.session_state.plans[1]
            st.session_state.stage = "refinement"
            st.rerun()
    
    if st.button("Start Over", key="start_over_plan"):
        st.session_state.stage = "input"
        st.rerun()

elif st.session_state.stage == "refinement":
    st.header("Step 3: Refine Your Plan")
    
    with st.expander("Selected Plan", expanded=True):
        st.write(st.session_state.selected_plan)
    
    st.subheader("Plan Refinement Chat")
    chat_container = st.container()
    
    with chat_container:
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.write(f"You: {msg['content']}")
            else:
                st.write(f"Agent: {msg['content']}")
    
    user_message = st.text_input("Enter your suggestions or questions about the plan:")
    
    if st.button("Send"):
        if user_message.strip():
            st.session_state.chat_history.append({"role": "user", "content": user_message})
            
            st.session_state.selected_plan = process_chat_message(user_message, st.session_state.selected_plan)
            
            agent_response = "I've updated the plan based on your input. You can continue refining or execute the plan when ready."
            st.session_state.chat_history.append({"role": "agent", "content": agent_response})
            
            st.rerun()
    
    if st.button("Execute Plan"):
        st.session_state.final_response = execute_plan(st.session_state.selected_plan)
        st.session_state.stage = "final"
        st.rerun()
    
    if st.button("Start Over", key="start_over_refine"):
        st.session_state.stage = "input"
        st.rerun()

elif st.session_state.stage == "final":
    st.expander("Selected Plan", expanded=True).write(st.session_state.selected_plan)
    st.header("Step 4: Final Result")
    
    st.markdown(st.session_state.final_response)
    
    if st.button("Start New Task"):
        st.session_state.stage = "input"
        st.session_state.user_task = ""
        st.session_state.plans = []
        st.session_state.selected_plan = None
        st.session_state.final_response = ""
        st.rerun()