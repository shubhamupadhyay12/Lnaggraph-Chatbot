from langgraph.graph import StateGraph , START , END 
from typing import TypedDict , Annotated 
from langchain_huggingface import HuggingFaceEndpoint , ChatHuggingFace
from langchain_core.messages import HumanMessage 
from dotenv import load_dotenv
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import add_messages

load_dotenv()

llm = HuggingFaceEndpoint(repo_id ="Qwen/Qwen2.5-7B-Instruct")
model = ChatHuggingFace(llm=llm)

class Chatstate(TypedDict):
    
    messages : Annotated[list, add_messages]
    
    
def chat_node(state:Chatstate):
    messages = state['messages']
    response = model.invoke(messages)
    return {'messages':[response]}

#checkpointer
checkpointer = InMemorySaver()

graph = StateGraph(Chatstate)
graph.add_node('chat_node',chat_node)
graph.add_edge(START,'chat_node')
graph.add_edge('chat_node',END)

chatbot = graph.compile(checkpointer=checkpointer)


