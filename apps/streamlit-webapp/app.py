# LIBRARIES
# *********

import streamlit as st
import numpy as np
import pandas as pd



# DEFAULT UI SETTINGS
# *******************
# Note: This must be the first Streamlit command used in your app, and must only be set once

st.set_page_config(
  page_title="NACS | News Article Classifier and Summarizer",  # String or None. Strings get appended with "• Streamlit". 
	page_icon="random",  # String, anything supported by st.image, or None.
	layout="wide",  # Can be "centered" (default) or "wide". In the future also "dashboard", etc.
	initial_sidebar_state="expanded"  # Can be "auto", "expanded", "collapsed"
)



## SIDEBAR WIDGETS
## ***************

# For Section Visibilities
st.sidebar.subheader("Section Visibility")
show_help_widget = st.sidebar.checkbox("Show About and Help section", value=False)
show_text_area = st.sidebar.checkbox("Show Textbox Area", value=True)
show_full_text = st.sidebar.checkbox("Show Full Text", value=False)

# For Map Section
st.sidebar.subheader("Map Settings")
map_hour_to_filter_widget = st.sidebar.slider('Hour', 0, 23, 17)  # min: 0h, max: 23h, default: 17h



# APP TITLE
# *********

st.title("NACS | News Article Classifier and Summarizer")

if show_help_widget:
  """
  ## About and Help
  """

  expander_about = st.beta_expander("What does this app do?")
  expander_about.write("""
  This application can be used to:

  - Classify an uncategorized news article contents into one of the pre-determined category.
  - Summarize the contents of an article.
  """
  )

  expander_how = st.beta_expander("How does it works?")
  expander_how.write("""
  In order to summarize and classify an article content, we obviously need the article's content. There are 2 ways that you can provide it to the application:

  - Copy and Paste the article content into the Text Area below
  - Click on our accompagying Google Chrome Extension to automatically redirect from an article that you found online
  """
  )

  expander_geek = st.beta_expander("Tell me more about the technical stuffs!")
  expander_geek.write("""
  Oh! You like geek stuff? Cool! Me as well! 
  
  Well, as you might have noticed, this web application mostly deals with texts and their statistics. 
  
  We are using Natural Language Processings and a pre-trained Machine Learning algorithm to predict the probable category of a piece of textual content. After training multiple methods, we settled down with [Logistic Regression] as our predicting method. The features used to make the prediction is purely based on the text. We convert the text into vectors of numbers and counts of terms in the text using [TF-IDF Vectorizer]. 
  
  On the other hand, for the summarization, we are using the [T5-Model].
  """
  )

  expander_built = st.beta_expander("How was this webapp built?")
  expander_built.write("""
  The front-end of this webapp is primarly built with [Streamlit + Google Chrome Extension].

  The back-end is made with [Azure], mostly for hosting the Vectors.
  """
  )



## MAIN PAGE CONTENTS
## ******************

st.write("")
st.write("")
st.write("")

if show_text_area:
  """
  ## Paste Text Contents Here
  """
  article_contents = st.text_area("Text Contents", height=300) 


if show_full_text and article_contents:
  """
  ---
  ### Ok, here is the text we got and what we are working with
  """
  st.write(article_contents)


if article_contents:

  """## Predicted Category"""
  st.write("[Use Model to Make Prediction Here]")

  """## Short Summary"""
  st.write("[Use Model to Generate a Short Summary Here]")

