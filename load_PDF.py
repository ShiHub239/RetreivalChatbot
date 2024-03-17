import uuid
from pinecone import Pinecone
import os
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import TokenTextSplitter

load_dotenv()

pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))

embeddings_model = OpenAIEmbeddings()

index = pc.Index("pdfs")

# path = "./data/2020.acl-main.442.pdf"
path = "./data/FHSA_Resource.pdf"

def create_embeddings(texts, metadata):
    embed_list = []
    vectors = embeddings_model.embed_documents(texts)
    for i, vector in enumerate(vectors):        
        embed_list.append({
            "id": str(uuid.uuid4()),
            "values": vector,
            "metadata": {
                            "text": texts[i],
                            "page": metadata["page"],
                            "source": metadata["source"]
                        }
        })
    return embed_list

def process_page(page):
    text_splitter = TokenTextSplitter(
        chunk_size = 150,
        chunk_overlap = 30
    )
    return text_splitter.split_text(page.page_content)

loader = PyPDFLoader(path)
pages = loader.load()

for page in pages:
    text_list = process_page(page)
    text_vectors = create_embeddings(text_list, page.metadata)
    index.upsert(
        vectors=text_vectors,
        namespace="test150"
    )
    
    print('test')






