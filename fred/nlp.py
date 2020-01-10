#Ah la la, Ah la la, Gimme Three wishes, I wanna be that Dirtyfinger and his six...
from sklearn.feature_extraction.text import CountVectorizer 
from sklearn.decomposition import LatentDirichletAllocation
from textblob import TextBlob
import nltk

import numpy as np
import pandas as pd

#Each function will be applied to the columns with the Series.apply() method 

def find_polarity(input_text):
    """
    Takes one document and outputs a polarity score. -1 is Very Negative, 1 is Super Positive
    This function should be applied to a column and outputted to a new column.
    """
    return TextBlob(input_text).sentiment.polarity

def find_subjectivity(input_text):
    """
    Takes one document and outputs a subjectivity score. 0 is cold objectivity, 1 is very subjective
    This function should be applied to a column and outputted to a new column.
    """
    return TextBlob(input_text).sentiment.subjectivity

def create_sentiment_df(input_column):
    """
    Accepts a column of text data. Returns a dataframe with the original text with their polarity and 
    subjectivity scores appended to it.
    """
    cols = ['text','polarity','subjectivity']
    df = pd.DataFrame(columns=cols)
    df['text'] = input_column
    df['polarity'] = input_column.apply(find_polarity)
    df['subjectivity'] = input_column.apply(find_subjectivity)
    return df

def make_word_counts(input_column):
    """
    I should probably stop at the doc term matrix.
    """
#words that appear in less than 80% of the document and appear in at least 2 documents. Also removes the stop
#words that are in sklearns stopword list.
    count_vect = CountVectorizer(max_df=0.8, min_df=2, stop_words='english')
#The doc term matrix is a sparse matrix that has as many columns as there are words in the corpus/input_column.
#count_vect is now 'fitted' to the corpus we gave it. It has some useful methods and attributes to use later.
    doc_term_matrix = count_vect.fit_transform(input_column.values.astype('U'))
#I'm unsure about the astype('U'), but it was in the tutorial I copied this stuff from

#n_components defines how many topic/clusters will be sorted. 
    LDA = LatentDirichletAllocation(n_components=5, random_state=42)
    LDA.fit(doc_term_matrix)

#LDA, after fitting to the document term matrix, is an array of 5. Each element is a topic, with a probability of
# each word/feature/column in the doc_term_matrix    
    first_topic = LDA.components_[0]
#This is the top 5 words/features in the first topic. It returns the index, so we have to look up the actual
#word in the count_vect object
    first_topic.argsort()[-5:]
#loops through the 5 words, and passes them to the count_vect.get_feature_name method
    for i in first_topic.argsort()[-5:]: 
        print(count_vect.get_feature_names()[i])

# Loops through the 5 topics, which are the LDA.components. 
# The inner loop is is the loop above this one 
    for i, topic in enumerate(LDA.components_): 
        print(f"Top 5 words for topic #{i}:") 
        print([count_vect.get_feature_names()[i] for i in topic.argsort()[-5:]]) 
        print('\n')
        pass

def show_topic_words(input_column,n_topics=5):
    """
    Takes a column/Series as an input. Returns nothing. Prints the top 5 words for n topics.
    5 is the default n of topics
    """
    count_vect = CountVectorizer(max_df=0.8, min_df=2, stop_words='english')
    doc_term_matrix = count_vect.fit_transform(input_column.values.astype('U'))
    LDA = LatentDirichletAllocation(n_components=n_topics, random_state=42)
    LDA.fit(doc_term_matrix)
    for i, topic in enumerate(LDA.components_): 
        print(f"Top 5 words for topic #{i}:") 
        print([count_vect.get_feature_names()[i] for i in topic.argsort()[-5:]]) 
        print('\n')