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


def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "0"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "OauthKeys.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)
    # channelName = input("Enter Channel Name : ")
    channelName = "TheStraightPipes"
    URL = "https://www.googleapis.com/youtube/v3/channels?key=AIzaSyB3zWY2vQ-3gaNbHiCzUTEUwafJWMi0PIE&forUsername=" + channelName + "&part=id"
    # https://www.googleapis.com/youtube/v3/channels?key=AIzaSyB3zWY2vQ-3gaNbHiCzUTEUwafJWMi0PIE&forUsername=TheStraightPipes&part=id
    r = requests.get(url=URL)

    # extracting data in json format
    data = list(r.json().items())

    request = youtube.search().list(part="snippet", channelId=data[3][1][0]["id"], maxResults=50, order="date")
    response = request.execute()
    fdata = json.dumps(response)
    f = open("comments/vidlist.json", "w+")
    f.write(fdata)
    f.close()

    print(response)


if __name__ == "__main__":
    main()
