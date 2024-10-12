from flask import Flask, render_template, request, jsonify
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')

app = Flask(__name__)


def preprocess_text(text):
    return ' '.join([word.lower() for word in text.split() if word.lower() not in stop_words])


stop_words = stopwords.words('english')
newsgroups = fetch_20newsgroups(subset='all')
processed_data = [preprocess_text(text) for text in newsgroups.data]
vectorizer = TfidfVectorizer(max_df=0.95, max_features=1000, ngram_range=(1, 2))
tfidf_matrix = vectorizer.fit_transform(processed_data)
lsa = TruncatedSVD(n_components=50, random_state=42)
lsa_matrix = lsa.fit_transform(tfidf_matrix)

def search_engine(query):
    """
    Function to search for top 5 similar documents given a query
    """
    processed_query = preprocess_text(query)
    query_vector = vectorizer.transform([processed_query])
    query_lsa = lsa.transform(query_vector)
    similarities = cosine_similarity(query_lsa, lsa_matrix)[0]
    top_indices = similarities.argsort()[-5:][::-1]
    top_documents = np.array([newsgroups.data[i] for i in top_indices])
    top_similarities = np.array([similarities[i] for i in top_indices])
    return top_documents, top_similarities, top_indices

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    documents, similarities, indices = search_engine(query)
    return jsonify({'documents': documents.tolist(), 'similarities': similarities.tolist(), 'indices': indices.tolist()}) 


if __name__ == '__main__':
    app.run(debug=True,port=3000)
