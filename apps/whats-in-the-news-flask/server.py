# This is a simple placeholder of how things work with Flask

# Import needed libraries
# ***********************

from flask import Flask, request, redirect, url_for, flash, jsonify
import joblib
import sklearn
import json
# import boto3


# Required Helper Function
# ************************

from helpers import process_text, get_category_mapping, get_summary


# Create a new webapp instance
# ****************************

app = Flask(__name__)

# Preset all needed files at server start
# ***************************************

# For large files that needs to be downloaded from somewhere, download them here
pickle_file = "./models/MultinomialLogisticRegression-TFIDF5000-Best-RandomizedSearch3CV.pkl"
# pickle_file = boto3.s3().getfile(filepath)

# Then, recreate the prediction model
with open(pickle_file, 'rb') as file:
    model = joblib.load(file)

# Define routes and their handlers
# ********************************

# Handler of the root
@app.route('/')
def root_handler():
    # There is nothing here: Move along
    return {
      "code": 404,
      "message": "Not found"
    }

# Handler for prediction and summarization
@app.route('/api/predict_summarize/', methods=["POST"])
def summarize_handler():
    # Get the passed data
    data = request.get_json() # An array of strings

    # Predict our category
    predicted_num = model.predict(data)[0]

    # Generate Summary
    summary = get_summary(data[0])

    # Get our category mapping to their number from the helpers
    category = get_category_mapping(predicted_num)

    # Return the result as JSON
    return json.dumps({
      "code": 200,
      "number": str(predicted_num),
      "category": category,
      "summary": summary,
    })

# If exectuable, run the app
if __name__ == '__main__':
    app.run(
      host='127.0.0.1', 
      debug=False # Remove this for production
    )

# To run the app:
# python3 app-hello.py
