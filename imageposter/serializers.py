from rest_framework import serializers
from .models import PostedPicture


class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostedPicture
        fields = '__all__'


class PictureApiSerializer(serializers.Serializer):
    width = serializers.IntegerField()
    height = serializers.IntegerField()
    name = serializers.CharField()
    file = serializers.FileField()

    def create(self, validated_data):
        return PostedPicture.objects.create(**validated_data)

