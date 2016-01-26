from pymongo import MongoClient
from pprint import pprint


client = MongoClient("mongodb://localhost:27017")
db = client.jstor

articleText = db.articleText

texts =  articleText.find({},{"text":1}).limit(5)

for text in texts:
    print len(text["text"])


