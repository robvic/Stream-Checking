import os
import json
from datetime import datetime as dt
import hashlib
from elasticsearch import Elasticsearch

es = Elasticsearch('http://localhost:9200')

INDEX_NAME = "documentos"
CORRECTED_PATH = "./files/corrected_transcriptions"
MATCH_PATH = "./files/matches"

def hash_file(path):
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()
    
def indexation():
    if not es.indices.exists(index=INDEX_NAME):
        es.indices.create(index=INDEX_NAME)

    for file in os.listdir(CORRECTED_PATH):
        if file.endswith(".txt"):
            path = os.path.join(CORRECTED_PATH, file)
            with open(path, "r", encoding="windows-1252") as f:
                content = f.read()

            doc = {
                "file_name" : file,
                "content" : content
            }

            id = hash_file(path)

            es.index(index=INDEX_NAME, id=id, body=doc)
    print("Done.")

def find_terms(term):
    query = {
        "query" : {
            "match" : {
                "content" : term
            }
        }
    }

    results = es.search(index=INDEX_NAME, body=query)
    hits = results["hits"]["hits"]

    for hit in hits:
        timestamp = dt.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_file = os.path.join(MATCH_PATH, f"match_{term}_{timestamp}.json") 
        data = {
            "term" : term,
            "file" : hit['_source']['file_name'],
            "content" : hit['_source']['content'],
            "score" : hit['_score']
        }
        with open(output_file, 'w+') as f:
            json.dump(data, f, indent=4)

if __name__ == "__main__":
    #indexation()
    term = "Listerine"
    find_terms(term)