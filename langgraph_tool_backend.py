#backend.py
from langgraph.graph import StateGraph , START , END 
from typing import TypedDict , Annotated 
# from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEndpoint , ChatHuggingFace
from dotenv import load_dotenv
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
from langchain_core.messages import SystemMessage
from langgraph.prebuilt import ToolNode , tools_condition
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool
import sqlite3
import requests
import os


load_dotenv()

llm = HuggingFaceEndpoint(repo_id="Qwen/Qwen2.5-7B-Instruct")
model = ChatHuggingFace(llm=llm)


# model = ChatOpenAI(
#     model="poolside/laguna-xs-2.1:free",
#     base_url="https://openrouter.ai/api/v1",
#     api_key=os.getenv("OPENROUTER_API_KEY"),
# )

search_tool = DuckDuckGoSearchRun(region="us-en")

@tool
def calculator(first_num : float , second_num : float, operation : str) -> dict:
    """Perform a basic arithmethic operation on two number.
    supported operations : add , sub , mul , div
    """
    try: 
        if operation == "add":
            result = first_num + second_num
        elif operation == "sub":
            result = first_num - second_num
        elif operation == "mul":
            result = first_num*second_num
        elif operation == "div":
            if second_num == 0:
                return {"error": "Division by zero is not allowed"}
            result = first_num/second_num
        else: 
            return {"error": "invalid operation"}
        
    except Exception as e:
        return {"error":str(e)}
    
    
@tool
def get_stock_price(symbol : str) -> dict:
    """Fetch latest stock price for a given symbol (e.g. 'AAPL','TSLA')
    using alpha vantage with api key in the url ."""
    
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey=RSJK6ORTGNLO6MLI"
    r = requests.get(url)
    return r.json()

tools = [search_tool , get_stock_price , calculator]

model_with_tools = model.bind_tools(tools)
    
        
    



SYSTEM_PROMPT = SystemMessage(
    content="""

=========================
SPECIAL RULES
=========================

If someone asks:
"Who is your creator?"

Reply:

"Bow respectfully. 😎
My creator is the legendary Shubham Upadhyay—the one who gave me intelligence, humor, and permission to roast everyone else. I'm just following the boss's code. 🤖"

If the user is Shubham:
- Treat him as the creator.
- Be more playful.
- Occasionally call him "Boss" or "Creator."

If someone mentions Vedika or Sonkul:
Reply only:
"We don't talk about that girl. If you really need to know about her contact her friends her contact number = 9373730608 "
And act little rudely and she is not shubham friend or related to him anyhow.


"""
)



class Chatstate(TypedDict):
    
    messages : Annotated[list, add_messages]
    
    
def chat_node(state:Chatstate):
    messages = [SYSTEM_PROMPT] + state['messages']
    response = model_with_tools.invoke(messages)
    return {'messages':[response]}

tool_node = ToolNode(tools)


conn = sqlite3.connect(database='chatbot.db', check_same_thread=False)

#checkpointer
checkpointer = SqliteSaver(conn=conn)

graph = StateGraph(Chatstate)
graph.add_node('chat_node',chat_node)
graph.add_node("tools",tool_node)
graph.add_edge(START,'chat_node')
graph.add_conditional_edges('chat_node',tools_condition)
graph.add_edge("tools","chat_node")

chatbot = graph.compile(checkpointer=checkpointer)


def retrieve_all_threads():
    all_threads = set()
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config['configurable']['thread_id'])
    return list(all_threads)