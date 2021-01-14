# TP NLP KM
## Description
Search engine for the https://www.kaggle.com/santiagobasulto/all-hacker-news-posts-stories-askshow-hn-polls dataset
## Requirement
- Python 3
- pip

## Download the dataset
there are 2 ways to download the dataset

## Installation
- go to the project directory
```
python -m venv venv
venv\Scripts\activate
pip install -r requirement.txt
python -m spacy download en_core_web_lg
```
### Setup the API
- go to https://www.kaggle.com
- create an account
- go to https://www.kaggle.com/<username>/account
- click on "Create New API Token"
- download your kaggle.json
- move kaggle.json to ``C:\Users\<Windows-username>\.kaggle\kaggle.json`` for Windows or ``~/.kaggle/kaggle.json`` for Linux
- the dataset will be automatically downloaded when starting

### Download manually the dataset
- go to https://www.kaggle.com/santiagobasulto/all-hacker-news-posts-stories-askshow-hn-polls
- click on "Download (205MB)"
- login if needed
- extract the hn.csv of the archive on the project directory

## Run
```
python manage.py runserver
```
- wait the download of the dataset (~205MB to download)
- wait the model generation
- go to http://127.0.0.1:8000/

