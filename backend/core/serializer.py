from rest_framework import serializers
from .models import *


class ReactSerializer(serializers.ModelSerializer):
    class Meta:
        model = React
        fields = ['name', 'detail']


class SendImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SendImage
        fields = ['src','image_id']

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['image_id']

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['image_id','note']

class UploadimageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadImage
        fields = ['image_id','image']