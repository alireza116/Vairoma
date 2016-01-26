import os
from pymongo import MongoClient
import json

client = MongoClient("mongodb://localhost:27017")
db = client.jstor

json_dir_name = "D:/Karduni/jstor/"

extension = ".json"


for file in os.listdir(json_dir_name):
    print file + " opened"
    if file.endswith(extension):
        print "this is a json file"
        with open(json_dir_name+file) as jsonFile:
            for line in jsonFile:
                article = json.loads(line)
                db.articles.insert(article)
    print "insertion Complete"
