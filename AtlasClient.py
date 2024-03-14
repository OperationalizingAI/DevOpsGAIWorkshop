from pymongo import MongoClient

class AtlasClient ():

    def __init__ (self, altas_uri, dbname):
        self.mongodb_client = MongoClient(altas_uri)
        self.database = self.mongodb_client[dbname]

    def get_collection (self, collection_name):
        collection = self.database[collection_name]
        return collection

    def find (self, collection_name, filter = {}, limit=10):
        collection = self.database[collection_name]
        items = list(collection.find(filter=filter, limit=limit))
        return items

    # https://www.mongodb.com/docs/atlas/atlas-vector-search/vector-search-stage/
    def vector_search(self, collection_name, index_name, attr_name, embedding_vector, limit=5):
        collection = self.database[collection_name]
        results = collection.aggregate([
            {
                '$vectorSearch': {
                    "index": index_name,
                    "path": attr_name,
                    "queryVector": embedding_vector,
                    "numCandidates": 50,
                    "limit": limit,
                }
            },
            ## We are extracting 'vectorSearchScore' here
            ## columns with 1 are included, columns with 0 are excluded
            {
                "$project": {
                    '_id' : 1,
                    'text' : 1,
                    'source' : 1,
                    "search_score": { "$meta": "vectorSearchScore" }
            }
            }
            ])
        return list(results)

    def close_connection(self):
        self.mongodb_client.close()
