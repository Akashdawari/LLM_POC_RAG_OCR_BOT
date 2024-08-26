from typing import List, Optional
from typing_extensions import TypedDict
from chain_component import *
from langgraph.graph import END, StateGraph, START
from langchain_community.chat_models import AzureChatOpenAI
from ingest_component import Document, get_related_documents

# Node defination

class GraphState(TypedDict):

    question: str
    generation: str
    documents: List[Document]
    llm: AzureChatOpenAI
    loop_check: int
    all_docs: List[Document]

# Nodes

def retrieve(state):
    """
    Retrieve documents

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key added to state, documents, that contains retrieved documents
    """
    print("---RETRIEVE---")
    question = state["question"]
    all_docs = state["all_docs"]
    # Retrieval
    documents = get_related_documents(question, all_docs)
    return {"documents": documents, "question": question}


def generate(state):
    """
    Generate answer

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key added to state, generation, that contains LLM generation
    """
    print("---GENERATE---")
    question = state["question"]
    documents = state["documents"]
    loop_check = state["loop_check"]
    llm = state["llm"]
    if not loop_check:
        loop_check=1

    if not documents or loop_check> 2:
        return {"documents": documents, "question": question, "generation": None, "loop_check": loop_check+1}

    # RAG generation
    generation = rag_chain(question, documents, llm)
    return {"documents": documents, "question": question, "generation": generation, "loop_check": loop_check+1}



def grade_documents(state):
    """
    Determines whether the retrieved documents are relevant to the question.

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): Updates documents key with only filtered relevant documents
    """

    print("---CHECK DOCUMENT RELEVANCE TO QUESTION---")
    question = state["question"]
    documents = state["documents"]
    llm = state["llm"]

    # Score each doc
    filtered_docs = []
    for d in documents:
        grade = grade_assigner_chain(question, d.page_content, llm)

        if grade == "yes":
            print("---GRADE: DOCUMENT RELEVANT---")
            filtered_docs.append(d)
        else:
            print("---GRADE: DOCUMENT NOT RELEVANT---")
            continue
    return {"documents": filtered_docs, "question": question}

def transform_query(state):
    """
    Transform the query to produce a better question.

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): Updates question key with a re-phrased question
    """

    print("---TRANSFORM QUERY---")
    question = state["question"]
    documents = state["documents"]
    loop_check = state["loop_check"]
    llm = state["llm"]

    # Re-write question
    better_question = question_rewriter_chain(question, llm)
    return {"documents": documents, "question": better_question, "loop_check": loop_check+1}

# Edge

def decide_to_generate(state):
    """
    Determines whether to generate an answer, or re-generate a question.

    Args:
        state (dict): The current graph state

    Returns:
        str: Binary decision for next node to call
    """

    print("---ASSESS GRADED DOCUMENTS---")
    state["question"]
    filtered_documents = state["documents"]
    loop_check = state["loop_check"]

    if loop_check >  2:
        print("---DECISION: GENERATE Loop Break---")
        return "generate" 

    if not filtered_documents:
        # All documents have been filtered check_relevance
        # We will re-generate a new query
        print(
            "---DECISION: ALL DOCUMENTS ARE NOT RELEVANT TO QUESTION, TRANSFORM QUERY---"
        )
        return "transform_query"
    else:
        # We have relevant documents, so generate answer
        print("---DECISION: GENERATE---")
        return "generate"
    


def grade_generation_v_documents_and_question(state):
    """
    Determines whether the generation is grounded in the document and answers question.

    Args:
        state (dict): The current graph state

    Returns:
        str: Decision for next node to call
    """

    print("---CHECK HALLUCINATIONS---")
    question = state["question"]
    documents = state["documents"]
    generation = state["generation"]
    loop_check = state["loop_check"]
    print(question, generation, loop_check)
    llm = state["llm"]

    if not generation or loop_check >  2:
        return "useful"


    grade = hallucination_grader_chain(documents, generation, llm)

    # Check hallucination
    if grade == "yes":
        print("---DECISION: GENERATION IS GROUNDED IN DOCUMENTS---")
        # Check question-answering
        print("---GRADE GENERATION vs QUESTION---")
        grade = answer_grader_chain(question, generation, llm)
        if grade == "yes":
            print("---DECISION: GENERATION ADDRESSES QUESTION---")
            return "useful"
        else:
            print("---DECISION: GENERATION DOES NOT ADDRESS QUESTION---")
            return "not useful"
    else:
        print("---DECISION: GENERATION IS NOT GROUNDED IN DOCUMENTS, RE-TRY---")
        return "not supported"

