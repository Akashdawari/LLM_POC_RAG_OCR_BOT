import os
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain.agents import tool
from datetime import datetime


@tool
def current_datetime() -> str:
    'This tool help you to get the current datetime which helps you in search online'
    return str(datetime.now())


@tool
def search_online(question: str) -> str:

    """The tool is used to search onilne query.
    The input of the tool is a google query of type string."""

    try:
        search = GoogleSerperAPIWrapper(serper_api_key=os.getenv("SERPER_KEY"))
        result = search.run(question)
        return result
    except Exception as e:
        return "Cannot able to generate online result"
    


def tool_initilizer():
    

    tool_list = [search_online, current_datetime]

    return tool_list