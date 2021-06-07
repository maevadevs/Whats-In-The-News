# Import needed libraries
import re
import numpy as np
from newspaper import Article
import requests
import json


def highlight_article_important(article_contents, important_words):
    """
    Allows to highlight the important words of an article based on a list of important words.
    """

    # important_words list to be fetched from the classifier

    # Convert important words into a numpy array
    important_words = np.array(important_words)

    # Tokenize for processing
    article_contents_tokenized = np.array(article_contents.split())
    article_contents_tokenized_lower = np.char.lower(article_contents_tokenized)
    article_contents_tokenized_lower_no_punct = np.array(list(map(lambda tk: re.sub("\W", "", tk), article_contents_tokenized_lower)))

    # Create a filter for picking the right token
    np_filter = [token in important_words for token in article_contents_tokenized_lower_no_punct]

    # Zip matching token and filter
    article_contents_zipped = zip(article_contents_tokenized, np_filter)

    # Now, filter the text that we want to mark
    final_tokens = []
    for text, status in article_contents_zipped:
        if status:
            final_tokens.append(f"<mark>{text}</mark>")
        else:
            final_tokens.append(text)

    # Finally, recombine the texts altogether
    final_str = " ".join(final_tokens)

    # And return result
    return final_str


def get_article_text_from_url(url):
    """
    Returns a tuple of:
        - message: The textual content of an article from its url or an error message
        - status: The status to distinguish wether it is an "error" or a "success"
    """

    try:
        # First, check if the url is good
        is_actual_url = bool(
            re.match(
                r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)",
                url
            )
        )

        # If it is good, parse the article and return the text
        if (is_actual_url):
            # Convert url into an Article object
            article = Article(url, memoize_articles=False)
            # Download and parse the article
            article.download()
            article.parse()
            # We are only interested at the article text
            message = article.text
            status = "success"
            # Finally, return the message and the status
            return message, status
        else:
            # Create an error message 
            message = "Sorry, this is not a valid URL. Or did you forget to include the 'http://' or 'https://' part?",
            status = "error_invalid_url"
            # Finally, return the message and the status
            return message, status
    except:
        # Create an error message 
        message = "Sorry, something went wrong."
        status = "error_internal_error"
        # Finally, return the message and the status
        return message, status


def get_prediction_and_summary(list_of_texts, api_url):
    """
    Returns the result from calling the backend predictor and summarizer as a tuple: (category, summary)
    """

    # Send the request and grab the response
    res = requests.post(
        api_url, 
        json=list_of_texts
    )

    # Parse the response JSON's text into a dictionary
    res_dict = json.loads(res.text)

    # Return the predicted category and the summary
    return (int(res_dict["number"]), res_dict["category"], res_dict["summary"])


def get_wordcloud_mapping(predicted_num):

    """
    Set of wordcloud-numbers mapping. 
    This is used to get back the actual wordcloud picture from the predicted_num.
    """

    wordcloud_mapping = [
        ('./wordcloud-images/wordcloud-arts and entertainment.png', 0),
        ('./wordcloud-images/wordcloud-automobiles.png', 1),
        ('./wordcloud-images/wordcloud-business.png', 2),
        ('./wordcloud-images/wordcloud-climate and environment.png', 3),
        ('./wordcloud-images/wordcloud-energy.png', 4),
        ('./wordcloud-images/wordcloud-finance and economics.png', 5),
        ('./wordcloud-images/wordcloud-food.png', 6),
        ('./wordcloud-images/wordcloud-global healthcare.png', 7),
        ('./wordcloud-images/wordcloud-health and wellness.png', 8),
        ('./wordcloud-images/wordcloud-legal and crimes.png', 9),
        ('./wordcloud-images/wordcloud-life.png', 10),
        ('./wordcloud-images/wordcloud-markets and investments.png', 11),
        ('./wordcloud-images/wordcloud-personal finance.png', 12),
        ('./wordcloud-images/wordcloud-politics.png', 13),
        ('./wordcloud-images/wordcloud-real estate.png', 14),
        ('./wordcloud-images/wordcloud-science and technology.png', 15),
        ('./wordcloud-images/wordcloud-sports.png', 16),
        ('./wordcloud-images/wordcloud-travel and transportation.png', 17),
        ('./wordcloud-images/wordcloud-us.png', 18),
        ('./wordcloud-images/wordcloud-wealth.png', 19),
        ('./wordcloud-images/wordcloud-world.png', 20)
    ]

    # Now, get the actual wordcloud from the mapping
    for worcloud, num in wordcloud_mapping:
        if num == predicted_num:
            return worcloud
