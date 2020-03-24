import json
import comment_extract as ce
import sentimentYouTube as syt
import fancySentiment as fs

no_comments = 1000
total_comments = []
total_sentiment = [(0,0)]

with open("comments/vidlist.json") as json_file:
    data = json.load(json_file)
    vlist = data['items']

for each in vlist:
    title = each['snippet']['title']
    print("Downloading comments of ", title)
    vid = each['id']['videoId']
    comments = ce.commentExtract(vid, no_comments)
    total_comments = total_comments + comments
    sent = syt.sentiment(comments)
    print(sent)
    total_sentiment.append(sent)

fs.fancySentiment(total_comments)

total_sentiment = total_sentiment[1:]

with open("comments/ts.txt", 'w+') as f:
    for each in total_sentiment:
        f.write(str(each))
        f.write("\n")
