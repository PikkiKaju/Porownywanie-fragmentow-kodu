import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status

from backend import settings

from .models import *
from .serializer import *

# Class-based view for handling Text-related data (text input)
class TextView(APIView):
  serializer_class = TextSerializer 

  # GET method to retrieve all Text objects
  def get(self, request):
    # A list of dictionaries containing the id and inputText of each Text object
    textDetail = [{"id": detail.id, "inputText": detail.inputText} for detail in Text.objects.all()]
    return Response(textDetail)

  # POST method to create a new Text object
  def post(self, request):
    # Create a serializer instance with the request data
    serializer = TextSerializer(data=request.data)  

    # Check if the data is valid
    if serializer.is_valid(raise_exception=True):  
      serializer.save()  # Save the new Text object to the database
      return Response(serializer.data)

  # DELETE method to delete a Text object by its primary key (pk)
  def delete(self, request, pk):
    try:
      react_object = Text.objects.get(pk=pk)  # Retrieve the Text object to be deleted
      react_object.delete()  # Delete the object from the database
      return Response(status=status.HTTP_204_NO_CONTENT)
    except Text.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)


# Class-based view for handling file uploads
class FileView(APIView):
  parser_classes = [MultiPartParser]  # Set the parser for handling multipart form data (file uploads)
  serializer_class = FileSerializer

  # GET method to retrieve all File objects
  def get(self, request):
    # A list of dictionaries containing the id and file URL of each File object
    files = File.objects.all()  # Pobierz wszystkie pliki
    serializer = FileSerializer(files, many=True)  # Zastosuj serializer do listy plików
    return Response(serializer.data, status=status.HTTP_200_OK)

  # POST method to upload a new file
  def post(self, request):
        files = request.FILES.getlist('files')

        if not files:
            return Response({"error": "No files provided."}, status=status.HTTP_400_BAD_REQUEST)

        file_instances = []
        for file in files:
            file_instance = File.objects.create(file=file)
            file_instances.append(file_instance)

        serializer = FileSerializer(file_instances, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

  # DELETE method to delete a File object by its primary key (pk)
  def delete(self, request, pk):
    try:
      react_object = File.objects.get(pk=pk)  # Retrieve the File object to be deleted
      react_object.delete()  # Delete the object from the database
      return Response(status=status.HTTP_204_NO_CONTENT) 
    except File.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)
    
# Class-based view for handling file uploads for the HDHGN
class HDHGNFileView(APIView):
  parser_classes = [MultiPartParser]  # Set the parser for handling multipart form data (file uploads)
  serializer_class = FileSerializer

  def runFileAnalysis(self,file):
    return file

  # POST method to upload a new file
  def post(self, request):
    # Create a serializer instance with the request data
    serializer = FileSerializer(data=request.data)

    # Check if the data is valid
    if serializer.is_valid(raise_exception=True):
      # Save the new File object to the database
      file_instance = serializer.save()

      # Run the file analysis
      self.runFileAnalysis(os.path.join(settings.MEDIA_ROOT, serializer.data['file']))

      # Delete the File instance from db and storage
      file_instance.delete()

      return Response(serializer.data)


