# -*- coding: utf-8 -*-

# Sample Python code for youtube.search.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os
import json
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import requests

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
# maxVids = 50


def getIds(youtube, maxVids):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    # os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    # api_service_name = "youtube"
    # api_version = "v3"
    # client_secrets_file = "OauthKeys.json"

    # Get credentials and create an API client
    # flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
    # credentials = flow.run_console()
    # youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)

    # with open("keys.json") as json_file:
    #     keys = json.load(json_file)

    # # URL = 'https://www.googleapis.com/youtube/v3/channels?key=AIzaSyB3zWY2vQ-3gaNbHiCzUTEUwafJWMi0PIE&forUsername=' + channelName + '&part=id'
    # URL = "https://www.googleapis.com/youtube/v3/channels"
    # getReqParams = {"key": keys["APIKey"], "forUsername": channelName, "part": "id", "maxResults": 1}

    # r = requests.get(url=URL, params=getReqParams)

    # # extracting data in json format
    # data = list(r.json().items())
    # channelName = input('Enter Channel Name : ')
    channelName = "Shmee150"
    requestId = youtube.channels().list(part="id", forUsername=channelName, maxResults=1)
    responseId = requestId.execute()
    request = youtube.search().list(part="snippet", channelId=responseId["items"][0]["id"], maxResults=maxVids, order="date")
    response = request.execute()
    fdata = json.dumps(response)
    filePtr = open("comments/vidlist.json", "w+")
    filePtr.write(fdata)
    filePtr.close()

    print(response)


# if __name__ == "__main__":
#     main()
