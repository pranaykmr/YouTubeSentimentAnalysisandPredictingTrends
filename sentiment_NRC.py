import string
import numpy as np
import pandas as pd
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer


def sentimentNRC(comments, sentimentFile):
    comment = " ".join(comments)
    filepath = "data/NRC-Emotion-Lexicon-Wordlevel-v0.92.txt"
    emolex_df = pd.read_csv(filepath, names=["word", "emotion", "association"], sep="\t")
    emolex_words = emolex_df.pivot(index="word", columns="emotion", values="association").reset_index()
    emotions = emolex_words.columns.drop("word")
    emo_df = pd.DataFrame(0, index=np.arange(1), columns=emotions)

    stemmer = SnowballStemmer("english")
    stopword = set(stopwords.words("english") + list(string.punctuation) + ["n't"])

    document = word_tokenize(comment)
    document = [word for word in document if word.isalpha() and word not in stopword]
    word_count = 0
    for word in document:
        word = stemmer.stem(word.lower())
        emo_score = emolex_words[emolex_words.word == word]
        if not emo_score.empty:
            word_count += 1
            for emotion in list(emotions):
                emo_df.at[0, emotion] += emo_score[emotion]

    sentimentFile.write("Sentiment NRC" + "\n")
    print("Sentiment NRC")
    for emotion in emotions:
        emo_df[emotion] = emo_df[emotion] / word_count
        print(emotion + " : ", (emo_df[emotion][0]))
        sentimentFile.write(emotion + " : " + str((emo_df[emotion][0])) + "\n")

    return emo_df
