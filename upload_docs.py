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

embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)



pinecone.init(
        api_key=PINECONE_API_KEY,  # find at app.pinecone.io
        environment=PINECONE_API_ENV  # next to api key in console
    )
index_name = "langchaintest"

splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap  = 20,
)

print(OPENAI_API_KEY)
print(PINECONE_API_KEY)
print(PINECONE_API_ENV)

def load_pdf(path):

    loader = PyPDFLoader(path)

    data = loader.load()

    print (f'You have {len(data)} document(s) in your data')
    print (f'There are {len(data[0].page_content)} characters in your document')

    chunks = splitter.split_documents(data)

    print (f'Now you have {len(chunks)} documents')

    if index_name not in pinecone.list_indexes():

        pinecone.create_index(name=index_name, metric="cosine", dimension=1536)
        index = pinecone.Index(index_name=index_name)  
        vectorstore = Pinecone(index, embeddings.embed_query, "text")
        vectorstore.from_texts([t.page_content for t in chunks], embeddings, index_name=index_name)

    else:

        index = pinecone.Index(index_name=index_name)  
        vectorstore = Pinecone(index, embeddings.embed_query, "text")
        vectorstore.add_texts([t.page_content for t in chunks])


if __name__ == "__main__":

    for file in os.listdir('docs'):

        if file.endswith('.pdf'):

            load_pdf(f'docs/{file}')
