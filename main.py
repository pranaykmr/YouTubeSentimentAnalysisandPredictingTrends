import os
import json
import extractComments as ec
import sentimentYouTube as syt
import fancySentiment as fs
import getVideoIds as fid
import googleapiclient.discovery
import google_auth_oauthlib

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

with open("comments/vidlist.json") as json_file:
    vlist = json.load(json_file)

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
    print(sent)
    total_sentiment.append(sent)

sentimentFile.close()
print("Total Comments Scraped " + str(len(total_comments)))
fs.fancySentiment(total_comments)

total_sentiment = total_sentiment[1:]

with open("comments/ts.txt", "w+") as f:
    for sentiment in total_sentiment:
        f.write(str(sentiment))
        f.write("\n")
