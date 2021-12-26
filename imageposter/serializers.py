from rest_framework import serializers
from .models import PostedPicture


class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostedPicture
        fields = '__all__'
