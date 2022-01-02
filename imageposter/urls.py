from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import HomePageView, AddImage, PictureViewSet, AddPictureApi, AddPictureApi1

router = DefaultRouter()
router.register('all_pictures', PictureViewSet, basename='all_pictures')

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('add/', AddImage.as_view(), name='add'),
    path('api', AddPictureApi.as_view(), name='api'),
    path('api1', AddPictureApi1.as_view(), name='api1'),

]

urlpatterns += router.urls


