import re
import os
from dotenv import load_dotenv
from pypdf import PdfReader
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
import pinecone

load_dotenv()

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
PINECONE_API_ENV = os.environ.get('PINECONE_API_ENV')

loader = PyPDFLoader('docs/SenecaLettereLucilio.pdf')

data = loader.load()

print (f'You have {len(data)} document(s) in your data')
print (f'There are {len(data[30].page_content)} characters in your document')

splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size = 1000,
    chunk_overlap  = 20,
)

chunks = splitter.split_documents(data)

print (f'Now you have {len(chunks)} documents')

embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

pinecone.init(
    api_key=PINECONE_API_KEY,  # find at app.pinecone.io
    environment=PINECONE_API_ENV  # next to api key in console
)
index_name = "langchaintest"

pinecone.delete_index(index_name)

if index_name not in pinecone.list_indexes():

    pinecone.create_index(name=index_name, metric="cosine", dimension=1536)
    docsearch = Pinecone.from_texts([t.page_content for t in chunks], embeddings, index_name=index_name)

else:
    
    docsearch = Pinecone.from_existing_index(index_name, embeddings)

query = "Quali sono le caratteristiche di un buon amico?"
docs = docsearch.similarity_search(query)

print(docs)