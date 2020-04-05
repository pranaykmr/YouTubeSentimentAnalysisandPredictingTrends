import json


def getStatistics(youtube, vlist, channelName):
    videoIds = [x["id"]["videoId"] for x in vlist]
    if len(videoIds) <= 50:
        request = youtube.videos().list(part="statistics", maxResults=50, id=",".join(videoIds))
        response = request.execute()
        writetofile(response["items"], channelName)
    else:
        chunkedVideos = make_chunks(videoIds, 50)
        stats = []
        for vids in chunkedVideos:
            request = youtube.videos().list(part="statistics", maxResults=50, id=",".join(vids))
            response = request.execute()
            stats.extend(response["items"])
        writetofile(stats, channelName)


def make_chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i : i + n]


def writetofile(stats, channelName):
    fdata = json.dumps(stats)
    filePtr = open("comments/" + channelName + "_stats.json", "w")
    filePtr.write(fdata)
    filePtr.close()
