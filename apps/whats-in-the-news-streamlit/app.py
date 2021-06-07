# LIBRARIES
# *********

import streamlit as st
import os
from dotenv import load_dotenv


# CONSTANTS
# *********

# load env variales
load_dotenv() # => True if no error

# Grab our constants and secrets
SVC_ENDPOINT = os.getenv("SVC_ENDPOINT")


# HELPER FUNCTIONS
# ****************

from helpers import get_article_text_from_url, get_prediction_and_summary, get_wordcloud_mapping, highlight_article_important


# DEFAULT UI SETTINGS
# *******************
# Note: This must be the first Streamlit command used in your app, and must only be set once

st.set_page_config(
    page_title="News Article Classifier and Summarizer", # String or None. Strings get appended with "• Streamlit". 
    page_icon="icons/favicon.ico",                       # String, anything supported by st.image, or None.
    layout="wide",                                       # Can be "centered" (default) or "wide". In the future also "dashboard", etc.
    initial_sidebar_state="expanded"                     # Can be "auto", "expanded", "collapsed"
)

# Get the Query Parameters
q_params = st.experimental_get_query_params()


## SIDEBAR WIDGETS
## ***************

# --- For Input Method ---
st.sidebar.subheader("Input Method")
# This is how the user choose how to enter their text or use a URL
input_method = st.sidebar.selectbox(
    "How do you want to input your article's text?",
    ("I have a URL from a News Website", "Paste the actual text myself"),
    index=0, # Default is to paste the text
)

# --- For Section Visibilities ---
st.sidebar.subheader("Section Visibility")
# This is whether to show or collapse the Help Texts
show_help_widget = st.sidebar.checkbox(
    "Show About and Help section",
    value=False
)
# This is whether to show or collapse the preview of the text we are working with
show_full_text = st.sidebar.checkbox(
    "Show full text preview", 
    value=True
)

# --- For Resetting Fields ---
st.sidebar.subheader("Clear URL Params")
# This is for clearing the params from the URL bar
click_reset = st.sidebar.button('Clear')
if click_reset:
    # Reset Query Params
    st.experimental_set_query_params()


# APP TITLE
# *********

# Set title with a logo
col1, mid, col2 = st.beta_columns([1, 1, 20])

with col1:
    st.image('icons/icon_large.png', width=65)

with col2:
    st.title("What's In The News")

# Add a subheader
st.subheader("A News Article Classifier and Summarizer Web App")


# ABOUT AND HELP SECTION
# **********************

# This is collapsible based on widget selection
if show_help_widget:
    
    """
    ---
    ## About and Help
    """

    # Entry 1
    with st.beta_expander("What does this app do?"):
        """
        This application can be used to:

        - Classify an uncategorized news article contents into one of the pre-determined category.
        - Summarize the contents of an article.
        - Classify and Summarize an existing news article found on the web.
        """

    # Entry 2
    with st.beta_expander("How does it works?"):
        """
        In order to summarize and classify an article content, we obviously need the article's content. There are 2 ways that you can provide it to the application, based on your selection from the dropdown widget on the sidebar:
        
        - Copy and Paste an article content into the Text Area
        - Copy and Paste an existing article's URL into the Text Input
        \n
        As an alternative to Copying-And-Pasting, you could browse the web, and if you find an interesting piece of article, simply click on the Chrome Browser Extension while on that article's page.
        """

    # Entry 3
    with st.beta_expander("Tell me more about the technical stuffs!"):
        """
        Oh! You like geek stuff? Cool! Me as well! 
        
        Well, as you might have noticed, this web application mostly deals with texts and their statistics. 
        
        I am using Natural Language Processings and a pre-trained Machine Learning algorithm to predict the probable category of a piece of textual content. After training multiple methods, I settled down with [Logistic Regression] as our predicting method. The features used to make the prediction is purely based on the text. I convert the text into vectors of numbers and counts of terms in the text using [TF-IDF Vectorizer]. 
        
        On the other hand, for the summarization, I am using the [T5-Model].
        """

    # Entry 4
    with st.beta_expander("How was this webapp built?"):
        """
        The front-end of this webapp is primarly built with [Streamlit + Google Chrome Extension].

        The back-end is made with [Azure Web App], mostly for hosting the Vectors. Most of the model training were done in Jupyter, taking advantage of Cloud Computing by using Azure Machine Learning Services.
        """

    # Entry 5
    with st.beta_expander("Can I take a look at your source code?"):
        """
        Absolutely! You can find them here: [What's In The News](https://github.com/maevadevs/Whats-In-The-News)
        """
    """
    ---
    """


## MAIN PAGE CONTENTS
## ******************

# Add some spaces
st.write("")
st.write("")
st.write("")

