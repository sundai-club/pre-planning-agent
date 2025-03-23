import streamlit as st


st.title("Pre-Planning Agent")

if 'user_task' not in st.session_state:
    user_task = st.text_input("Enter your task/query:")
    st.session_state.user_task = user_task

submit = st.button("Submit")

if submit:
    