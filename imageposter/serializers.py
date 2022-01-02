from rest_framework import serializers
from .models import PostedPicture


class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostedPicture
        fields = '__all__'


class PictureApiSerializer(serializers.Serializer):
    width = serializers.IntegerField()
    height = serializers.IntegerField(required=False, default=None)
    file = serializers.FileField()


