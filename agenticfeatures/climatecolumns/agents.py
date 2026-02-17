import requests
import pathlib
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool
import os
from langchain.messages import ToolMessage
from langchain.messages import AnyMessage
from typing_extensions import TypedDict, Annotated
import operator
from langchain.agents import create_agent
from langgraph.graph import StateGraph, START, END
from agenticfeatures.climatecolumns.tools import searchforpapers, ResearchDocument



BASE_DIR = pathlib.Path(__file__).parent.parent
LOCAL_ENV = BASE_DIR / 'config' / '.env'

if LOCAL_ENV.exists():
    load_dotenv(dotenv_path=LOCAL_ENV)
else:
    load_dotenv()

gemini_api_key = os.getenv('GEMINI_API_KEY')

gemini_model = model = ChatGoogleGenerativeAI(
    model="gemini-3-pro-preview",
    api_key=gemini_api_key,
    temperature=1
)

class NewsDict(TypedDict):
    title: str
    focus: str

class FocusArea(TypedDict):
    area: str
    documents: list[str]
    newses: list[NewsDict]


tools = [searchforpapers]

tools_by_name = {tool.name: tool for tool in tools}

class FocusAreaList(TypedDict):
    focus_areas: list[FocusArea]

class State(TypedDict):
    documents: Annotated[list[ResearchDocument], operator.add]
    focus_area : Annotated[list[FocusArea], operator.add]
    messages: Annotated[list[AnyMessage], operator.add]
    status: str

"""

Agentic Workflow for generating research and news based articles
"""

def generate_articles(api_key : str = os.getenv('GEMINI_API_KEY')):
    graphBuilder = StateGraph(State)

    def research_fetcher(state: State):
        documents = searchforpapers.invoke({})
        return {"documents": documents, "messages": [], "focus_area": [], "status": "papers fetched"}

    graphBuilder.add_node("paper_fetcher", research_fetcher)
    graphBuilder.add_edge(START, "paper_fetcher")



    def focus_area_finder(state: State):

        documents = state["documents"]
        formatted_docs = ""
        for i, doc in enumerate(documents, 1):
            formatted_docs += f"""
            Document {i}:
            Title: {doc['title']}
            Abstract: {doc['abstract']}
            """

            prompt = f"""
                        Group the following research documents into distinct focus areas.

                        {formatted_docs}

                        Rules:
                        - Each focus area must be unique.
                        - If multiple documents belong to the same theme, group them.
                        - Output ONLY structured JSON.
                        - Do not add newses. Leave newses as empty list.
                        """
        agent = create_agent(model=model, system_prompt = "Your job is to find focus areas from the list of documents and group them together in a list",

    response_format=FocusAreaList)

        response = agent.invoke({"messages": [{"role" : "user", "content" : prompt}]})
        structured_response = response["structured_response"]
        return {
            "focus_area":structured_response["focus_areas"] ,
            "status": "discovered_focus areas"
        }
    graphBuilder.add_node("focus_area_finder", focus_area_finder)
    graphBuilder.add_edge("paper_fetcher", "focus_area_finder")
    graphBuilder.add_edge("focus_area_finder", END)
    graph = graphBuilder.compile()
    state = graph.invoke({})
    return state















