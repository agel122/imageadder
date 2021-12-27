import hashlib

from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status


from .models import PostedPicture
from .forms import PostImage
from .serializers import PictureSerializer, PictureApiSerializer


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
        height = request.data.get("height")
        name = request.data.get("name")
        file = request.data.get("file")
        hash_name = hashlib.md5(name.encode()).hexdigest()
        new_filename = f'{hash_name}_{width}x{height}'
        serializer = PictureSerializer(data={
            'title': new_filename,
            'cover': file,
        })
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)














