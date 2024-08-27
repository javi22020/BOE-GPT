import chromadb

client = chromadb.HttpClient()

collection = client.get_collection("docs")
print(collection.count())