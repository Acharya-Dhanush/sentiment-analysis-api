from flask import Flask, request, jsonify
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer

# Initialize Flask app
app = Flask(__name__)

# Load the trained model and vectorizer
with open("sentiment_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)

with open("tfidf_vectorizer.pkl", "rb") as vectorizer_file:
    vectorizer = pickle.load(vectorizer_file)

@app.route("/")
def home():
    return "Sentiment Analysis API is Running!"

# Define the prediction endpoint
@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get JSON input
        data = request.get_json()
        review_text = data["review_text"]

        # Transform the text using TF-IDF vectorizer
        review_vectorized = vectorizer.transform([review_text])

        # Predict sentiment
        prediction = model.predict(review_vectorized)[0]
        sentiment = "positive" if prediction == 1 else "negative"

        # Return JSON response
        return jsonify({"review_text": review_text, "sentiment_prediction": sentiment})

    except Exception as e:
        return jsonify({"error": str(e)})

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
