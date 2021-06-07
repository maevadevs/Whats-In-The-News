import joblib
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import numpy as np
# For summarization
import torch
import pandas as pd
import numpy as np
from transformers import AutoTokenizer, AutoModelWithLMHead #AutoModelForCausalLM

# Pre-load these for the summarization
# Initialize pre-trained tokenizer and model
summary_tokenizer = AutoTokenizer.from_pretrained("t5-base")
summary_model = AutoModelWithLMHead.from_pretrained("t5-base", return_dict=True)

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')


def get_summary(text):
    """Summarize a piece of text using T5 Pre-trained model"""

    # Tokenize and tensorize the text
    # For tasks in T5, add the task verb. In our case: summarize
    # Max length of tokens supported by T5 is 512
    inputs = summary_tokenizer.encode(
        "summarize: ", 
        text, 
        return_tensors="pt", 
        max_length=512, 
        truncation=True
    )

    # Generate the summaries: 18 words < summary < 150 words
    outputs = summary_model.generate(
        inputs, 
        max_length=150, 
        min_length=18, 
        length_penalty=5, 
        num_beams=2
    )

    # Convert summary output tensor IDs to text
    summary = summary_tokenizer.decode(outputs[0])

    # Return the summary
    return summary


def process_text(text):

    """
    Preprocess a given text: 
        - Lowercase
        - Tokenize
        - Remove non-needed tokens
        - Lemmatize
        - Clean
    """

    # Convert to lowercase, replace newlines with spaces, strip whitespaces
    text = text.lower().strip()

    # Tokenize
    word_tokens = word_tokenize(text)
    # Convert to a numpy array
    word_tokens = np.array(word_tokens)

    # Keep only alphabetic characters
    is_alpha = list(map(str.isalpha, word_tokens))
    word_tokens = word_tokens[is_alpha]

    # Remove stopwords
    custom_stopwords = ["said", "say", "says"]
    stop_words = set(stopwords.words("english") + custom_stopwords)
    is_not_stopword = list(map(lambda token: token not in stop_words, word_tokens))
    word_tokens = word_tokens[is_not_stopword]

    # Lemmatize
    lemmatizer = WordNetLemmatizer()
    vectorize_lemmatizer = np.vectorize(lemmatizer.lemmatize)
    word_tokens = vectorize_lemmatizer(word_tokens)

    # Convert into a setence form
    sentence = " ".join(word_tokens)

    # Return final tokenized sentence
    return sentence


def get_category_mapping(predicted_num):

    """
    Set of category-numbers mapping. 
    This is used to get back the actual category from the predicted_num.
    """

    category_mapping = [
        ('Arts and Entertainment', 0),
        ('Automobiles', 1),
        ('Business', 2),
        ('Climate and Environment', 3),
        ('Energy', 4),
        ('Finance and Economics', 5),
        ('Food', 6),
        ('Global Healthcare', 7),
        ('Health and Wellness', 8),
        ('Legal and Crimes', 9),
        ('Life', 10),
        ('Markets and Investments', 11),
        ('Personal Finance', 12),
        ('Politics', 13),
        ('Real Estate', 14),
        ('Science and Technology', 15),
        ('Sports', 16),
        ('Travel and Transportation', 17),
        ('U.S.', 18),
        ('Wealth', 19),
        ('World', 20)
    ]

    # Now, get the actual category from the mapping
    for category, num in category_mapping:
        if num == predicted_num:
            return category


