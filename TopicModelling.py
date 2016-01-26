from gensim import corpora, models, similarities
from unidecode import unidecode
import json
import re
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

stop_words = "a,able,about,across,after,all,almost,also,am,among,an,and,any,are,as,at,be,because,been,but,by,can,cannot,could,dear,did,do,does,either,else,ever,every,for,from,get,got,had,has,have,he,her,hers,him,his,how,however,i,if,in,into,is,it,its,just,least,let,like,likely,may,me,might,most,must,my,neither,no,nor,not,of,off,often,on,only,or,other,our,own,rather,said,say,says,she,should,since,so,some,than,that,the,their,them,then,there,these,they,this,tis,to,too,twas,us,wants,was,we,were,what,when,where,which,while,who,whom,why,will,with,would,yet,you,your"
stop_words = stop_words.split(",")


def tokenizer(text):
    word_tokens = []
    text = unidecode(text)
    text = re.sub('- ', "",text)
    words = re.findall('\d{4}|[A-Za-z]{2,}',text)
    lower_case = [w.lower() for w in words]
    for w in lower_case:
        if w not in stop_words:
            word_tokens.append(w)
    return word_tokens

dictionary = corpora.Dictionary(tokenizer(json.loads(line)["text"]) for line in open("articleTexts.json") )
dictionary.save("jstorArticles.dict")

class MyCorpus(object):
    def __iter__(self):
        for line in open("articleTexts.json"):
            yield dictionary.doc2bow(tokenizer(json.loads(line)["text"]))


corpus_memory_friendly = MyCorpus()

numTopics = 30

lda = models.ldamodel.LdaModel(corpus = corpus_memory_friendly, id2word = dictionary, num_topics = numTopics,update_every=1, chunksize=10000, passes=1)

topics = lda.print_topics(numTopics)

