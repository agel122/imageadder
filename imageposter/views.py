from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy

from rest_framework import viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status


from .models import PostedPicture
from .forms import PostImage
from .serializers import PictureSerializer, PictureApiSerializer

from rename_resize.resizer import resize_rename


class HomePageView(ListView):
    model = PostedPicture
    template_name = 'home.html'


class AddImage(CreateView):
    model = PostedPicture
    form_class = PostImage
    template_name = 'add.html'
    success_url = reverse_lazy('home')


class PictureViewSet(viewsets.ModelViewSet):
    queryset = PostedPicture.objects.all()
    serializer_class = PictureSerializer


class AddPictureApi(CreateAPIView):
    serializer_class = PictureApiSerializer

    def post(self, request, *args, **kwargs):
        width = request.data.get("width")
        if request.data.get("height"):
            height = request.data.get("height")
        else:
            height = None
        file = request.data.get("file")
        result = resize_rename(file, width, height)

        serializer = PictureSerializer(data={
            'title': result['name'],
            'cover': result['file'],
        })
        if serializer.is_valid():
            if not PostedPicture.objects.filter(title=result['name']):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                serializer = PictureSerializer(PostedPicture.objects.get(title=result['name']))
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddPictureApi1(CreateAPIView):
    serializer_class = PictureApiSerializer

    def post(self, request, *args, **kwargs):
        width = request.data.get("width")
        if request.data.get("height"):
            height = request.data.get("height")
        else:
            height = None
        file = request.data.get("file")
        result = resize_rename(file, width, height)

        serializer = PictureSerializer(data={
            'title': result['name'],
            'cover': result['file'],
        })
        if serializer.is_valid():
            if not PostedPicture.objects.filter(title=result['name']):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                serializer = PictureSerializer(PostedPicture.objects.get(title=result['name']))
                return Response({'url_to_file': PostedPicture.objects.get(title=result['name']).cover.url},
                                status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)












