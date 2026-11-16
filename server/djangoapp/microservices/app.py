from flask import Flask, jsonify
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

app = Flask(__name__)
sia = SentimentIntensityAnalyzer()


@app.get('/')
def home():
    return jsonify(status='ok', service='VADER sentiment analyzer')


@app.get('/analyze/<path:input_txt>')
def analyze_sentiment(input_txt):
    scores = sia.polarity_scores(input_txt)
    score = scores['compound']
    sentiment = 'positive' if score >= 0.05 else 'negative' if score <= -0.05 else 'neutral'
    return jsonify(sentiment=sentiment, scores=scores)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)
