# LIBRARIES
# *********

import streamlit as st
import numpy as np
import pandas as pd
import re



# DEFAULT UI SETTINGS
# *******************
# Note: This must be the first Streamlit command used in your app, and must only be set once

st.set_page_config(
  page_title="News Article Classifier and Summarizer",  # String or None. Strings get appended with "• Streamlit". 
	page_icon="icons/favicon.ico",  # String, anything supported by st.image, or None.
	layout="wide",  # Can be "centered" (default) or "wide". In the future also "dashboard", etc.
	initial_sidebar_state="expanded"  # Can be "auto", "expanded", "collapsed"
)

# Get the Query Parameters
q_params = st.experimental_get_query_params()



## SIDEBAR WIDGETS
## ***************

# For Input Method
st.sidebar.subheader("Input Method")
# This is how the user choose how to enter their text
input_method = st.sidebar.selectbox(
  "How do you want to input your article's text?",
  ("I have a URL from a News Website", "Paste the actual text myself"),
  index=0,
)

# For Section Visibilities
st.sidebar.subheader("Section Visibility")
# This is whether to show or collapse the Help Texts
show_help_widget = st.sidebar.checkbox("Show About and Help section", value=False)
# This is whether to show or collapse the preview of the text we are working with
show_full_text = st.sidebar.checkbox("Show full text preview", value=True)

# For Resetting Fields
st.sidebar.subheader("Clear URL Params")
click_reset = st.sidebar.button('Clear')

if click_reset:
  # Reset Query Params
  st.experimental_set_query_params()

# APP TITLE
# *********

# st.title("What's In The News")
col1, mid, col2 = st.beta_columns([1,1,20])
with col1:
    st.image('icons/icon_large.png', width=65)
with col2:
    st.title("What's In The News")
st.subheader("A News Article Classifier and Summarizer Web App")



# ABOUT AND HELP SECTION
# **********************

# This is collapsible based on widget selection
if show_help_widget:
  """
  ## About and Help
  """

  # Entry 1
  with st.beta_expander("What does this app do?"):
    st.write("""
    This application can be used to:

    - Classify an uncategorized news article contents into one of the pre-determined category.
    - Summarize the contents of an article.
    - Classify and Summarize an existing news article found on the web.
    """
    )

  # Entry 2
  with st.beta_expander("How does it works?"):
    st.write("""
    In order to summarize and classify an article content, we obviously need the article's content. There are 2 ways that you can provide it to the application, based on your selection from the dropdown widget on the sidebar:
    
    - Copy and Paste an article content into the Text Area
    - Copy and Paste an existing article's URL into the Text Input
    \n
    As an alternative to Copying-And-Pasting, you could browse the web, and if you find an interesting piece of article, simply click on the Chrome Browser Extension while on that article's page.
    """
    )

  # Entry 3
  with st.beta_expander("Tell me more about the technical stuffs!"):
    st.write("""
    Oh! You like geek stuff? Cool! Me as well! 
    
    Well, as you might have noticed, this web application mostly deals with texts and their statistics. 
    
    I am using Natural Language Processings and a pre-trained Machine Learning algorithm to predict the probable category of a piece of textual content. After training multiple methods, I settled down with [Logistic Regression] as our predicting method. The features used to make the prediction is purely based on the text. I convert the text into vectors of numbers and counts of terms in the text using [TF-IDF Vectorizer]. 
    
    On the other hand, for the summarization, I am using the [T5-Model].
    """
    )

  with st.beta_expander("How was this webapp built?"):
    st.write("""
    The front-end of this webapp is primarly built with [Streamlit + Google Chrome Extension].

    The back-end is made with [Azure Web App], mostly for hosting the Vectors. Most of the model training were done in Jupyter, taking advantage of Cloud Computing by using Azure Machine Learning Services.
    """
    )

  with st.beta_expander("Can I take a look at your source code?"):
    """
    Absolutely! You can find them here: [What's In The News](https://github.com/maevadevs/Whats-In-The-News)
    """
    


## MAIN PAGE CONTENTS
## ******************

# Add some spaces
st.write("")
st.write("")
st.write("")

# Check the input method selected on the widget sidebar
if input_method == "I have a URL from a News Website":

  # All the URL input to be collapsible
  with st.beta_expander("", expanded=True):
    """
    ## Paste the Article's URL Here
    """ 
    # If the URL params is set, use that value: This is redirection from the Chrome Extension
    if q_params and "url" in q_params:
      # Value from url params
      article_url = st.text_input(
        "Article URL", 
        help="Must include the 'http://' or 'https://' part",
        value=q_params["url"][0]
      )
    # If no URL params, default to regular user input
    else:
      article_url = st.text_input("Article URL", help="Must include the 'http://' or 'https://' part")

    # Now, make sure that we actually got a URL, not just giberish stuff
    is_actual_url = bool(re.match(r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)", article_url))

  # If URL is confirmed, continue
  if is_actual_url:
    # TODO: Fetch the content of the article from the URL to be used here instead
    article_contents = article_url # For now, just testing

    if show_full_text:
      """
      ---
      ### Ok, here is the text we got and what we are working with
      """
      st.write(article_contents)
    
    """
    ---
    ## Predicted Category
    """
    st.write("[Use Model to Make Prediction Here]")

    """## Short Summary"""
    st.write("[Use Model to Generate a Short Summary Here]")
    
  if article_url and not is_actual_url:
    st.write("Sorry, that is not a valid URL. Please try again.")


if input_method == "Paste the actual text myself":

  with st.beta_expander("", expanded=True):
    """
    ## Paste Text Contents Here
    """
    article_texts = st.text_area("Text Contents", height=200).strip()
    article_texts_length = len(article_texts)

  if show_full_text and article_texts:
    """
    ---
    ### Ok, here is the text we got and what we are working with
    """
    st.write(article_texts)

  if article_texts and len(article_texts) >= 250:
    """
    ---
    ## Predicted Category
    """
    st.write("[Use Model to Make Prediction Here]")

    """## Short Summary"""
    st.write("[Use Model to Generate a Short Summary Here]")

  elif len(article_texts) >= 1 and len(article_texts) < 250:
    st.write(f"Nope. Unable... Sorry, your text is too short. It is only {article_texts_length} character long.\nWe need at least 250 characters, roughly about 4 sentences-long in order to make something happen.")

