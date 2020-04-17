import json
import googleapiclient.errors


def getIds(youtube, maxVids):
    responseId, channelName = getChannelName(youtube)
    response = getVideos(youtube, responseId["items"][0]["id"]["channelId"], maxVids)
    videos = response["items"]
    while "nextPageToken" in response and len(videos) < maxVids:
        response = getNextPageVideos(
            youtube, responseId["items"][0]["id"]["channelId"], response["nextPageToken"], (50 if maxVids - len(videos) > 50 else maxVids - len(videos))
        )
        videos.extend(response["items"])
    fdata = json.dumps(videos)
    filePtr = open("comments/" + channelName + "_vidlist.json", "w")
    filePtr.write(fdata)
    filePtr.close()
    # print(response)
    return channelName


def getChannelName(youtube):
    channelName = input("Enter Channel Name : ")
    requestId = youtube.search().list(part="snippet", order="relevance", q=channelName, type="channel")
    responseId = requestId.execute()
    if len(responseId["items"]) == 0:
        print("Please Enter Valid Channel Display Name")
        return getChannelName(youtube)
    else:
        return responseId, channelName


def getVideos(youtube, channelId, maxVids):
    if maxVids > 50:
        maxVids = 50
    request = youtube.search().list(part="snippet", type="video", channelId=channelId, maxResults=maxVids, order="date")
    return request.execute()


def getNextPageVideos(youtube, channelId, nextPageToken, maxVids):
    request = youtube.search().list(part="snippet", type="video", channelId=channelId, maxResults=maxVids, order="date", pageToken=nextPageToken)
    return request.execute()
