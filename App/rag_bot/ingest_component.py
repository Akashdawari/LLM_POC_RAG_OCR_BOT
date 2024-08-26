from langchain_community.document_loaders import Docx2txtLoader, PyPDFLoader, TextLoader, UnstructuredPowerPointLoader, CSVLoader
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain_text_splitters import CharacterTextSplitter
from langchain_core.pydantic_v1 import BaseModel
from typing import Optional
import pandas as pd
import os


class Document(BaseModel):

    page_content: str
    page_number: Optional[str]


def ingest_documents(file_path, file_extension):
    try: 
        documents = []
        print(file_path, file_extension)
        if file_extension.lower() == '.pdf':
            loader = PyPDFLoader(file_path)
            documents.extend(loader.load_and_split())
        elif file_extension.lower() in ['.docx', '.doc']:
            loader = Docx2txtLoader(file_path)
            documents.extend(loader.load())
        elif file_extension.lower() == '.txt':
            loader = TextLoader(file_path)
            documents.extend(loader.load()) 
        elif file_extension.lower() in ['.xlsx', '.xls']:
            try:
                excel_file = pd.ExcelFile(file_path)
                for sheet_name in excel_file.sheet_names:
                    try: 
                        # Read each sheet into a DataFrame
                        df = pd.read_excel(excel_file, sheet_name)

                        # Convert DataFrame to CSV and save it
                        csv_filename = f"{sheet_name}.csv"
                        df.to_csv(csv_filename, index=False, encoding='utf-8')

                        # Now, you can use your loader to load the CSV file
                        loader = CSVLoader(file_path=csv_filename, encoding='utf8')
                        documents.extend(loader.load())
                        os.remove(csv_filename)
                        print("Success Sheet Name ==> ",sheet_name)
                    except Exception as e:
                        print("Error Sheet Name ==> ",sheet_name, str(e))
                excel_file.close()
            except Exception as e:
                print("ERROR", str(e))
                return False
        elif file_extension.lower() == '.csv':
            loader = CSVLoader(file_path=file_path)
            documents.extend(loader.load())
        elif file_extension.lower() == '.pptx':
            loader = UnstructuredPowerPointLoader(file_path)
            documents.extend(loader.load())
        if len(documents):
            # split it into chunks
            text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
            docs = text_splitter.split_documents(documents)
            return True, docs
        else:
            print("empty documents")
        return False, []
    except Exception as e:
        print(str(e))
        return False, []


def get_related_documents(question, all_docs):
    embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

    # load it into Chroma
    db = Chroma.from_documents(all_docs, embedding_function)

    docs = db.similarity_search_with_score(question, k=4)

    if len(docs)>0:
        relevant_docs = []
        for kk in docs:
            doc, score = kk
            if score < 1:
                temp = Document(page_content=doc.page_content,
                        page_number=doc.metadata.get("page", None))
                relevant_docs.append(temp)
        return relevant_docs
    return []