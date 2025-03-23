import streamlit as st
from typing import List, Dict

# Set page title
st.set_page_config(page_title="Pre-Planning Agent", layout="wide")

# Initialize session state variables
if 'stage' not in st.session_state:
    st.session_state.stage = "input"  # Possible values: input, plan_selection, refinement, execution, final
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

# Function to generate initial plans
def generate_initial_plans(task: str) -> List[Dict]:
    # In a real application, this would call an AI service or use custom logic
    # For demo purposes, we'll create simple placeholder plans
    plan1 = {
        "title": f"Plan A for: {task}",
        "steps": [
            "Research relevant information",
            "Analyze key components",
            "Develop preliminary solution",
            "Test and validate approach"
        ],
        "estimated_time": "2-3 hours",
        "complexity": "Medium"
    }
    
    plan2 = {
        "title": f"Plan B for: {task}",
        "steps": [
            "Break down task into sub-components",
            "Prioritize critical elements",
            "Implement rapid prototype",
            "Iterate based on feedback"
        ],
        "estimated_time": "1-2 hours",
        "complexity": "Low"
    }
    
    return [plan1, plan2]

# Function to process chat message and update plan
def process_chat_message(message: str, plan: Dict) -> Dict:
    # In a real application, this would use an AI to refine the plan
    # For demo purposes, we'll just append the message to the plan
    updated_plan = plan.copy()
    updated_plan["steps"].append(f"New step based on: {message}")
    return updated_plan

# Function to execute plan and generate final response
def execute_plan(plan: Dict) -> str:
    # In a real application, this would execute the plan using AI or other logic
    # For demo purposes, we'll create a simple response
    steps_text = "\n".join([f"- {step}" for step in plan["steps"]])
    return f"""
    ## Executed Plan: {plan['title']}
    
    ### Steps Completed:
    {steps_text}
    
    ### Results
    The plan was executed successfully with {plan['complexity']} complexity.
    Total time spent: {plan['estimated_time']}.
    
    ### Summary
    The task was completed according to the refined plan. All objectives were met.
    """

# Main app layout
st.title("Pre-Planning Agent")

# Stage 1: User Input
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

# Stage 2: Plan Selection
elif st.session_state.stage == "plan_selection":
    st.header("Step 2: Select a Plan")
    
    st.write(f"Task: {st.session_state.user_task}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(st.session_state.plans[0]["title"])
        st.write("Steps:")
        for step in st.session_state.plans[0]["steps"]:
            st.write(f"- {step}")
        st.write(f"Estimated Time: {st.session_state.plans[0]['estimated_time']}")
        st.write(f"Complexity: {st.session_state.plans[0]['complexity']}")
        
        if st.button("Select Plan A"):
            st.session_state.selected_plan = st.session_state.plans[0]
            st.session_state.stage = "refinement"
            st.rerun()
    
    with col2:
        st.subheader(st.session_state.plans[1]["title"])
        st.write("Steps:")
        for step in st.session_state.plans[1]["steps"]:
            st.write(f"- {step}")
        st.write(f"Estimated Time: {st.session_state.plans[1]['estimated_time']}")
        st.write(f"Complexity: {st.session_state.plans[1]['complexity']}")
        
        if st.button("Select Plan B"):
            st.session_state.selected_plan = st.session_state.plans[1]
            st.session_state.stage = "refinement"
            st.rerun()
    
    if st.button("Start Over", key="start_over_plan"):
        st.session_state.stage = "input"
        st.rerun()

# Stage 3: Plan Refinement Chat
elif st.session_state.stage == "refinement":
    st.header("Step 3: Refine Your Plan")
    
    # Display selected plan
    with st.expander("Selected Plan", expanded=True):
        st.subheader(st.session_state.selected_plan["title"])
        st.write("Steps:")
        for step in st.session_state.selected_plan["steps"]:
            st.write(f"- {step}")
        st.write(f"Estimated Time: {st.session_state.selected_plan['estimated_time']}")
        st.write(f"Complexity: {st.session_state.selected_plan['complexity']}")
    
    # Chat history
    st.subheader("Plan Refinement Chat")
    chat_container = st.container()
    
    with chat_container:
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.write(f"You: {msg['content']}")
            else:
                st.write(f"Agent: {msg['content']}")
    
    # Chat input
    user_message = st.text_input("Enter your suggestions or questions about the plan:")
    
    if st.button("Send"):
        if user_message.strip():
            # Add user message to chat history
            st.session_state.chat_history.append({"role": "user", "content": user_message})
            
            # Update the plan based on user input
            st.session_state.selected_plan = process_chat_message(user_message, st.session_state.selected_plan)
            
            # Add agent response to chat history
            agent_response = "I've updated the plan based on your input. You can continue refining or execute the plan when ready."
            st.session_state.chat_history.append({"role": "agent", "content": agent_response})
            
            st.rerun()
    
    # Execute plan button
    if st.button("Execute Plan"):
        st.session_state.final_response = execute_plan(st.session_state.selected_plan)
        st.session_state.stage = "final"
        st.rerun()
    
    if st.button("Start Over", key="start_over_refine"):
        st.session_state.stage = "input"
        st.rerun()

# Stage 4: Final Response
elif st.session_state.stage == "final":
    st.header("Step 4: Final Result")
    
    st.markdown(st.session_state.final_response)
    
    if st.button("Start New Task"):
        # Reset all session state except history (could be useful to keep)
        st.session_state.stage = "input"
        st.session_state.user_task = ""
        st.session_state.plans = []
        st.session_state.selected_plan = None
        st.session_state.final_response = ""
        st.rerun()