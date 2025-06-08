from pymongo.mongo_client import MongoClient
from flask import Flask, request, jsonify
from pymongo import MongoClient
from marshmallow import Schema, fields, ValidationError
import os
import random
from sentence_transformers import SentenceTransformer
import json 

client = MongoClient("mongodb+srv://stark-123:pwd@cluster0.qq2ou.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['PINELABS_DOC']
collection = db['documentation_context'] 
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2') 


def load_existing_filenames(path="file_hash.json"):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {} 

def save_updated_filenames(data, path="file_hash.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


try:
    client.admin.command('ping')
    print("You successfully connected to MongoDB!")
except Exception as e:
    print(e) 

class DocumentSchema(Schema):
    embedding = fields.List(fields.Float(), required=True) 
    file_path = fields.Str(required=True)                   
    chunk_seq_no = fields.Int(required=True)               
    file_concept = fields.Str(required=True) 


document_schema = DocumentSchema() 

def post_document(data):
  document_data = document_schema.load(data)
  result = collection.insert_one(document_data)
  return 

def generate_chunks(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    words = text.split()
    chunk_size = 250
    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)

    return chunks
 

def get_embedding(text):
    embeddings = model.encode(text)
    return embeddings.tolist()   

def process_files(root_folder, v3_root):
    file_hash_map = load_existing_filenames(r"C:\Users\MuraliB\Desktop\pl_online_hackathon_2025\file_hash.json")

    for dirpath, _, filenames in os.walk(root_folder):
        for fname in filenames:
            if fname in file_hash_map:
                print(f"⏭️ Skipping duplicate filename: {fname}")
                continue  # skip if already exists

            full_path = os.path.join(dirpath, fname)
            rel_path = os.path.relpath(full_path, start=v3_root)
            rel_path = rel_path.replace("\\", "/") 
            file_concept = os.path.splitext(fname)[0]  

            chunks = generate_chunks(full_path)  # get list of text chunks

            for seq_no, chunk_text in enumerate(chunks):
                embedding = get_embedding(chunk_text)  # embed actual chunk text

                document = {
                    "embedding": embedding,
                    "file_path": rel_path,
                    "chunk_seq_no": seq_no,
                    "file_concept": file_concept
                }

                try:
                    validated = document_schema.load(document)
                    collection.insert_one(validated)
                    print(f"✅ Inserted chunk {seq_no} of {fname}")
                except ValidationError as ve:
                    print(f"❌ Validation error for {fname} chunk {seq_no}: {ve}") 

            file_hash_map[fname] = 1 
    save_updated_filenames(file_hash_map, r"C:\Users\MuraliB\Desktop\pl_online_hackathon_2025\file_hash.json")

if __name__ == "__main__":
    folder_path = r"C:\Users\MuraliB\Desktop\pl_online_hackathon_2025\Integration Docs\export-project__01973fdf-b0b2-7c67-9b9a-03d534689017\v3.0\Payouts"
      # Replace with actual root folder
    v3_root = r"C:\Users\MuraliB\Desktop\pl_online_hackathon_2025\Integration Docs\export-project__01973fdf-b0b2-7c67-9b9a-03d534689017\v3.0"

    process_files(folder_path,v3_root)


