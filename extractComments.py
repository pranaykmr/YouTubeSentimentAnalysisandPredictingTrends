import time
import json
from googleapiclient.errors import HttpError


with open("auth/keys.json") as json_file:
    keys = json.load(json_file)
key = keys["APIKey"]


def commentExtract(videoId, youtube, count=-1):
    page_info = makeRequest(youtube, videoId)
    comments = []
    comments = [x["snippet"]["topLevelComment"]["snippet"]["textOriginal"] for x in page_info["items"]]

    while ("nextPageToken" in page_info) and (len(comments) < count):
        temp = page_info
        page_info = getNextPage(youtube, videoId, page_info["nextPageToken"])
        commentList = [x["snippet"]["topLevelComment"]["snippet"]["textOriginal"] for x in page_info["items"]]
        comments.extend(commentList)
    return comments


def makeRequest(youtube, videoId, retryCount=3):
    try:
        request = youtube.commentThreads().list(part="snippet", videoId=videoId, maxResults=100)
        return request.execute()
    except HttpError as ex:
        if retryCount - 1 == 0:
            return {"items": []}
        if ex.resp.status == 403:
            time.sleep(60)
        return makeRequest(youtube, videoId, retryCount - 1)


def getNextPage(youtube, videoId, pageToken, retryCount=3):
    try:
        request = youtube.commentThreads().list(part="snippet", videoId=videoId, maxResults=100, pageToken=pageToken)
        return request.execute()
    except HttpError as ex:
        if retryCount - 1 == 0:
            return {"items": []}
        if ex.resp.status == 403:
            time.sleep(60)
        return getNextPage(youtube, videoId, pageToken, retryCount - 1)