# Check the input method selected on the widget sidebar
# -- Case 1: The user have a URL
if input_method == "I have a URL from a News Website":

    # All the URL input to be collapsible
    with st.beta_expander("", expanded=True):
        """
        ## Paste the Article's URL or Use the Chrome Extension
        """
        # If the URL params is set, use that value for article_url
        # This is redirection from the Chrome Extension
        if q_params and "url" in q_params:

            # Set value from url params on the text_input
            article_url = st.text_input(
                "Article URL",
                help="Must include the 'http://' or 'https://' part",
                value=q_params["url"][0]
            )
        
        # If no URL params, default to regular user input
        else:
            article_url = st.text_input(
                "Article URL",
                help="Must include the 'http://' or 'https://' part"
            )

        # Pass the url to get_article_text_from_url() => Either and article or
        article_text, status = get_article_text_from_url(article_url)

    # If good text was return, continue
    if status == "success":
        article_contents = article_text
        
        # Now, we can predict the category of the article
        number, pred_category, summary = get_prediction_and_summary([article_contents], SVC_ENDPOINT)

        # Present the prediction and category to the screen

        """ 
        ---
        ## Can We Predict The Category of this Content?
        """
        
        prediction_message = f"Based on our analysis of the textual contents, this is a <span style=\"font-size: 1.5em;\"><strong>{pred_category}</strong></span> article."
        st.markdown(prediction_message, unsafe_allow_html=True)

        """
        This prediction was generated by comparing with the contents of similar articles in our dataset. This category is typically made of the following terms, based on the data we have in our dataset:
        """

        st.image(get_wordcloud_mapping(number))

        # Present the short summary on the screen

        """## Can We Generate A Short Summary?"""

        """Our model generated the following summary from the text."""

        short_summary = f"<cite style=\"font-size: 1.5em; color: #888;\">{summary}</cite>"
        st.markdown(short_summary, unsafe_allow_html=True)

        # Show full text if user wants to look at it
        if show_full_text:
            """
            ---
            ### Here is the text we got and what we worked with to generate those results:
            """

            # If we get a list of important_words from the predictor
            # article_contents = highlight_article_important(article_contents, important_words)
        
            # st.write(article_contents)
            st.markdown(article_contents, unsafe_allow_html=True)

    # Handling errors
    if article_url and (
        status == "error_invalid_url"
        or status == "error_internal_error"
    ):
        # The error message will be on the article_text
        st.write(article_text)

# -- Case 2: The user have the actual text
if input_method == "Paste the actual text myself":

    # All the text input to be collapsible
    with st.beta_expander("", expanded=True):
        """
        ## Paste Text Contents Here
        """
        article_texts = st.text_area("Text Contents", height=200).strip()
        article_texts_length = len(article_texts)

    #     # Show full text if user wants to look at it
    # if show_full_text and article_texts:
    #     """
    #     ---
    #     ### Ok, here is the text we got and what we are working with
    #     """
    #     st.write(article_texts)

    # Check that the user did not just used some gibberish like "Hello world" or "test"
    if article_texts and len(article_texts) >= 250:

        # Now, we can predict the category of the article
        number, pred_category, summary = get_prediction_and_summary([article_texts], SVC_ENDPOINT)

        # Present the prediction and category to the screen

        """ 
        ---
        ## Can We Predict The Category of this Content?
        """
        
        prediction_message = f"Based on our analysis of the textual contents, this is a <span style=\"font-size: 1.5em;\"><strong>{pred_category}</strong></span> article."
        st.markdown(prediction_message, unsafe_allow_html=True)

        """
        This prediction was generated by comparing with the contents of similar articles in our dataset. This category is typically made of the following terms, based on the data we have in our dataset:
        """

        st.image(get_wordcloud_mapping(number))

        # Present the short summary on the screen

        """## Can We Generate A Short Summary?"""

        """Our model generated the following summary from the text."""

        short_summary = f"<cite style=\"font-size: 1.5em; color: #888;\">{summary}</cite>"
        st.markdown(short_summary, unsafe_allow_html=True)

    # Handle error when the user input gibberish stuff
    elif len(article_texts) >= 1 and len(article_texts) < 250:
        # Print help message
        st.write(
            f"Sorry, your text is too short. It is only {article_texts_length} character long.\nWe need at least 250 characters, roughly about 4 sentences-long in order to make something happen."
        )

    # Show full text if user wants to look at it
    if article_texts and show_full_text:
        """
        ---
        ### Here is the text we got and what we worked with to generate those results:
        """

        # If we get a list of important_words from the predictor
        # article_contents = highlight_article_important(article_contents, important_words)
    
        # st.write(article_contents)
        st.markdown(article_texts, unsafe_allow_html=True)
