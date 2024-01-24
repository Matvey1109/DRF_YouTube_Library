from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.permissions import IsAdminUser
from .serializers import UserSerializer, VideoSerializer
from .models import Video
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth.models import User
from pytube import YouTube


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class VideoCreate(APIView):
    def post(self, request):
        part_of_url = request.data.get("part_of_url")  # part_of_url as a body param
        url = "https://www.youtube.com/watch?v=" + part_of_url

        try:
            yt = YouTube(url)
            video_data = {
                "title": yt.title,
                "author": yt.author,
                "thumbnail_url": yt.thumbnail_url,
                "number_of_views": yt.views,
                "user": request.user.id,
            }

            serializer = VideoSerializer(data=video_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserVideosList(generics.ListAPIView):
    serializer_class = VideoSerializer

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        return Video.objects.filter(user=user_id)


class VideoDelete(generics.DestroyAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_destroy(self, instance):
        instance.delete()


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
