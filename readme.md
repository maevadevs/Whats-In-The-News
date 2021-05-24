# What's In The News?

## Project Summary

How many news articles can you read in the morning? How long does it take you to read everything? Maybe you don't have much time and simply skim through the headlines? Have you ever thought *"I just wish there is something that can give me a quick summary rundown of all these articles so I can be on top of everything fast"*? Well, those are the same questions that lead me to want an application that could do just that and my drive for creating the *What's In The News* NLP project.

In the past decades, Data Science has made a leap-forward progress and has helped us to better understand the world around us using scientific knowledge and tools. When it comes to textual data, Data Science has multiple tools and methods to analyze it. Natural Language Processing (NLP) methods are what we use to analyze and process textual data from different mediums.

In this project, we analyze textual data contained within News Articles and build a Data Science application that would allow us to dissect those articles. Then, with some NLP-based Machine Learning methods, we make predictions on classifying News Articles and generate short-summaries of those articles.

My goals for this project are to:

- Build a web application that analyzes textual contents of News Articles
- Use Machine Learning to categorize the topic of a given News Article based on its contents
- Use Machine Learning to generate a short text summary of a given News Article based on its contents

## Data Questions

Here are the data questions that we are trying to answer with this project:

1. What statistical characteristics can we uncover from News Article texts?
2. Given the textual contents of a News Article, can we predict its category?
3. Given the textual contents of a News Article, can we generate a short summary?

## Datasets

### [All The News 2.1](https://components.one/datasets/all-the-news-2-news-articles-dataset/)

The primary dataset used in this project consists of news articles from the `All The News 2.1` dataset. As raw, this dataset contains 2.7 million news articles and essays from 27 distinct American publishers. However, after applying cleanups on it, I ended up with slightly lower than 2.6 million news articles from 26 distinct American publishers. The articles from this dataset mostly span from 2013 to early 2020. However, after applying the preliminaries data cleaning, we end up with a range of 2016-2020.

**Disclaimer: This project is for non-commercial and research purposes only. All rights, including copyright, in the content of the original articles are owned by the original owners. Original Data Collection by Components.**

This dataset includes the following columns:

- `date` - Date of publication of the article
- `author` - Author of the article
- `title` - Title of the article
- `article` - Textual content of the article
- `url` - URL of the article (For some)
- `section` - The section category of the news article (For some)
- `publication` - The publisher of the news article

### [BBC News Datasets](http://mlg.ucd.ie/datasets/bbc.html)

Additionally, I am using these smaller BBC datasets for discovery purposes. This set consists of two news article datasets, originating from BBC News from 2004-2005. The datasets used for this project are the raw `txt` files, not the pre-processed datasets.

**Disclaimer: This project is for non-commercial and research purposes only. All rights, including copyright, in the content of the original articles are owned by the original owners. Original Data Collection by D. Greene and P. Cunningham. Publication: D. Greene and P. Cunningham. "Practical Solutions to the Problem of Diagonal Dominance in Kernel Document Clustering", Proc. ICML 2006.**

- `BBC` Dataset: Consists of 2225 documents from the BBC news website corresponding to stories in five topical areas:
  - Business
  - Entertainment
  - Politics
  - Sport
  - Tech
- `BBC Sport` Dataset: Consists of 737 documents from the BBC Sport website corresponding to sports news articles in five topical areas
  - Athletics
  - Cricket
  - Football
  - Rugby
  - Tennis
