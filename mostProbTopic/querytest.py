import os

from mostProbTopic.refine import Preprocess

dir_name = os.path.dirname(os.path.abspath(__file__)) + "\\"

def QnA2(question,tl):
    from gensim import corpora, models, similarities, matutils
    from nltk.stem.snowball import SnowballStemmer
    stemmer = SnowballStemmer("english")

    qn = Preprocess(question,tl)
    from six import iteritems
    # collect statistics about all tokens
    file_name = dir_name + "Output.txt"
    dictionary = corpora.Dictionary(line.lower().split() for line in open(file_name))
    # remove stop words and words that appear only once
    file_name = dir_name + "stop.txt"
    stopwords_io_stream = open(file_name, 'r')
    stoplist = stopwords_io_stream.read().split()
    stop_ids = [dictionary.token2id[stopword] for stopword in stoplist
                if stopword in dictionary.token2id]
    # once_ids = [tokenid for tokenid, docfreq in iteritems(dictionary.dfs) if docfreq == 1]
    dictionary.filter_tokens(stop_ids)  # remove stop words and words that appear only once
    dictionary.compactify()  # remove gaps in id sequence after words that were removed
    # print(dictionary)

    # The second dictionary for the topics in Topic.txt
    file_name = dir_name + "Topic.txt"
    dictionary1 = corpora.Dictionary(line.lower().split() for line in open(file_name))
    # remove stop words and words that appear only once
    # stopwords_io_stream = open('stop.txt', 'r')
    # stoplist = stopwords_io_stream.read().split()
    stop_ids = [dictionary1.token2id[stopword] for stopword in stoplist
                if stopword in dictionary1.token2id]
    # once_ids = [tokenid for tokenid, docfreq in iteritems(dictionary.dfs) if docfreq == 1]
    dictionary1.filter_tokens(stop_ids)  # remove stop words and words that appear only once
    dictionary1.compactify()  # remove gaps in id sequence after words that were removed
    # print(dictionary1)
    dictionary.merge_with(dictionary1)
    # print(dictionary)

    class MyCorpus(object):
        def __iter__(self):
            file_name = dir_name + "Output.txt"
            for line in open(file_name):
                # assume there's one document per line, tokens separated by whitespace
                yield dictionary.doc2bow(line.lower().split())

    class TrainCorpus(object):
        def __iter__(self):
            file_name = dir_name + "Topic.txt"
            for line in open(file_name):
                # assume there's one document per line, tokens separated by whitespace
                yield dictionary.doc2bow(line.lower().split())

    corpus_memory_friendly = MyCorpus()  # doesn't load the corpus into memory!
    corpus_train = TrainCorpus()
    # print(list(corpus_memory_friendly)[0])
    # print(list(corpus_train)[0])
    file_name = dir_name + "corpus.mm"
    corpora.MmCorpus.serialize(file_name, corpus_memory_friendly)
    file_name = dir_name + "corpustrain.mm"
    corpora.MmCorpus.serialize(file_name, corpus_train)
    # corpus = TestCorpus()
    # print(corpus_memory_friendly)
    # for vector in corpus_memory_friendly:
    #     print(vector)
    # print(list(corpus_memory_friendly))
    topics = []
    file_name = dir_name + "Topic"
    topicfile = open(file_name,'r')
    for topic in topicfile:
        topics.append(topic.replace('\n',''))

    # print(topics)
    tfidf = models.TfidfModel(corpus_memory_friendly)
    corpus_tfidf = tfidf[corpus_memory_friendly]
    lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics = len(topics)) # OPTIMIZE THE NO. OF TOPICS
    lda = models.LdaModel(corpus_memory_friendly, id2word=dictionary, num_topics = int(len(topics)/1.5), passes=20, iterations = 200) # OPTIMIZE THE NO. OF TOPICS
    # Certainly not working

    # terms = matutils.Dense2Corpus(lda.state.get_lambda())
    # index1 = similarities.MatrixSimilarity(terms)
    # lda.save('ldamodel')
    # lda = models.Ldamodel.load('ldamodel')
    corpus_lsi = lsi[corpus_tfidf]
    corpus_lda = lda[corpus_memory_friendly]
    doc = "Is it dangerous to use the toothbrush?"
    doc = qn
    file_name = dir_name + "stop.txt"
    stopwords_io_stream = open(file_name, 'r')
    stopwords = stopwords_io_stream.read().split()
    tokenized = doc.lower().replace('?','').split()
    refined = [word for word in tokenized if word not in stopwords]
    refined = [stemmer.stem(word) for word in refined]
    doc = " ".join(refined)
    # print(doc)
    # vec_trans = list(terms)[dictionary.token2id[doc]]
    vec_bow = dictionary.doc2bow(doc.lower().split())
    vec_lsi = lsi[tfidf[vec_bow]] # convert the query to LSI space
    vec_lda = lda[vec_bow] # convert the query to LDA space
    file_name = dir_name + "corpustrain.mm"
    corpus = corpora.MmCorpus(file_name)
    # corpus_memory_friendly = corpora.MmCorpus('C:/Users/310286537/Documents/corpus.mm')
    # print(vec_bow)
    # print("CORPUS % s" % corpus_memory_friendly)
    # index = similarities.docsim.Similarity('C:/Users/310286537/Documents',lsi[tfidf[corpus]],num_features=len(topics)) # transform corpus to LSI space and index it
    # index1 = similarities.docsim.Similarity('C:/Users/310286537/Documents',lda[tfidf[corpus]],num_features=len(topics)) # transform corpus to LDA space and index it

    index = similarities.docsim.MatrixSimilarity(lsi[tfidf[corpus]]) # transform corpus to LSI space and index it
    index1 = similarities.docsim.MatrixSimilarity(lda[corpus]) # transform corpus to LDA space and index it
    #
    sims = index[vec_lsi] # perform a similarity query against the corpus
    sims1 = index1[vec_lda] # perform a similarity query against the corpus
    esims = list(enumerate(sims))
    ssims = sorted(esims, key=lambda item: -item[1])
    esims1 = list(enumerate(sims1))
    ssims1 = sorted(esims1, key=lambda item: -item  [1])
    # for item in ssims[:6]:
    #     print(topics[item[0]], item[1])
    # print("==================================================")
    # for item in ssims1[:6]:
    #     print(topics[item[0]], item[1])
    #
    # print("\nADDITIONAL TRAINING\n")
    file_name = dir_name + "corpustrain.mm"
    corpus = corpora.MmCorpus(file_name)
    file_name = dir_name + "corpus.mm"
    corpus_memory = corpora.MmCorpus(file_name)
    import itertools
    merged_corpus= itertools.chain(corpus_memory,corpus)
    # print(merged_corpus)

    mc=[i for i in merged_corpus]

    file_name = dir_name + "merg_corp.mm"
    corpora.MmCorpus.serialize(file_name,mc)
    corp=corpora.MmCorpus(file_name)
    # print(corp)
    tfidf1=models.TfidfModel(corp)
    corpus_tfidf1=tfidf[corp]

    # tfidf1 = models.TfidfModel(corpus)
    # corpus_tfidf1 = tfidf[corpus]
    # lsi.add_documents(tfidf1)
    # lda.add_documents(tfidf1)
    # lda.add_documents(tfidf1)
    lsi = models.LsiModel(corpus_tfidf1, id2word=dictionary, num_topics = len(topics)) # OPTIMIZE THE NO. OF TOPICS
    lda = models.LdaModel(corp, id2word=dictionary, num_topics = int(len(topics)/1.5), passes=20, iterations = 200) # OPTIMIZE THE NO. OF TOPICS

    vec_lsi = lsi[tfidf1[vec_bow]] # convert the query to LSI space
    vec_lda = lda[vec_bow] # convert the query to LDA space
    # corpus = corpora.MmCorpus('C:/Users/310286537/Documents/corpustrain.mm')
    # corpus_memory_friendly = corpora.MmCorpus('C:/Users/310286537/Documents/corpus.mm')
    # # print("CORPUS % s" % corpus_memory_friendly)
    # index = similarities.docsim.Similarity('C:/Users/310286537/Documents',lsi[tfidf1[corpus]],num_features=len(topics)) # transform corpus to LSI space and index it
    # index1 = similarities.docsim.Similarity('C:/Users/310286537/Documents',lda[tfidf1[corpus]],num_features=len(topics)) # transform corpus to LDA space and index it

    index = similarities.docsim.MatrixSimilarity(lsi[tfidf1[corpus]]) # transform corpus to LSI space and index it
    index1 = similarities.docsim.MatrixSimilarity(lda[corpus]) # transform corpus to LDA space and index it

    sims_mc = index[vec_lsi] # perform a similarity query against the corpus
    sims1_mc = index1[vec_lda] # perform a similarity query against the corpus
    esims_mc = list(enumerate(sims_mc))
    ssims_mc = sorted(esims_mc, key=lambda item: -item[1])
    esims1_mc = list(enumerate(sims1_mc))
    ssims1_mc = sorted(esims1_mc, key=lambda item: -item[1])
    # print(topics)
    # for item in ssims_mc[:6]:
    #     print(topics[item[0]], item[1])
    # print("================================================")
    # for item in ssims1_mc[:6]:
    #     print(topics[item[0]], item[1])
    # # print(sims[0])
    ultimate_sims = []
    for i in range(0,len(topics)):
        ultimate_sims.append(sims[i]*0.57+sims1[i]*0.01+sims_mc[i]*0.37+sims1_mc[i]*0.05)
    eultimate_sims = list(enumerate(ultimate_sims))
    # ultimate_sims = sorted(eultimate_sims, key=lambda item: -item[1])
    res = []
    # print(ultimate_sims)
    # print(eultimate_sims)
    for item in eultimate_sims:
        tuple = (topics[item[0]], item[1])
        res.append(tuple)
    # print("\n=================================================")
    # sims = sorted(sims, reverse = True)
    # sims1 = sorted(sims1, reverse = True)
    # sims_mc = sorted(sims_mc, reverse = True)
    # sims1_mc = sorted(sims1_mc, reverse = True)
    # print(sims[:9])
    # print(sims1[:9])
    # print(sims_mc[:9])
    # print(sims1_mc[:9])
    # print(res[:9])
    # print(res)
    return res