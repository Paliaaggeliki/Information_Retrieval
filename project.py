#Project 2: Building a Simple Search Engine
import os
import re
import math
from collections import defaultdict
import streamlit as st

# Set page config
st.set_page_config(
    page_title="Customized Search Engine",
    page_icon="🔍",
    layout="centered"
)

# Function to preprocess text
def preprocess_text(text):
    text = text.lower()  # Convert to lowercase
    text = re.sub(r'\W', ' ', text)  # Remove non-alphanumeric characters
    return text.split()

# Function to create inverted index
def create_inverted_index(documents):
    inverted_index = defaultdict(list)
    for doc_id, doc_content in enumerate(documents):
        terms = preprocess_text(doc_content)
        for term in terms:
            if doc_id not in inverted_index[term]:
                inverted_index[term].append(doc_id)
    return inverted_index

# Function to calculate TF-IDF score
def calculate_tfidf(query, inverted_index, documents):
    query_terms = preprocess_text(query)
    tfidf_scores = defaultdict(float)
    for term in query_terms:
        if term in inverted_index:
            df = len(inverted_index[term])  # Document frequency
            idf = math.log(len(documents) / (df + 1))  # Inverse document frequency
            for doc_id in inverted_index[term]:
                tf = documents[doc_id].count(term) / len(documents[doc_id])  # Term frequency
                tfidf_scores[doc_id] += tf * idf
    return tfidf_scores

# Function to rank documents
def rank_documents(query, inverted_index, documents):
    tfidf_scores = calculate_tfidf(query, inverted_index, documents)
    ranked_docs = sorted(tfidf_scores.items(), key=lambda x: x[1], reverse=True)
    return ranked_docs

# Sidebar
st.sidebar.title("Search Engine")
query = st.sidebar.text_input('Enter your query')

# Load documents
documents_dir = '.'  # Assuming all text files are in the same directory as the script
documents = []
document_files = ['black_hole.txt', 'Cinderella.txt', 'Rapunzel.txt', 'The Frog King.txt', 'The Owl.txt', 
                  'Iron John.txt', 'Lazy Harry.txt', 'The Moon.txt']
for filename in document_files:
    with open(filename, 'r') as file:
        documents.append(file.read())

# Create inverted index
inverted_index = create_inverted_index(documents)

# Search and display results
if st.sidebar.button('Search'):
    ranked_docs = rank_documents(query, inverted_index, documents)
    st.subheader("Search Results")
    for doc_id, score in ranked_docs:
        st.write(f'Document: {document_files[doc_id]}, Score: {score}')

