from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import HomePageView, AddImage, PictureViewSet

router = DefaultRouter()
router.register('all_pictures', PictureViewSet, basename='all_pictures')

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('add/', AddImage.as_view(), name='add'),
]

urlpatterns += router.urls


