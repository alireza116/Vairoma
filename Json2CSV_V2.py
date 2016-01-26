__author__ = 'alire_000'

import json
import csv
import os
from unidecode import unidecode # I don't have a good grasp of decoding and encoding. I found this library to work with all the fields.
import re

def encode_dict(d): #encodes all the objects to ascii characters
 for k, v in d.iteritems():
   if isinstance(v, unicode):
     d[k] = v.encode('utf-8')
   elif isinstance(v, dict):
     d[k] = encode_dict(d[k])
 return d

def check_exist(title): # Checks to see if this part of json exists and can be called and if it is it returns the results. if not it returns "N/A"
    if title in row and len(row[title]) > 0 and isinstance(row[title],basestring) :
        return unidecode(row[title])
    elif title in row and isinstance(row[title], list):
        return unidecode(" ".join(i for i in row[title]))
    else:
        return "N/A"

def listToString(title): # This function is for the lists that we want to be concatonated into a single string.
    if title in row and isinstance(row[title], list):
        return unidecode('--'.join(i for i in row[title]))
    elif title in row and isinstance(row[title], basestring):
        return unidecode(row[title])
    else:
        return "N/A"

def data_cleanup(data): # this function is supposed to deal with the main text data...
    # text = " \n".join(i for i in data)
    # text = re.sub('[^A-Za-z0-9]+', ' ', text)
    # text = text.replace("\n", " ")
    # text = text.replace("\r", " ")
    text = ""
    for i in data:
        i = i.replace("- ", "")
        text = text + "[" + i + "]"
    text = unidecode(text)
    return text

def text_cleanup(text): # I found xml tags in reviewd-work field, this function is for that field
    soup = BeautifulSoup(text,'xml')
    result = soup.get_text()
    if len(result) > 0:
        return soup.get_text().strip()
    else:
        return "N/A"

titles = ['discipline','journaltitle','title','publication-date','authors','pageraenge','pagecount','volume','reviewd-work','doi','number','type','data','orig_data'] # header


dir_name = "C:/Users/darts2/Desktop/jstor" #where I have stored the json files
extension = ".json"


with open("data.csv", 'a') as csvFile:
    csvWriter = csv.writer(csvFile, delimiter=",")
    csvWriter.writerow(titles)

for file in os.listdir(dir_name):
    print file + " opened"
    if file.endswith(extension):
        print "this is a json file"
        data = []

        with open(file) as jsonFile:
            for line in jsonFile:
                data.append(json.loads(line))


        with open("data.csv", 'a') as csvFile:
            csvWriter = csv.writer(csvFile, delimiter=",")
            for row in data:
                row = encode_dict(row)
                # I write the csv rows here.
                rows = [listToString("discipline"),check_exist("journaltitle"),check_exist("title"),check_exist("publication-date"),listToString("authors"),check_exist("pagerange"),check_exist("pagecount"),check_exist("volume"),check_exist("reviewed-work"),check_exist("doi"),check_exist("number"),check_exist("type"),data_cleanup(row['data']['ocr']),str(row['data']['ocr'])]
                csvWriter.writerow(rows)
        print file +" done!"
    else:
        print "this is not a json file"
