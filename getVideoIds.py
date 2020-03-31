import json
import googleapiclient.errors


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
    # channelName = input("Enter Channel Name : ")
    # channelName = "Traveling Desi"
    # requestId = youtube.channels().list(part="id", forUsername=channelName, maxResults=1)
    # responseId = requestId.execute()

    # requestId = youtube.search().list(part="snippet", order="videoCount", q=channelName, type="channel")
    # responseId = requestId.execute()
    # request = youtube.search().list(part="snippet", channelId=responseId["items"][0]["id"]["channelId"], maxResults=maxVids, order="date")
    # response = request.execute()
    responseId, channelName = getChannelName(youtube)
    response = getVideos(youtube, responseId["items"][0]["id"]["channelId"], maxVids)
    videos = response["items"]
    while "nextPageToken" in response and len(videos) < maxVids:
        response = getNextPageVideos(
            youtube, responseId["items"][0]["id"]["channelId"], response["nextPageToken"], (50 if maxVids - len(videos) > 50 else maxVids - len(videos))
        )
        videos.extend(response["items"])
    fdata = json.dumps(videos)
    filePtr = open("comments/vidlist.json", "w")
    filePtr.write(fdata)
    filePtr.close()
    print(response)
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
