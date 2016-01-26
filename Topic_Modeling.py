__author__ = 'darts2'
#for this model to work, you need nltk, gensim . pip install should work for both. easily. look up how to install each. let me know if you had a problem.


from gensim import corpora, models, similarities
from nltk.stem import WordNetLemmatizer
import re
import csv

stop_words = []
documents = []
texts = []

#This parts reads the stop words and puts them into a list.
with open("stop-word-list.csv", "r") as stopwords:
    text = stopwords.read()
    list = re.findall('[A-Za-z]+', text)
    stop_words = list
print stop_words
#This function tokenizes the documents
def tokens(text):
    word_tokens = []
    lemmetized = []
    words = re.findall('[A-Za-z]{2,}',text)
    lower_case = [w.lower() for w in words]
    wnl = WordNetLemmatizer()
    for w in lower_case:
        lemmetized.append(wnl.lemmatize(w))
    for w in lemmetized:
        if w not in stop_words:
            word_tokens.append(w)
    return word_tokens

#if you want to add other stop words to the stop words list add them to this list. example: ["data","visualization","visual","paper","challenge","analysis", "analytics"]
#if you see any wierd word that you don't want in the results, put it in this list.
other_stop_words = []

if len(other_stop_words) > 0:
    for word in other_stop_words:
        stop_words.append(word)

#put the path to your file here, it SHOULD have a column "Abstract" where the abstracts are located.

path = "Articles_Vast.csv"

with open(path, "r") as infile:
    csvReader = csv.DictReader(infile)
    for line in csvReader:
        documents.append(line['Abstract'])

#this part creates a tokens list for each document,
for document in documents:
    texts.append(tokens(document))

dictionary = corpora.Dictionary(texts)

corpus = [dictionary.doc2bow(text) for text in texts]

# this is the topic modeling part! change the number of topics to see which you like. also, number of passes.
numTopics = 30
lda = models.ldamodel.LdaModel(corpus = corpus, id2word = dictionary, num_topics = numTopics,update_every=1, chunksize=50, passes=20)

# you can print the list of topics here. num_topics should match num_topics from the previous step.
topics = lda.show_topics(num_topics=numTopics,formatted=False)
topicsResults = {}
print "TOPICS : "
for topic in  topics:
    print "Topic id: " + str(topic[0]) + " words: " +  ", ".join(word[0] for word in topic[1])
    topicsResults.update({topic[0]:" ".join([word[0] for word in topic[1]])})

print "\n--------------------------\n"

# From here on is Data output

doc_lda = lda[corpus]

top2Topics = [] # this list contains the ID for top 2 topics for each document . this is ordered based on the main document excel file.
sorted_topics = []

for document in doc_lda:
    #list of top topics for each document descending sorted.
    top_topics = sorted(document,key=lambda x: x[1],reverse=True)
    sorted_topics.append(top_topics)
    if len(top_topics) >= 2:
        top2Topics.append([top_topics[0][0],top_topics[1][0]])
    else:
        top2Topics.append([top_topics[0][0]])

for document in sorted_topics:
    print document
#this part returns a CSV file with top 2 topics for each document. Simply copy and paste the content to your Excel file.
#
i = 0
with open("DocumentTopics.csv","w") as outFile:
    csvWriter = csv.writer(outFile, lineterminator='\n')
    csvWriter.writerow(["topicID 1","topicID 2", "topicWords 1", "topicWords 2"])
    for document in doc_lda:
        documentTopics = top2Topics[i]
        if len(documentTopics) == 2:
            topicWords1 = topicsResults[documentTopics[0]]
            topicWords2 = topicsResults[documentTopics[1]]
            csvWriter.writerow([documentTopics[0],documentTopics[1],topicWords1,topicWords2])
        else:
            topicWords1 = topicsResults[documentTopics[0]]
            csvWriter.writerow([documentTopics[0],"N/A",topicWords1,"N/A"])
        i = i + 1
print i





