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

client = MongoClient("mongodb+srv://stark-123:stark-123@cluster0.qq2ou.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
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
                    print(f"⚠️ Failed to read {file_path}: {e}")

    return "\n".join(appended_text) 


def generate_response(query) -> str:
    context_meta_data = find_similar_chunks(query) 
    # context_meta_data is a list of fielnames each file is a documentation for developers. now i need to append it in response please refer here for additional details  
    for name in context_meta_data:
        formatted.append(f"• {name}")

    formatted.append("\n🧾 Extracted Documentation Content:\n")
    formatted.append(raw_text)

    return "\n".join(formatted)
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
        )

        user_prompt = (
        f"Developer Query:\n{query}\n\n"
        f"Documentation Context:\n{context_data}"
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
            return result
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
        prompt = generate_response(query) 

        return jsonify({"prompt": prompt}), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
    

if __name__ == '__main__':
    app.run(debug=True, port=5000)
