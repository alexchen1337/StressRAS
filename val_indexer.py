from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import pandas as pd
import os

# Elasticsearch setup
es = Elasticsearch("http://localhost:9200")
INDEX_NAME = "valorant_matches"

def create_index():
    settings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        "mappings": {
            "properties": {
                "match_id": {"type": "keyword"},
                "map": {"type": "keyword"},
                "team1": {"type": "keyword"},
                "team2": {"type": "keyword"},
                "winner": {"type": "keyword"},
                "score_team1": {"type": "integer"},
                "score_team2": {"type": "integer"},
                "date": {"type": "date"},
                "event": {"type": "keyword"},
                "stage": {"type": "keyword"},
                # Add text fields with better search capabilities
                "team1_players": {"type": "text", "analyzer": "standard"},
                "team2_players": {"type": "text", "analyzer": "standard"}
            }
        }
    }
    
    if es.indices.exists(index=INDEX_NAME):
        es.indices.delete(index=INDEX_NAME)
    es.indices.create(index=INDEX_NAME, body=settings)
    print(f"Created index: {INDEX_NAME}")

def generate_documents(df):
    for _, row in df.iterrows():
        doc = row.to_dict()
        yield {
            "_index": INDEX_NAME,
            "_source": doc
        }

def index_data():
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    
    # Read all CSV files in the data directory
    for file in os.listdir(data_dir):
        if file.endswith('.csv'):
            file_path = os.path.join(data_dir, file)
            print(f"Indexing {file}...")
            
            df = pd.read_csv(file_path)
            create_index()
            success, _ = bulk(es, generate_documents(df))
            print(f"Successfully indexed {success} documents")

if __name__ == "__main__":
    index_data()