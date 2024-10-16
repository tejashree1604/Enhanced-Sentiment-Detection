from flask import Flask, request, render_template
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')

app = Flask(__name__)

# Initialize the sentiment analyzer and stop words
analyzer = SentimentIntensityAnalyzer()
stop_words = set(stopwords.words('english'))

def handle_negation(text):
    negations = ["not", "no", "never", "none", "neither", "nor", "n't"]
    words = text.split()
    negated_text = []
    negate = True

    for word in words:
        if word.lower() in negations:
            negate = True
        else:
            if negate:
                negated_text.append("not_" + word)
                negate = False
            else:
                negated_text.append(word)

    return " ".join(negated_text)

@app.route('/')
def my_form():
    return render_template('form.html')

@app.route('/', methods=['POST'])
def my_form_post():
    # Convert to lowercase
    text1 = request.form['text1'].lower()

    # Handle negations in the input text
    negated_text = handle_negation(text1)

    # Remove digits and stop words
    text_final = ''.join(c for c in negated_text if not c.isdigit())
    processed_doc1 = ' '.join([word for word in text_final.split() if word not in stop_words])

    # Get sentiment scores
    dd = analyzer.polarity_scores(processed_doc1)

    # Calculate compound score
    compound = round((1 + dd['compound']) / 2, 2)

    # You may interpret the final sentiment label based on the compound score
    if dd['compound'] >= 0.05:
        sentiment_label = "Positive"
    elif dd['compound'] <= -0.05:
        sentiment_label = "Negative"
    else:
        sentiment_label = "Neutral"

    return render_template(
        'form.html',
        final=sentiment_label,
        text1=text_final,
        text2=dd['pos'],
        text4=compound,
        text3=dd['neu'],
        text5=dd['neg']
    )

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5002, threaded=True)
from flask import Flask, request, render_template
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')

app = Flask(__name__)

# Initialize the sentiment analyzer and stop words
analyzer = SentimentIntensityAnalyzer()
stop_words = set(stopwords.words('english'))

def handle_negation(text):
    negations = ["not", "no", "never", "none", "neither", "nor", "n't"]
    words = text.split()
    negated_text = []
    negate = False

    for word in words:
        if word.lower() in negations:
            negate = True
        else:
            if negate:
                negated_text.append("not_" + word)
                negate = False
            else:
                negated_text.append(word)

    return " ".join(negated_text)

@app.route('/')
def my_form():
    return render_template('form.html')

@app.route('/', methods=['POST'])
def my_form_post():
    # Convert to lowercase
    text1 = request.form['text1'].lower()

    # Handle negations in the input text
    negated_text = handle_negation(text1)

    # Remove digits and stop words
    text_final = ''.join(c for c in negated_text if not c.isdigit())
    processed_doc1 = ' '.join([word for word in text_final.split() if word not in stop_words])

    # Get sentiment scores
    dd = analyzer.polarity_scores(processed_doc1)

    # Calculate compound score
    compound = round((1 + dd['compound']) / 2, 2)

    # You may interpret the final sentiment label based on the compound score
    if dd['compound'] >= 0.05:
        sentiment_label = "Positive"
    elif dd['compound'] <= -0.05:
        sentiment_label = "Negative"
    else:
        sentiment_label = "Neutral"

    return render_template(
        'form.html',
        final=sentiment_label,
        text1=text_final,
        text2=dd['pos'],
        text4=compound,
        text3=dd['neu'],
        text5=dd['neg']
    )

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5002, threaded=True)
