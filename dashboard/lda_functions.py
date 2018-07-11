import spacy
from spacy.lang.en import English
import nltk
from nltk.corpus import wordnet as wn
import random
import pickle
import gensim
from gensim import corpora
from django.conf import settings

#nlp = spacy.load('en_core_web_sm')
spacy.load('en')

parser = English()

nltk.download('wordnet')
nltk.download('stopwords')

NUM_TOPICS = 10
en_stop = set(nltk.corpus.stopwords.words('english'))

def tokenize(text):

    # parse text and extract tokens

    lda_tokens = []
    tokens = parser(text)
    for token in tokens:
        # omit spaces
        if token.orth_.isspace():
            continue
        # omit urls
        elif token.like_url:
            continue
        else:
            lda_tokens.append(token.lower_)
    return lda_tokens


def get_lemma(word):

    # get right word using morphy function from wordnet
    lemma = wn.morphy(word)
    if lemma is None:
        return word
    else:
        return lemma


def prepare_text_for_lda(text):
    tokens = tokenize(text)

    # extract words with more than 4 characters
    tokens = [token for token in tokens if len(token) > 4]

    # extract words other than stop words
    tokens = [token for token in tokens if token not in en_stop]

    tokens = [get_lemma(token) for token in tokens]

    return tokens


# re-trainable model
# def get_lda_model(text_data):

#     # load existing dictionary if present
#     try:
#         dictionary = gensim.corpora.Dictionary.load('dictionary.gensim')
#     except:
#         # initialize a Dictionary with input data
#         dictionary = corpora.Dictionary(text_data)

#     # save dictionary for future use
#     dictionary.save('dictionary.gensim')

#     try:
#         corpus = pickle.load(open('corpus.pkl', 'rb'))

#     except:
#         # create a bag of words from the dictionary and source data
#         corpus = [dictionary.doc2bow(text) for text in text_data]

#     # save corpus for future use
#     pickle.dump(corpus, open('corpus.pkl', 'wb'))

#     try:
#         ldamodel = gensim.models.ldamodel.LdaModel.load('model%s.gensim' % settings.NUM_TOPICS)
#     except:
#         # train the model with the corpus
#         ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = settings.NUM_TOPICS, id2word=dictionary, passes=15)

#     # save model for future usage
#     ldamodel.save('model%s.gensim' % settings.NUM_TOPICS)

#     return ldamodel


def get_lda_model(text_data):
    
    # initialize a Dictionary with input data
    dictionary = corpora.Dictionary(text_data)

    # create a bag of words from the dictionary and source data
    corpus = [dictionary.doc2bow(text) for text in text_data]

    # train the model with the corpus
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = settings.NUM_TOPICS, id2word=dictionary)

    return ldamodel