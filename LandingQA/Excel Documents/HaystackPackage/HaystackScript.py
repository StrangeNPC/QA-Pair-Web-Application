from haystack.document_stores import InMemoryDocumentStore
from haystack.utils import fetch_archive_from_http,clean_wiki_text,convert_files_to_docs,print_answers
from haystack.pipelines import ExtractiveQAPipeline
from haystack.nodes import BM25Retriever, FARMReader
from haystack.nodes import RAGenerator, DensePassageRetriever
from haystack.pipelines.standard_pipelines import TextIndexingPipeline
from haystack import Document
import logging
import os


logging.basicConfig(format="%(levelname)s - %(name)s -  %(message)s", level=logging.WARNING)
logging.getLogger("haystack").setLevel(logging.INFO)

import pandas as pd

# Create dataframe with columns "title" and "text"
current=os.getcwd()
df = pd.read_excel(current+"\\LandingQA\\Excel Documents\\"+"PSSCOC_Cleaned.xlsx")
# Minimal cleaning
df.fillna(value="", inplace=True)

print(df.head())
df.to_excel("df.xlsx")

# Define the directory where the text files are located
#text_files_dir = os.getcwd() + "\\TextFile"

# Use data to initialize Document objects
titles = list(df["title"].values)
texts = list(df["text"].values)
documents = []
for title, text in zip(titles, texts):
    documents.append(Document(content=text, meta={"name": title or ""}))

from haystack.document_stores import FAISSDocumentStore
from haystack.nodes import RAGenerator, DensePassageRetriever


# Initialize FAISS document store.
# Set `return_embedding` to `True`, so generator doesn't have to perform re-embedding
document_store = FAISSDocumentStore(faiss_index_factory_str="Flat", return_embedding=True,sql_url="sqlite://")
#document_store = FAISSDocumentStore( sql_url="sqlite:///my_doc_store.db")

from haystack.nodes import EmbeddingRetriever

# Initialize EmbeddingRetriever Retriever to encode documents, encode question and query documents
retriever = EmbeddingRetriever(
    document_store=document_store,
    embedding_model="flax-sentence-embeddings/all_datasets_v3_mpnet-base",
    model_format="sentence_transformers"
)

from haystack.nodes import Seq2SeqGenerator

generator = Seq2SeqGenerator(model_name_or_path="vblagoje/bart_lfqa")

# Delete existing documents in documents store
document_store.delete_documents()

# Write documents to document store
document_store.write_documents(documents)

# Add documents embeddings to index
document_store.update_embeddings(retriever=retriever)

QUESTIONS = [
    "What must happen for the Employer to terminate the contract in PSSCOC?",
    "What happens when a Contractor is terminated for default in PSSCOC?",
    "What are the liquidated damages after termination in PSSCOC?",
    "Is the contractor responsible for damages caused by the subcontractor in PSSCOC?",
    "Write me a contract provision on a Cafe within an underground rail system"
]

# Or alternatively use the Pipeline class
from haystack.pipelines import GenerativeQAPipeline
from haystack.utils import print_answers

pipe = GenerativeQAPipeline(generator=generator, retriever=retriever)
for question in QUESTIONS:
    res = pipe.run(query=question, params={"Generator": {"top_k": 1}, "Retriever": {"top_k": 5}})
    print_answers(res, details="minimum")