import os
import json
import extractComments as ec
import sentiment_vader as sv
import visualisations as vis
import getVideoIds as fid
import googleapiclient.discovery
import google_auth_oauthlib
import getVideoStatistics as vs
import pandas as p
import sentiment_afinn as sa
import sentiment_NRC as snrc
import mapper
import predictionModels as pred

with open("constants.json") as json_file:
    constants = json.load(json_file)

with open("auth/keys.json") as json_file:
    keys = json.load(json_file)

total_comments = []
total_sentiment = [(0, 0, 0)]
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
input()
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(constants["OAuthFile"], constants["Scopes"])
    constants["OAuthFile"], constants["Scopes"])
credentials = flow.run_console()
youtube = googleapiclient.discovery.build(
youtube = googleapiclient.discovery.build(constants["ApiServiceName"], constants["ApiVersion"], developerKey=keys["APIKey"])
channelName = fid.getIds(youtube, constants["VideoCount"])

with open("comments/" + channelName + "_vidlist.json") as json_file:
    vlist = json.load(json_file)


videoIds = [x["id"]["videoId"] for x in vlist]
stats = vs.getStatistics(youtube, videoIds)


filePath = "sentimentAnalysis/" + str(channelName) + ".txt"
sentimentFile = open(filePath, "w")
commentsInfo = []
for index, v in enumerate(vlist):
    title = v["snippet"]["title"]
    sentimentFile.write("Video Number : " +
    sentimentFile.write("Video Number : " + str(index + 1) + " --> " + title + "\n")
    print("Downloading comments of Video Number : " + str(index + 1) + " --> ", title)
    print("Downloading comments of Video Number : " +
          str(index + 1) + " --> ", title)
    vid = v["id"]["videoId"]
    comments = ec.commentExtract(vid, youtube, constants["CommentCount"])
    total_comments.extend(comments)
    if len(comments) > 0:
        sent_vader = sv.analyze_sentiment(comments, sentimentFile)
        sent_afinn = sa.analyze_sentiment(comments, sentimentFile)
        sent_NRC = snrc.sentimentNRC(comments, sentimentFile)
        stats[index]["title"] = "Video Number : " + \
        stats[index]["title"] = "Video Number : " + str(index + 1) + " --> " + title + "\n"
        stats[index] = mapper.mapObject(sent_vader, sent_afinn, sent_NRC, stats[index], comments)
        stats[index] = mapper.mapObject(
            sent_vader, sent_afinn, sent_NRC, stats[index], comments)
    total_sentiment.append(sent_vader)

fdata = json.dumps(stats)
filePtr = open("comments/" + channelName + "_stats.json", "w")
filePtr.write(fdata)
filePtr.close()

"""
Data Frame Created

Data columns (total 25 columns):
 #   Column            Non-Null Count  Dtype  
---  ------            --------------  -----  
 0   kind              25 non-null     object 
 1   etag              25 non-null     object 
 2   id                25 non-null     object 
 3   title             25 non-null     object 
 4   positive_vader    25 non-null     float64
 5   negative_vader    25 non-null     float64
 6   neutral_vader     25 non-null     int64  
 7   positive_afinn    25 non-null     float64
 8   negative_afinn    25 non-null     int64  
 9   neutral_afinn     25 non-null     float64
 10  anger_NRC         25 non-null     float64
 11  anticipation_NRC  25 non-null     float64
 12  disgust_NRC       25 non-null     float64
 13  fear_NRC          25 non-null     float64
 14  joy_NRC           25 non-null     float64
 15  negative_NRC      25 non-null     float64
 16  positive_NRC      25 non-null     float64
 17  sadness_NRC       25 non-null     float64
 18  surprise_NRC      25 non-null     float64
 19  trust_NRC         25 non-null     float64
 20  viewCount         25 non-null     int64  
 21  likeCount         25 non-null     int64  
 22  dislikeCount      25 non-null     int64  
 23  commentCount      25 non-null     int64  
 24  likedislikeratio  25 non-null     float64

"""
dataframe = p.read_json("comments/" + channelName + "_stats.json")
dataframe.info()
dataframe.shape


sentimentFile.close()
print("Total Comments Scraped " + str(len(total_comments)))
# fs.fancySentiment(total_comments)

pred.performPredictions(channelName)

vis.performVisualisations(channelName, total_comments)

total_sentiment = total_sentiment[1:]

with open("comments/" + channelName + "_ts.txt", "w") as f:
    for sentiment in total_sentiment:
        f.write(str(sentiment))
        f.write("\n")
