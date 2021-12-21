from django.urls import path

from .views import HomePageView, AddImage

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('add/', AddImage.as_view(), name='add'),
]
