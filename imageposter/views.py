import hashlib

# from PIL import Image
# import io

from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
# from django.core.files.base import ContentFile


from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status


from .models import PostedPicture
from .forms import PostImage
from .serializers import PictureSerializer, PictureApiSerializer

from rename_resize import resizer


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
        name_to_hash = file.name.split('.')[0]
        file_to_save = io.BytesIO()
        image = Image.open(file)
        image_resized = image.resize((int(width), int(height)))

        hash_name = hashlib.md5(name_to_hash.encode()).hexdigest()
        new_filename = f'{hash_name}_{width}x{height}'
        name_to_save = new_filename + '.png'
        image_resized.save(file_to_save, 'png')
        file_to_save.seek(0)
        django_friendly_file = ContentFile(file_to_save.read(), name_to_save)

        serializer = PictureSerializer(data={
            'title': new_filename,
            'cover': django_friendly_file,
        })
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)














