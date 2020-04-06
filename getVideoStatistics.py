def getStatistics(youtube, videoIds):
    if len(videoIds) <= 50:
        request = youtube.videos().list(part="statistics", maxResults=50, id=",".join(videoIds))
        response = request.execute()
        return response["items"]
    else:
        chunkedVideos = make_chunks(videoIds, 50)
        stats = []
        for vids in chunkedVideos:
            request = youtube.videos().list(part="statistics", maxResults=50, id=",".join(vids))
            response = request.execute()
            stats.extend(response["items"])
        return stats


def make_chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i : i + n]
