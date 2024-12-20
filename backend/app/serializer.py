from rest_framework import serializers
from .models import *

class TextSerializer(serializers.ModelSerializer):
    """
    Serializer for the Text model. Serializes and deserializes Text model data to/from JSON.

    Fields:
        - id: The primary key of the Text instance.
        - inputText: The text input by the user.
    """
    class Meta:
        model = Text
        fields = ['id', 'inputText']

class FileSerializer(serializers.ModelSerializer):
    """
    Serializer for the File model. Serializes and deserializes File model data to/from JSON.

    Fields:
        - id: The primary key of the File instance.
        - file: The FileField representing the uploaded file.  In the JSON response, this will contain the file path.
    """
    class Meta:
        model = File
        fields = ['id', 'file']