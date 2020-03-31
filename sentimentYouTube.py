import training_classifier as tcl
from nltk.tokenize import word_tokenize
import os.path
import pickle
from statistics import mode
from nltk.classify import ClassifierI
from nltk.metrics import BigramAssocMeasures
from nltk.collocations import BigramCollocationFinder as BCF
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import itertools


def features(words):
	temp = word_tokenize(words)

	words = [temp[0]]
	for i in range(1, len(temp)):
		if(temp[i] != temp[i-1]):
			words.append(temp[i])

	scoreF = BigramAssocMeasures.chi_sq

	# bigram count
	n = 150

	bigrams = BCF.from_words(words).nbest(scoreF, n)

	return dict([word,True] for word in itertools.chain(words, bigrams))

class VoteClassifier(ClassifierI):
	def __init__(self, *classifiers):
		self.__classifiers = classifiers

	def classify(self, comments):
		votes = []
		for c in self.__classifiers:
			v = c.classify(comments)
			votes.append(v)
		con = mode(votes)

		choice_votes = votes.count(mode(votes))
		conf = (1.0 * choice_votes) / len(votes)

		return con, conf



def sentimentNew(comments):
    commentbot = SentimentIntensityAnalyzer()
    fresult = {"positivenum": 0, "negativenum": 0, "neutralnum": 0}
    count = 0
    for comment in comments:
        vs = commentbot.polarity_scores(comment)
        count += 1
        if vs['compound'] >= 0.05:
            fresult["positivenum"] += 1
        elif vs['compound'] <= - 0.05:
            fresult["negativenum"] += 1
        else:
            fresult["neutralnum"] += 1

    print("Positive sentiment : ", fresult["positivenum"]/count * 100)
    print("Negative sentiment : ", fresult["negativenum"]/count * 100)
    print("Neutral sentiment : ", fresult["neutralnum"]/count * 100)
    return (fresult["positivenum"], fresult["negativenum"], fresult["neutralnum"])

# def sentiment(comments):
#     if not os.path.isfile('classifier.pickle'):
#         tcl.training()
#     fl = open('classifier.pickle', 'rb')
#     classifier = pickle.load(fl)
#     fl.close()

#     pos = 0
#     neg = 0
#     for words in comments:
#         comment = features(words)
#         # print(words)
#         sentiment_value, confidence = VoteClassifier(
#             classifier).classify(comment)
#         # print(sentiment_value)
#         if sentiment_value == 'positive' and confidence * 100 >= 60:
#             pos += 1
#         else:
#             neg += 1
#     psent = (pos * 100.0 / len(comments))
#     nsent = (neg * 100.0 / len(comments))
#     print("Positive sentiment : ", (pos * 100.0 / len(comments)))
#     print("Negative sentiment : ", (neg * 100.0 / len(comments)))
#     return (psent, nsent)
