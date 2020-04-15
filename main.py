import os
import json
import extractComments as ec
import sentimentYouTube as syt
import fancySentiment as fs
import getVideoIds as fid
import googleapiclient.discovery
import google_auth_oauthlib
import getVideoStatistics as vs
import pandas as p

with open("constants.json") as json_file:
    constants = json.load(json_file)

with open("auth/keys.json") as json_file:
    keys = json.load(json_file)

total_comments = []
# total_sentiment = [(0, 0)]
total_sentiment = [(0, 0, 0)]
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
input()
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(constants["OAuthFile"], constants["Scopes"])
credentials = flow.run_console()
youtube = googleapiclient.discovery.build(constants["ApiServiceName"], constants["ApiVersion"], developerKey=keys["APIKey"])
channelName = fid.getIds(youtube, constants["VideoCount"])

with open("comments/" + channelName + "_vidlist.json") as json_file:
    vlist = json.load(json_file)


videoIds = [x["id"]["videoId"] for x in vlist]
stats = vs.getStatistics(youtube, videoIds)


filePath = "sentimentAnalysis/" + str(channelName) + ".txt"
sentimentFile = open(filePath, "w")
for index, v in enumerate(vlist):
    title = v["snippet"]["title"]
    sentimentFile.write("Video Number : " + str(index + 1) + " --> " + title + "\n")
    print("Downloading comments of Video Number : " + str(index + 1) + " --> ", title)
    vid = v["id"]["videoId"]
    comments = ec.commentExtract(vid, youtube, constants["CommentCount"])
    total_comments.extend(comments)
    # sent = syt.sentiment(comments)
    sent = syt.sentimentNew(comments, sentimentFile)
    positive, negative, neutral = sent
    for i in range(len(stats)):
        if stats[i]["id"] == vid:
            stats[i]["positive"] = (positive / len(comments)) * 100
            stats[i]["negative"] = (negative / len(comments)) * 100
            stats[i]["neutral"] = (neutral / len(comments)) * 100
            stats[i]["title"] = "Video Number : " + str(index + 1) + " --> " + title + "\n"
            stats[i]["viewCount"] = stats[i]["statistics"]["viewCount"]
            stats[i]["likeCount"] = stats[i]["statistics"]["likeCount"]
            stats[i]["dislikeCount"] = stats[i]["statistics"]["dislikeCount"]
            stats[i]["commentCount"] = stats[i]["statistics"]["commentCount"]
            stats[i]["likedislikeratio"] = (stats[i]["likeCount"]) / (stats[i]["dislikeCount"])
            del stats[i]["statistics"]
            break
    print(sent)
    total_sentiment.append(sent)


fdata = json.dumps(stats)
filePtr = open("comments/" + channelName + "_stats.json", "w")
filePtr.write(fdata)
filePtr.close()

"""
Data Frame Created

Data columns (total 11 columns):
 #   Column        Non-Null Count  Dtype  
---  ------        --------------  -----  
 0   kind          25 non-null     object 
 1   etag          25 non-null     object 
 2   id            25 non-null     object 
 3   positive      25 non-null     float64
 4   negative      25 non-null     float64
 5   neutral       25 non-null     float64
 6   title         25 non-null     object 
 7   viewCount     25 non-null     int64  
 8   likeCount     25 non-null     int64  
 9   dislikeCount  25 non-null     int64  
 10  commentCount  25 non-null     int64  

"""
dataframe = p.read_json("comments/" + channelName + "_stats.json")
dataframe.info()
dataframe.shape

sentimentFile.close()
print("Total Comments Scraped " + str(len(total_comments)))
fs.fancySentiment(total_comments)

total_sentiment = total_sentiment[1:]

with open("comments/" + channelName + "_ts.txt", "w") as f:
    for sentiment in total_sentiment:
        f.write(str(sentiment))
        f.write("\n")
