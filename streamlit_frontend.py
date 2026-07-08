import streamlit as st 
from langgraph_backend import model
from langchain_core.messages import HumanMessage, AIMessage

CONFIG = {"configurable": {"thread_id": "1"}}

if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

for message in st.session_state["message_history"]:
    with st.chat_message(message["role"]):
        st.text(message["content"])

user_input = st.chat_input("Type Here")

if user_input:
    st.session_state["message_history"].append({"role": "user","content": user_input})
    with st.chat_message("user"):
        st.text(user_input)

    messages = []

    for msg in st.session_state["message_history"]:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
            messages.append(AIMessage(content=msg["content"]))

    response = model.invoke(messages, config=CONFIG)
    ai_message = response.content

    st.session_state["message_history"].append({
        "role": "assistant",
        "content": ai_message
    })

    with st.chat_message("assistant"):
        st.text(ai_message)