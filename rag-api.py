from pymongo.mongo_client import MongoClient
from flask import Flask, request, jsonify
from pymongo import MongoClient
from marshmallow import Schema, fields, ValidationError
import os
import random
from sentence_transformers import SentenceTransformer
import json 
import openai
from openai import OpenAI
import os
import httpx
from flask_cors import CORS
import traceback
import logging
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from url_api_search import get_url_by_name,read_json_file

# Initialize logging
logging.basicConfig(level=logging.INFO) 
logger = logging.getLogger(__name__)
client = MongoClient("mongodb+srv://stark-123:pwd@cluster0.qq2ou.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['PINELABS_DOC']
collection = db['documentation_context'] 
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2') 

openai_api_key = ""
http_client = httpx.Client()
os.environ["OPENAI_API_KEY"] = openai_api_key
client = OpenAI(
    api_key=openai_api_key,
    http_client=http_client
) 

    
def get_embeddings(text):
    embeddings = model.encode(text)
    return embeddings.tolist()  

def save_embeddings_to_file(embeddings_dict, filename="endpoint_embeddings.json"):
    # Save embeddings dictionary {endpoint_name: embedding_list} to JSON file
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(embeddings_dict, f) 

def find_api_data(query):
    endpoints = [
        "Generate Token",
        "Payment Option PBP",
        "Create Order",
        "Fetch Order",
        "Create Payment Card",
        "Create Payment UPI",
        "Create Payment Netbanking",
        "Create Payment PBP",
        "Capture Payment",
        "Cancel Payment",
        "Create Refund",
        "OHS details"
    ] 

    # Load precomputed embeddings
    with open("endpoint_embeddings.json", "r") as f:
        endpoint_vecs_dict = json.load(f) 

    # Ensure all endpoints embeddings are present
    missing = [ep for ep in endpoints if ep not in endpoint_vecs_dict]
    if missing:
        raise ValueError(f"Missing embeddings for endpoints: {missing}")

    # Convert loaded embeddings (lists) to numpy arrays
    endpoint_vecs = np.array([np.array(endpoint_vecs_dict[ep]) for ep in endpoints])

    # Compute query embedding
    query_vec = np.array(get_embeddings(query)).reshape(1, -1)  # reshape for sklearn

    # Compute cosine similarity between query and all endpoint embeddings
    similarities = cosine_similarity(query_vec, endpoint_vecs)[0]

    # Get indices of top 2 matches
    top_indices = similarities.argsort()[-2:][::-1]

    # Get the top 2 endpoint names
    top_matches = [endpoints[i] for i in top_indices]

    # Read your API collection json
    collection = read_json_file(r"C:\Users\MuraliB\Desktop\pl_online_hackathon_2025\API Collection.json") 

    url_1 = get_url_by_name(collection, top_matches[0])
    url_2 = get_url_by_name(collection, top_matches[1]) 

    return [url_1, url_2] if url_1 and url_2 else []
    



def find_similar_chunks(query_text, limit=10):
    query_embedding = get_embeddings(query_text)  # returns a 384-dim list

    pipeline = [
        {
            "$vectorSearch": {
                "index": "vector_index",             # MongoDB Atlas vector index name
                "path": "embedding",                 # Field containing the embedding
                "queryVector": query_embedding,
                "exact": True,                       # Optional: True = brute force; False = approx
                "limit": limit
            }
        },
        {
            "$project": {
                "_id": 0,
                "file_concept": 1,
                "embedding": 1,
                "score": {"$meta": "vectorSearchScore"}
            }
        }
    ]

    results = list(collection.aggregate(pipeline))

    top_chunks = []
    for doc in results:
        top_chunks.append(doc['file_concept'])

    return top_chunks 


def append_file_contents(filenames, search_root):
    filenames_set = set(filenames)
    appended_text = []

    for dirpath, _, files in os.walk(search_root):
        for file in files:
            if file in filenames_set:
                file_path = os.path.join(dirpath, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        appended_text.append(f"\n---\n# {file}\n{content}")
                except Exception as e:
                    print(f"⚠ Failed to read {file_path}: {e}")

    return "\n".join(appended_text) 





def generate_response(query) -> str:
    urls = find_api_data(query)
    logger.info(f"Found URLs: {urls}")
    context_meta_data = find_similar_chunks(query) 
    formatted = []
    formatted.append("\n🧾 Extracted Documentation Content:\n")
    for name in context_meta_data:
        formatted.append(f"- {name}")  # using bullet point + inline code

    markdown_string = "\n".join(formatted)
 
    reference = markdown_string

    context_data = append_file_contents(context_meta_data, r"C:\Users\MuraliB\Desktop\pl_online_hackathon_2025\Integration Docs\export-project__01973fdf-b0b2-7c67-9b9a-03d534689017\v3.0")

    try:

        system_prompt = (
        "You are a senior technical assistant specialized in Pine Labs integration. "
        "Your role is to help developers understand and implement APIs, SDKs, and workflows "
        "using the Pine Labs documentation.\n\n"
        "You will be provided with relevant documentation context and a developer's query. "
        "Use the documentation along with your technical expertise and prior knowledge to provide "
        "a clear, accurate, and helpful response.\n\n" \
        "Keep your responses concise, focused on the query, and avoid unnecessary details. "
        "Provide output in markdown format only" 
        )

        user_prompt = (
        f"Developer Query:\n{query}\n\n"
        f"Documentation Context:\n{context_data}"
        f"Relvant API Endpoints:\n{urls}\n\n"
        )

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,
            max_tokens=4000
        )
        try:
            result = response.choices[0].message.content.strip()
            return result,reference
        except Exception as e:
            raise Exception(f"OpenAI parsing failed: {str(e)}")

    except Exception as e:
        raise Exception(f"OpenAI GPT-4o call failed: {str(e)}")



app = Flask(__name__)
CORS(app) 

@app.route('/generate-prompt', methods=['POST'])
def generate_prompt():
    try:
        data = request.get_json()

        if not data or 'query' not in data:
            return jsonify({"error": "Missing 'query' in request body"}), 400

        query = data['query']
        prompt,reference = generate_response(query) 

        return jsonify({"prompt": f"{prompt + reference}"}), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)