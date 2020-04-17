# import training_classifier as tcl
# from nltk.tokenize import word_tokenize
# import os.path
# import pickle
# from statistics import mode
# from nltk.classify import ClassifierI
# from nltk.metrics import BigramAssocMeasures
# from nltk.collocations import BigramCollocationFinder as BCF
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import itertools


def sentimentNew(comments, sentimentFile):
    commentbot = SentimentIntensityAnalyzer()
    fresult = {"positivenum": 0, "negativenum": 0, "neutralnum": 0}
    count = 0
    for comment in comments:
        vs = commentbot.polarity_scores(comment)
        count += 1
        if vs["compound"] >= 0.05:
            fresult["positivenum"] += 1
        elif vs["compound"] <= -0.05:
            fresult["negativenum"] += 1
        else:
            fresult["neutralnum"] += 1
    sentimentFile.write("Positive sentiment : " + str(fresult["positivenum"] / count * 100) + "\n")
    sentimentFile.write("Negative sentiment : " + str(fresult["negativenum"] / count * 100) + "\n")
    sentimentFile.write("Neutral sentiment : " + str(fresult["neutralnum"] / count * 100) + "\n")
    print("Positive sentiment : ", fresult["positivenum"] / count * 100)
    print("Negative sentiment : ", fresult["negativenum"] / count * 100)
    print("Neutral sentiment : ", fresult["neutralnum"] / count * 100)
    return (fresult["positivenum"], fresult["negativenum"], fresult["neutralnum"])
