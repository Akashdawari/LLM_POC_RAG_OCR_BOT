from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import (ChatPromptTemplate, SystemMessagePromptTemplate, 
                               HumanMessagePromptTemplate, PromptTemplate)
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain.output_parsers import PydanticOutputParser
from prompt_template import TEMPLATE
import os




# Data model
class GradeDocuments(BaseModel):
    """Binary score for relevance check on retrieved documents."""

    binary_score: str = Field(
        description="Documents are relevant to the question, 'yes' or 'no'"
    )


# Data model
class GradeHallucinations(BaseModel):
    """Binary score for hallucination present in generation answer."""

    binary_score: str = Field(
        description="Answer is grounded in the facts, 'yes' or 'no'"
    )

# Data model
class GradeAnswer(BaseModel):
    """Binary score to assess answer addresses question."""

    binary_score: str = Field(
        description="Answer addresses the question, 'yes' or 'no'"
    )

class OnlineNeedsChecker(BaseModel):
    """Binary score to assess the need of online resource"""

    binary_score: str = Field(
        description="Is there is a need of online resource to anser the user query, 'yes' or 'no'"
    )


def online_needs_check(question, docs, llm):

    # Prompt
    system = TEMPLATE["online_needs"]["system"]
    user = TEMPLATE["online_needs"]["user"]

    parser = PydanticOutputParser(pydantic_object=GradeDocuments)

    prompt = PromptTemplate(
    template=system,
    input_variables=[],
    partial_variables={"format_instructions": parser.get_format_instructions()}
    )

    system_message_prompt = SystemMessagePromptTemplate(prompt=prompt)

    human_message_prompt = HumanMessagePromptTemplate.from_template(user)

    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])


    retrieval_grader = chat_prompt | llm | parser
    
    k = retrieval_grader.invoke({"question": question, "document": docs})
    return k.binary_score

def search_online(question):

    try:
        search = GoogleSerperAPIWrapper(serper_api_key=os.getenv("SERPER_KEY"))
        result = search.run(question)
        return result
    except Exception as e:
        return "Cannot able to generate online result"


def grade_assigner_chain(question, docs, llm):
    
    # Prompt
    system = TEMPLATE["grade_assigner"]["system"]
    user = TEMPLATE["grade_assigner"]["user"]

    parser = PydanticOutputParser(pydantic_object=GradeDocuments)

    prompt = PromptTemplate(
    template=system,
    input_variables=[],
    partial_variables={"format_instructions": parser.get_format_instructions()}
    )

    system_message_prompt = SystemMessagePromptTemplate(prompt=prompt)

    human_message_prompt = HumanMessagePromptTemplate.from_template(user)

    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])


    retrieval_grader = chat_prompt | llm | parser
    
    k = retrieval_grader.invoke({"question": question, "document": docs})
    return k.binary_score



def rag_chain(question, doc_txt, llm):

    # Prompt
    system = TEMPLATE["rag_prompt"]["system"]
    user = TEMPLATE["rag_prompt"]["user"]

    grade_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            ("human", user),
        ]
    )
    retrieval_grader = grade_prompt | llm | StrOutputParser()
    k = retrieval_grader.invoke({"question": question, "context": doc_txt})
    return k


def hallucination_grader_chain(docs, generation, llm):


    # Prompt
    system = TEMPLATE["hallucination_grader"]["system"]
    user = TEMPLATE["hallucination_grader"]["user"]

    parser = PydanticOutputParser(pydantic_object=GradeHallucinations)

    prompt = PromptTemplate(
    template=system,
    input_variables=[],
    partial_variables={"format_instructions": parser.get_format_instructions()}
    )

    system_message_prompt = SystemMessagePromptTemplate(prompt=prompt)

    human_message_prompt = HumanMessagePromptTemplate.from_template(user)

    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])


    chain = chat_prompt | llm | parser

    k = chain.invoke({"documents": docs, "generation": generation})

    return k.binary_score


def answer_grader_chain(question, generation, llm):


    # Prompt
    system = TEMPLATE["answer_grader"]["system"]
    user = TEMPLATE["answer_grader"]["user"]
    
    parser = PydanticOutputParser(pydantic_object=GradeAnswer)

    prompt = PromptTemplate(
    template=system,
    input_variables=[],
    partial_variables={"format_instructions": parser.get_format_instructions()}
    )

    system_message_prompt = SystemMessagePromptTemplate(prompt=prompt)

    human_message_prompt = HumanMessagePromptTemplate.from_template(user)

    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])


    chain = chat_prompt | llm | parser

    k = chain.invoke({"question": question, "generation": generation})

    return k.binary_score


def question_rewriter_chain(question, llm):


    # Prompt
    system = TEMPLATE["question_rewriter"]["system"]
    user = TEMPLATE["question_rewriter"]["system"]
    re_write_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            ("human", user),
        ]
    )

    question_rewriter = re_write_prompt | llm | StrOutputParser()
    k = question_rewriter.invoke({"question": question})
    return k
