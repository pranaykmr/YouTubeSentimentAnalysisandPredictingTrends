import time
import sys
import json
from googleapiclient.errors import HttpError

# YOUTUBE_IN_LINK = (
#     "https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&maxResults=100&order=relevance&pageToken={pageToken}&videoId={videoId}&key={key}"
# )
# YOUTUBE_LINK = "https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&maxResults=100&order=relevance&videoId={videoId}&key={key}"

with open("auth/keys.json") as json_file:
    keys = json.load(json_file)
key = keys["APIKey"]


def commentExtract(videoId, youtube, count=-1):
    # api_service_name = "youtube"
    # api_version = "v3"
    # DEVELOPER_KEY = key

    # youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=DEVELOPER_KEY)
    # request = youtube.commentThreads().list(part="snippet", videoId=videoId, maxResults=100)

    # print("Comments downloading")
    #     page_info = requests.get(YOUTUBE_LINK.format(videoId=videoId, key=key))
    # while page_info.status_code != 200:
    #     if page_info.status_code != 429:
    #         print("Comments disabled")
    #         return []

    #     time.sleep(20)
    #     page_info = requests.get(YOUTUBE_LINK.format(videoId=videoId, key=key))

    # for i in range(len(page_info["items"])):
    #     comments.append(page_info["items"][i]["snippet"]["topLevelComment"]["snippet"]["textOriginal"])
    #     co += 1
    #     if co == count:
    #         PB.progress(co, count, cond=True)
    #         print()
    #         return comments
    page_info = makeRequest(youtube, videoId)
    comments = []
    comments = [x["snippet"]["topLevelComment"]["snippet"]["textOriginal"] for x in page_info["items"]]

    while ("nextPageToken" in page_info) and (len(comments) < count):
        temp = page_info
        page_info = getNextPage(youtube, videoId, page_info["nextPageToken"])
        commentList = [x["snippet"]["topLevelComment"]["snippet"]["textOriginal"] for x in page_info["items"]]
        comments.extend(commentList)
        # request = youtube.commentThreads().list(part="snippet", videoId=videoId, maxResults=100, pageToken=page_info["nextPageToken"])
        # page_info = requests.get(YOUTUBE_IN_LINK.format(videoId=videoId, key=key, pageToken=page_info["nextPageToken"]))

        # while page_info.status_code != 200:
        #     time.sleep(20)
        #     page_info = requests.get(YOUTUBE_IN_LINK.format(videoId=videoId, key=key, pageToken=temp["nextPageToken"]))
        # page_info = page_info.json()

        # for i in range(len(page_info["items"])):
        #     comments.append(page_info["items"][i]["snippet"]["topLevelComment"]["snippet"]["textOriginal"])
        #     co += 1
        #     if co == count:
        #         PB.progress(co, count, cond=True)
        #         print()
        #         return comments

    return comments


def makeRequest(youtube, videoId):
    try:
        request = youtube.commentThreads().list(part="snippet", videoId=videoId, maxResults=100)
        return request.execute()
    except HttpError as ex:
        time.sleep(60)
        return makeRequest(youtube, videoId)


def getNextPage(youtube, videoId, pageToken):
    try:
        request = youtube.commentThreads().list(part="snippet", videoId=videoId, maxResults=100, pageToken=pageToken)
        return request.execute()
    except HttpError as ex:
        time.sleep(60)
        return getNextPage(youtube, videoId, pageToken)
