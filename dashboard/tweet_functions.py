# tweet processing functions

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