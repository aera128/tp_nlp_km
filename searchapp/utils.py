import re

from nltk.corpus import stopwords


def get_wordnet_pos(tag):
    if tag.startswith('J'):
        return 'ADJ'
    elif tag.startswith('V'):
        return 'VERB'
    elif tag.startswith('N'):
        return 'NOUN'
    elif tag.startswith('R'):
        return 'ADV'
    else:
        return ''


def clean(query):
    query = re.sub('[^A-Za-z0-9 .,]+', '', query)
    query = query.lower()
    clean_query = ''
    for word in filter(None, re.split("[., ]", query)):
        if word not in stopwords.words('english'):
            clean_query += (word + ' ')
    return clean_query