def decide_to_online(state):

    print("--DECISION ONLINE SEARCH--")
    question = state["question"]
    docs = state["documents"]
    llm = state["llm"]

    if len(docs):

        result = online_needs_check(question, docs, llm)
        print(f"DECISION RESULT {result}")
        if result == 'yes':
            return "get_online_result"
        else:
            return "generate"
    else:
        print("--go online--")
        return "get_online_result"

def get_online_result(state):

    print("--Online Search-----")
    question = state["question"]
    docs = state["documents"]
    result = search_online(question)
    docs.append(f"Below is the online search result so mention in your answer to make user aware.\n{result}")

    return {"documents": docs}



def rag_machine(rag_type, relevant_docs, question, llm, all_docs):


    if rag_type=="**Simple RAG**":
        workflow = StateGraph(GraphState)
        workflow.add_node("generate_response", generate)

        # Build graph
        workflow.add_edge(START, "generate_response")
        workflow.add_edge("generate_response", END)

        inputs = {"question": question,
              "documents": relevant_docs, 
              "llm": llm}
        
        app = workflow.compile()

        k = app.invoke(inputs).get("generation", None)

        if k:
            return str(k) 
        return """It appears that our system is unable to find the relevant information or answer based on the documents provided in the database. Could you please restructure your query or verify if your query pertains to the documents available in the database?"""

        
    elif rag_type == "***Corrective RAG***":
        workflow = StateGraph(GraphState)
        workflow.add_node("document_grading", grade_documents)
        workflow.add_node("generate", generate)
        workflow.add_node("get_online_result", get_online_result)
        

        # Build graph
        workflow.add_edge(START, "document_grading")
        workflow.add_conditional_edges(
                    "document_grading",
                    decide_to_online,
                    {
                        "get_online_result": "get_online_result",
                        "generate": "generate",
                    },
                )
        workflow.add_edge("get_online_result", "generate")
        workflow.add_edge("generate", END)

        inputs = {"question": question,
              "documents": relevant_docs, 
              "llm": llm}
        
        app = workflow.compile()

        k = app.invoke(inputs).get("generation", None)

        if k:
            return str(k) 
        return """It appears that our system is unable to find the relevant information or answer based on the documents provided in the database. Could you please restructure your query or verify if your query pertains to the documents available in the database?"""


    else:
        workflow = StateGraph(GraphState)
        workflow.add_node("retrieve", retrieve)
        workflow.add_node("grade_documents", grade_documents)
        workflow.add_node("generate", generate)
        workflow.add_node("transform_query", transform_query)

        # # Build graph
        workflow.add_edge(START, "grade_documents")
        workflow.add_conditional_edges(
            "grade_documents",
            decide_to_generate,
            {
                "transform_query": "transform_query",
                "generate": "generate",
            },
        )
        workflow.add_edge("transform_query", "retrieve")
        workflow.add_edge("retrieve", "grade_documents")

        workflow.add_conditional_edges("generate", 
                                       grade_generation_v_documents_and_question,{
                                           "not supported": "generate",
                                            "useful": END,
                                            "not useful": "transform_query",
                                       })


        inputs = {"question": question,
              "documents": relevant_docs, 
              "llm": llm, 
              "loop_check": 0,
              "all_docs": all_docs}
        
        app = workflow.compile()

        k = app.invoke(inputs).get("generation", None)

        if k:
            return str(k) 
        return """It appears that our system is unable to find the relevant information or answer based on the documents provided in the database. Could you please restructure your query or verify if your query pertains to the documents available in the database?"""
