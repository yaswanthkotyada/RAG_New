

import faiss
import json 
import numpy as np
from sentence_transformers import SentenceTransformer 

index=faiss.read_index("embeddings_index.faiss")

print(f"Loaded {index.ntotal} embeddings from the FAISS index.")

# model = SentenceTransformer('all-MiniLM-L6-v2')
# model = SentenceTransformer('all-mpnet-base-v2')   #better for retervial --
# model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')   #better for retervial --
model = SentenceTransformer('sentence-transformers/distiluse-base-multilingual-cased-v1')   #better for retervial --


def generate_query_embedding(query):
    # Generate an embedding for the user's query
    return np.array(model.encode([query], normalize_embeddings=True)).astype('float32')

# Example query
def retrieve_top_k_chunks(query_embedding, k):
    # Perform the similarity search in FAISS
    distances, indices = index.search(query_embedding, k)  # k is the number of results to return
    return distances, indices

# Perform similarity search to get the top 3 chunks


def combine_retrview_chunks(indices, metadata, k):
    try:
        context=""
        for i in range (k) :
            chunk_idx=indices[0][i]
            chunk_text=metadata[chunk_idx]["text"]
            context+=chunk_text+"\n\n"
        return context
    except Exception as e:
        print(f"exception:{e}")
        return e