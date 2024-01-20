from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics, serializers, status
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import User
from .models import Video
from .serializers import UserSerializer, VideoSerializer
from pytube import YouTube


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class VideoList(generics.ListCreateAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

    def perform_create(self, serializer):
        part_of_url = self.request.GET.get("part_of_url")

        if not part_of_url:
            raise serializers.ValidationError("part_of_url is required.")

        url = "https://www.youtube.com/watch?v=" + part_of_url

        try:
            yt = YouTube(url)
            video_data = {
                "title": yt.title,
                "author": yt.author,
                "thumbnail_url": yt.thumbnail_url,
                "number_of_views": yt.views,
                "user": self.request.user,
            }

            serializer.validated_data.update(video_data)
            serializer.save()
        except Exception as e:
            raise serializers.ValidationError(str(e))

    def create(self, request, *args, **kwargs):
        # Allow only POST requests with 'part_of_url' in the query parameters
        if request.method == "POST" and not request.GET.get("part_of_url"):
            return Response(
                {"error": "part_of_url is required in the query parameters."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().create(request, *args, **kwargs)


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


url = "9bZkp7q19f0"
url = "https://www.youtube.com/watch?v=" + url
yt = YouTube(url)
# print(yt.title)
# print(yt.author)
# print(yt.views)
# print(yt.thumbnail_url)
