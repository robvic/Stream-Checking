import os
import hashlib
from elasticsearch import Elasticsearch

es = Elasticsearch('http://localhost:9200')

INDEX_NAME = "Documentos"
INPUT = "./files"

def hash_file(path):
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()
    
def indexation():
    if not es.indices.exists(INDEX_NAME):
        es.indices.create(INDEX_NAME)

    for file in os.listdir(INPUT):
        if file.endswith(".txt"):
            path = os.path.join(INPUT, file)
            with open(path, "r", encoding="utf-8") as f:
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
        print(f"{hit['_source']['file']} (Score: {hit['_score']})")