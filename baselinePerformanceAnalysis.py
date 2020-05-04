"""
This file is for to determine accuracy of all the sentiment algorithms on the baseline data
"""
# Import libraries and files
import pandas as p
from afinn import Afinn
import sentiment_afinn as sa
import numpy as np
from sklearn.metrics import accuracy_score
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# function for Vader Sentiment Analysis
def getVaderSentiment(row):
    commentbot = SentimentIntensityAnalyzer()
    vs = commentbot.polarity_scores(row["Comments"])
    if vs["compound"] >= 0.05:
        return 1.0
    elif vs["compound"] <= -0.05:
        return -1.0
    else:
        return 0


# function to calculate sentiment score using Vader
def analyze_sentiment_vader(df):
    df["vader_score"] = df.apply(lambda row: getVaderSentiment(row), axis=1)
    df["accuracy"] = np.where(df["vader_score"] == df["overallSentiment"], "True", "False")
    print(len(df[df["accuracy"] == "True"]) / len(df.index))


# function to calculate sentiment score using Afinn
def analyze_sentiment_afinn(df):
    af = Afinn()
    df.dropna(subset=["Comments"], inplace=True)
    data_clean = df.copy()
    data_clean["Comments"] = data_clean["Comments"].str.lower().str.strip()

    data_clean["Comments"] = data_clean["Comments"].apply(sa.preprocess)

    data_clean["Comments_Clean"] = data_clean["Comments"].apply(sa.remove_stopwords)
    data_clean["Normalized_Comments"] = data_clean["Comments_Clean"].apply(sa.simple_stemmer)
    data_clean = data_clean.drop(columns=data_clean[["Comments_Clean"]], axis=1)
    data_clean = data_clean[["Comments", "Normalized_Comments", "overallSentiment"]]
    data_clean_bckup_norm = data_clean.copy()
    data_clean["afinn_score"] = [sa.afinn_sent_analysis(comm, af) for comm in data_clean["Normalized_Comments"]]
    data_clean["afinn_sent_category"] = [sa.afinn_sent_category(scr) for scr in data_clean["afinn_score"]]
    data_clean["afinn_sent_category"] = np.where(data_clean["afinn_sent_category"] == "positive", 1.0, data_clean["afinn_sent_category"])
    data_clean["afinn_sent_category"] = np.where(data_clean["afinn_sent_category"] == "negative", -1.0, data_clean["afinn_sent_category"])
    data_clean["afinn_sent_category"] = np.where(data_clean["afinn_sent_category"] == "neutral", 0.0, data_clean["afinn_sent_category"])
    data_clean["accuracy"] = np.where(data_clean["afinn_sent_category"] == data_clean["overallSentiment"], "True", "False")
    print(len(data_clean[data_clean["accuracy"] == "True"]) / len(data_clean.index))


# Calling function to get accuracy for both Vader and Afinn
def performBaselineAnalysis():
    dataframe = p.read_csv("data/labeled_comments.csv", encoding="ISO-8859-1")
    dataframe["overallSentiment"] = (dataframe["Positive"] * 1) + (dataframe["Neutral"] * 0) + (dataframe["Negative"] * -1)
    analyze_sentiment_afinn(dataframe)
    analyze_sentiment_vader(dataframe)


performBaselineAnalysis()
