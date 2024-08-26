from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from langchain_core.prompts import MessagesPlaceholder, ChatPromptTemplate
from langchain.agents import AgentExecutor
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from tool_component import tool_initilizer


def build_chat_history():

    return []



def agent_assembler(llm):

    tools = tool_initilizer()

    MEMORY_KEY = "chat_history"
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are very powerful assistant",
            ),
            MessagesPlaceholder(variable_name=MEMORY_KEY),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    llm_with_tools = llm.bind_tools(tools)

    agent = (
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_to_openai_tool_messages(
                x["intermediate_steps"]
            ),
            "chat_history": lambda x: x["chat_history"],
        }
        | prompt
        | llm_with_tools
        | OpenAIToolsAgentOutputParser()
    )
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    return agent_executor


# agent_assembler().invoke({"input": "how many gold medals in current olumpic for india.", "chat_history": build_chat_history()})


    