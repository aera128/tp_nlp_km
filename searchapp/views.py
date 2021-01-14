import html
import os
import pickle

import pandas as pd
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from kaggle.api.kaggle_api_extended import KaggleApi
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from searchapp.models import SynonymGetter
from searchapp.utils import clean

print("Initializing variables...")
if not os.path.exists('hn.csv'):
    print("Downloading dataset please wait...")
    api = KaggleApi()
    api.authenticate()
    api.dataset_download_files('santiagobasulto/all-hacker-news-posts-stories-askshow-hn-polls', path='.',
                               unzip=True)
    print("Dataset downloaded")
df = pd.read_csv('hn.csv')
if os.path.exists('model.pickle'):
    print("Loading Model...")
    with open('model.pickle', 'rb') as f:
        out = pickle.load(f)
    X = out[0]
    vectorizer = out[1]
else:
    print("Generating Model...")
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(df['Title'].values.astype('U'))
    saveObject = (X, vectorizer)
    with open("model.pickle", "wb") as f:
        pickle.dump(saveObject, f)
syns = SynonymGetter()
print("Variables loaded")


def index(request):
    return render(request, 'searchapp/index.html', {})


@csrf_exempt
def search(request):
    if request.method == 'POST' and request.is_ajax():
        query = clean(html.escape(request.POST['query']))
        print("Query : ", query)
        page = html.escape(request.POST['page'])
        query_vec = vectorizer.transform([query])
        results = cosine_similarity(X, query_vec).reshape((-1,))
        json_result = list()
        results = results.argsort()[:][::-1]
        index = 0 + (50 * int(page))

        for i in results[0 + (50 * int(page)):50 + (50 * int(page))]:
            json_result.append({
                "id": int(df.iloc[i, 0]),
                "title": str(df.iloc[i, 1]),
                "type": str(df.iloc[i, 2]),
                "author": str(df.iloc[i, 3]),
                "created_at": str(df.iloc[i, 4]),
                "url": str(df.iloc[i, 5]),
                "num_points": int(df.iloc[i, 6]),
                "num_comments": int(df.iloc[i, 7]),
                "index": index,
            })
            index += 1

        synonyms = syns.search_syns(query)
        synonyms = list(dict.fromkeys(synonyms))
        return JsonResponse({
            "status": 200,
            "results": json_result,
            "count": len(results),
            "page": int(page),
            "synonyms": synonyms[:10]
        })
    else:
        return JsonResponse({
            "status": 405,
            "content": "Method Not Allowed"
        })
