from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy

from rest_framework import viewsets


from .models import PostedPicture
from .forms import PostImage
from .serializers import PictureSerializer

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
