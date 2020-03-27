import lxml
import requests
import time
import sys

# import progress_bar as PB
import json
import googleapiclient

# YOUTUBE_IN_LINK = (
#     "https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&maxResults=100&order=relevance&pageToken={pageToken}&videoId={videoId}&key={key}"
# )
# YOUTUBE_LINK = "https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&maxResults=100&order=relevance&videoId={videoId}&key={key}"

with open("keys.json") as json_file:
    keys = json.load(json_file)
key = keys["APIKey"]


def commentExtract(videoId, youtube, count=-1):
    # api_service_name = "youtube"
    # api_version = "v3"
    # DEVELOPER_KEY = key

    # youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=DEVELOPER_KEY)

    request = youtube.commentThreads().list(part="snippet", videoId=videoId, maxResults=100)
    page_info = request.execute()
    # print("Comments downloading")
    #     page_info = requests.get(YOUTUBE_LINK.format(videoId=videoId, key=key))
    # while page_info.status_code != 200:
    #     if page_info.status_code != 429:
    #         print("Comments disabled")
    #         return []

    #     time.sleep(20)
    #     page_info = requests.get(YOUTUBE_LINK.format(videoId=videoId, key=key))

    comments = []
    co = 0
    # for i in range(len(page_info["items"])):
    #     comments.append(page_info["items"][i]["snippet"]["topLevelComment"]["snippet"]["textOriginal"])
    #     co += 1
    #     if co == count:
    #         PB.progress(co, count, cond=True)
    #         print()
    #         return comments

    comments = [x["snippet"]["topLevelComment"]["snippet"]["textOriginal"] for x in page_info["items"]]

    # PB.progress(co, count)
    # INFINTE SCROLLING
    while ("nextPageToken" in page_info) and (len(comments) < count):
        temp = page_info
        request = youtube.commentThreads().list(part="snippet", videoId=videoId, maxResults=100, pageToken=page_info["nextPageToken"])
        page_info = request.execute()
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
        commentList = [x["snippet"]["topLevelComment"]["snippet"]["textOriginal"] for x in page_info["items"]]
        comments.extend(commentList)
        # PB.progress(co, count)
    # PB.progress(count, count, cond=True)
    print()

    return comments
