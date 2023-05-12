import os
from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains.question_answering import load_qa_chain
from langchain.vectorstores import Pinecone
import pinecone

load_dotenv()

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
PINECONE_API_ENV = os.environ.get('PINECONE_API_ENV')

class Seneca:

    def __init__(self, 
                    openai_api_key = OPENAI_API_KEY,
                    pinecone_api_key = PINECONE_API_KEY,
                    pinecone_api_env = PINECONE_API_ENV,
                 ) -> None:
        self.llm = OpenAI(temperature=0, openai_api_key=openai_api_key)
        self.chain = load_qa_chain(self.llm, chain_type="stuff")
        self.embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

        pinecone.init(
            api_key=pinecone_api_key,  # find at app.pinecone.io
            environment=pinecone_api_env  # next to api key in console
        )

        self.index_name = "langchaintest"

        self.docsearch = Pinecone.from_existing_index(self.index_name, self.embeddings)

    def ask(self, question):
        docs = self.docsearch.similarity_search(question)
        return self.chain.run(input_documents=docs, question=question)