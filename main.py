import json
import extractComments as ec
import sentimentYouTube as syt
import fancySentiment as fs
import getVideoIds as fid

# https://console.developers.google.com/apis/api/youtube.googleapis.com/credentials?authuser=1&project=smdmyoutube-272121

with open("constants.json") as json_file:
    constants = json.load(json_file)

# no_comments = 1000
total_comments = []
total_sentiment = [(0, 0)]

fid.getIds(constants["VideoCount"])

with open("comments/vidlist.json") as json_file:
    data = json.load(json_file)
    vlist = data["items"]

for v in vlist:
    title = v["snippet"]["title"]
    print("Downloading comments of ", title)
    vid = v["id"]["videoId"]
    comments = ec.commentExtract(vid, constants["CommentCount"])
    total_comments.extend(comments)
    sent = syt.sentiment(comments)
    print(sent)
    total_sentiment.append(sent)

fs.fancySentiment(total_comments)

total_sentiment = total_sentiment[1:]

with open("comments/ts.txt", "w+") as f:
    for sentiment in total_sentiment:
        f.write(str(sentiment))
        f.write("\n")
