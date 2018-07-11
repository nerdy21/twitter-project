# tweet processing functions
import re
import traceback
from django.conf import settings
from . lda_functions import tokenize, get_lemma, prepare_text_for_lda, get_lda_model
from collections import defaultdict


def extract_hashtags(tweets):

    hash_tags = {}
    # loop through tweets and extract hashtags and their occurences
    for tweet in tweets:
        for entry in tweet.hashtags:
            if entry.text not in list(hash_tags):
                hash_tags[entry.text] = 1
            else:
                hash_tags[entry.text] += 1

    # sort hashtags based on occurance count
    sorted_hashtags = sorted([{"name": key, "count": value} for key, value in hash_tags.items()], key=lambda k: k['count'], reverse=True)

    return sorted_hashtags


def retrieve_tweets(user_id):

    # retrieve tweets from the user account
    try:
        statuses = settings.TWITTER_API.GetUserTimeline(screen_name=user_id, 
            count=settings.TWEET_CRAWL_COUNT, include_rts=False
        )
    except:
        traceback.print_exc()
        statuses = []

    tweets_list = [tweet.text for tweet in statuses]
    #print(tweets_list)

    return statuses


def retrieve_topis(tweets):

    # tokenize documents
    documents = []
    for tweet in tweets:
        tokens = prepare_text_for_lda(tweet.text)
        documents.append(tokens)

    # calculate token frequency
    token_frequency = defaultdict(int)
    for doc in documents:
        for token in doc:
            token_frequency[token] += 1

    # filter out tokens with token_frequency 1
    documents = [
        [token for token in doc if token_frequency[token] > 1]
            for doc in documents
    ]

    # sort words in documents
    for doc in documents:
        doc.sort()

    # create the lda model using the documents
    ldamodel = get_lda_model(documents)

    # get human readable output
    topics = ldamodel.print_topics(num_words=1)

    # extract topic names from raw data
    topic_data = {}
    for topic in topics:
        topic_name = re.search(r'"([^"]*)"', topic[1])
        if topic_name:
            if (
                topic_name.groups()[0] in topic_data and
                topic_data[topic_name.groups()[0]] > topic[1].replace('"%s"' % topic_name.groups()[0], "").replace('*', '')
                ):
                continue
            else:
                topic_data[topic_name.groups()[0]] = topic[1].replace('"%s"' % topic_name.groups()[0], "").replace('*', '')

    # sort by probability
    topic_names = [k for k in sorted(topic_data, key=topic_data.get, reverse=True)]

    return topic_names
