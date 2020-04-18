import string
import pandas as pd
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

def sentimentNRC(channelName):
    commentwiseDF = pd.read_json("comments/" + channelName + "_commentwise.json")

    filepath = ('data/NRC-Emotion-Lexicon-Wordlevel-v0.92.txt')
    emolex_df = pd.read_csv(filepath,
                            names=["word", "emotion", "association"],
                            sep='\t')
    emolex_words = emolex_df.pivot(index='word',
                                   columns='emotion',
                                   values='association').reset_index()
    emotions = emolex_words.columns.drop('word')
    emo_df = pd.DataFrame(0, index=commentwiseDF.index, columns=emotions)

    stemmer = SnowballStemmer("english")
    stopword = set(stopwords.words('english') + list(string.punctuation) + ['n\'t'])

    for i in commentwiseDF.index:
        document = word_tokenize(commentwiseDF.loc[i]['comment'])
        document = [word for word in document if word.isalpha() and word not in stopword]
        for word in document:
            word = stemmer.stem(word.lower())
            emo_score = emolex_words[emolex_words.word == word]
            if not emo_score.empty:
                for emotion in list(emotions):
                        emo_df.at[i, emotion] += emo_score[emotion]
    
    new_df = pd.concat([commentwiseDF, emo_df], axis=1)
    new_df['word_count'] = new_df['comment'].apply(word_tokenize).apply(len)
    for emotion in emotions:
        new_df[emotion] = new_df[emotion] / new_df['word_count']

    for i in commentwiseDF.index:
        print('Sentiment Analysis for video : ' + new_df['videoTitle'][i])
        for emotion in emotions:
            print(emotion + ' : ', (new_df[emotion][i]))
    