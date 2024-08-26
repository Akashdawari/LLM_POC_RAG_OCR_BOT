import warnings
import os
import json

from langchain.prompts import (ChatPromptTemplate, SystemMessagePromptTemplate, 
                               HumanMessagePromptTemplate, PromptTemplate)
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List, Optional
from langchain.output_parsers import PydanticOutputParser
from langchain.chains import LLMChain
from datetime import  datetime
from llm_initilizer import llm_instance_builder
from prompt_template import TEMPLATE


# Ignore all warnings
warnings.filterwarnings("ignore")

class Item(BaseModel):
    ItemName: str = Field(description="""Item name mentioned in the text""")
    ItemQuantity: int = Field(description="""number of items or the quanity of the item mentioned in the text""")
    ItemPrice: float = Field(description = """calue or the price of the item""")

class Invoice(BaseModel):
    IsInvoice: bool = Field(description="""True if the text is of any kind of invoice or receipt else False if its other text.""")
    InvoiceNumber: Optional[str] = Field(description="It is the unique number or id for the perticular invoice or receipt")
    CustomerName: Optional[str] = Field(description="""the name of the customer mention in the invoice or the receipt.""")
    DateOfIssue: Optional[str] = Field(description="""Date of the invoice or receipt created""")
    Address: Optional[str] = Field(description="""address of the customer mention in the invoice or the receipt""")
    ItemDetails: Optional[List[Item]] = Field(description="""Item details mention in  the text like price, name and quantity.""")
    Currency: Optional[str] = Field(description="""currency of the item's price or values.""")

class Passanger(BaseModel):
    PassangerName: str = Field(description="""The name of the passanger mention in the raw text.""")
    PassangerAge: Optional[str] = Field(description="The age of the passanger mention in the raw text")
    PassangerSeat: Optional[str] = Field(description = "Details of the seat provided, mention in the raw text.")



class TravelTicket(BaseModel):
    IsTicket: bool = Field(description="True if the provided text is of a ticket of flight, train or any kind of travel ticket, else False")
    TicketType: Optional[str] = Field(description="The type of ticket like flight ticket or train ticket or ubur or ship etc.")
    PassangerDetails: Optional[List[Passanger]] = Field(description="""The details of the passanger mention in the raw text.""")
    PNR: Optional[str] = Field(description="It is the PNR (Passenger Name Record) mention in the raw text.")
    ETicketNumber: Optional[str] = Field(description="""It is the 'trip number/ID' or 'E-Ticket' or 'ticket number' or 'TR' mention in the raw text.""")
    Email: Optional[str] = Field(description="""It is the email id of the passanger mention in the ticket data""")
    TransportName: Optional[str] = Field(description="""It is the transport  name like airline name or train name etc mention in raw text.""")
    Price: Optional[float] = Field(description="""Total cost of the flight mention in the ticket. If it is not provided then pass None.""")
    Currency: Optional[str] = Field(description="Currency of the tricket value/price mention in the raw text.")
    DateOfTravel: Optional[datetime] = Field(description="The date of travel when the passenger going to onboard mention in the raw text")
    ArrivalDate: Optional[datetime] = Field(description="The datetime of arrival when the passenger going to arive mention in the raw text")
    OnboardingAt: Optional[str] = Field(description="The place name from where the passanger will onboard from, mention in the raw text")
    Destination: Optional[str] = Field(description="The place name where the passanger is going or the final destination mention in the raw text")

class IdentityCard(BaseModel):
    IsIDCard: bool = Field(description = "True if the provided text is of any ID Card, else False")
    IDCardName: Optional[str] =Field(description = "Name of the ID Card whct kind of ID is it.")
    PersonName: Optional[str] = Field(description = "Name of the individual mention in the raw test.")
    Age: Optional[str] = Field(description = "Age of the individual mention in the raw test.")
    Address: Optional[str] = Field(description = "Address of the individual mention in the id card raw text")
    UniqueNumber: Optional[str] = Field(description = "Unique number present in the id card raw text.")




def key_extractor(raw_text, type_file):
        
    try:
        llm = llm_instance_builder()

        system =  TEMPLATE["extraction_prompt"]["system"]
        user = TEMPLATE["extraction_prompt"]["user"]
        if type_file == "Ticket":
            parser = PydanticOutputParser(pydantic_object=TravelTicket)
        elif type_file == "Invoice":
            parser = PydanticOutputParser(pydantic_object=Invoice)
        elif type_file == "ID Card":
            parser = PydanticOutputParser(pydantic_object=IdentityCard)

        prompt = PromptTemplate(
        template=system,
        input_variables=[],
        partial_variables={"format_instructions": parser.get_format_instructions()}
        )

        system_message_prompt = SystemMessagePromptTemplate(prompt=prompt)

        human_message_prompt = HumanMessagePromptTemplate.from_template(user)

        chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

        chain = LLMChain(llm=llm_instance_builder(), prompt=chat_prompt)

        output = chain.run(text=raw_text)

        result = parser.parse(output)

        result = json.loads(result.json())
        return result
    
    except BaseException as e:
        print("Error key_extractor ",str(e))

