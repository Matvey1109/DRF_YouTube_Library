from rest_framework.decorators import api_view
from rest_framework.response import Response
from pytube import YouTube


@api_view(["GET"])
def download(request, url):
    try:
        url = "https://www.youtube.com/watch?v=" + url
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        stream.download()
        return Response({"msg": "Video downloaded successfully!"})
    except Exception as e:
        return Response({"error": str(e)})


# url = "9bZkp7q19f0"
# url = "https://www.youtube.com/watch?v=" + url
# yt = YouTube(url)
# print(yt.title)
