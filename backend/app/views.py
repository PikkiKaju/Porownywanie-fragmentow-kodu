import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status
import json

from backend.settings import BASE_DIR, MEDIA_ROOT

from .models import *
from .serializer import *

import HDHGN.PredictFile


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
      text_object = Text.objects.get(pk=pk)  # Retrieve the Text object to be deleted
      text_object.delete()  # Delete the object from the database
      return Response(status=status.HTTP_204_NO_CONTENT)
    except Text.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)


class FileListView(APIView):
    parser_classes = [MultiPartParser]  # Set the parser for handling multipart form data (file uploads)
    serializer_class = FileSerializer

    # POST method to upload a new file
    def post(self, request):
        # Check if the request is valid
        files = request.FILES.getlist('files')
        if not files:
            return Response({"error": "No files provided."}, status=status.HTTP_400_BAD_REQUEST)

        file_instances = []
        for file in files:
            file_instance = File.objects.create(file=file)
            file_instances.append(file_instance)

        serializer = FileSerializer(file_instances, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    # GET method to retrieve all File objects
    def get(self, request):
        try:
            # A list of dictionaries containing the id and file path of each File object
            files = File.objects.all()

            # Create the response object
            response = []
            for file in files:
                file_path = file.file.path
                # Check if file exists and add its contents to the response
                if os.path.exists(file_path):
                    with open(file_path, 'rb') as f:
                        file_content = f.read()
                    response.append({
                        "id": file.id,
                        "file_name": file.file.name,
                        "file_content": file_content
                    })
            return Response(response, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

# Class-based view for handling file uploads
class FileSingleView(APIView):
    # GET method to retrieve a speicific File object by its primary key (pk)
    def get(self, request, pk):
        try:
            file_object = File.objects.get(pk=pk) # Retrive the File object
            file_path = file_object.file.path # Get the file path
            # Check if file exists and send its contents
            if os.path.exists(file_path):
                with open(file_path, 'rb') as file:
                    file_content = file.read()
                
                return Response(file_content, content_type='application/octet-stream', status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    # DELETE method to delete a File object by its primary key (pk)
    def delete(self, request, pk):
        try:
            file_object = File.objects.get(pk=pk)  # Retrieve the File object to be deleted
            file_path = file_object.file.path  # Get the file path

            # Delete the object from the database
            file_object.delete() 

            # Delete the file from the file system
            if os.path.exists(file_path):
                os.remove(file_path)

            return Response(status=status.HTTP_204_NO_CONTENT) 
        except File.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        

class FilePredictView(APIView):
    parser_classes = [MultiPartParser]

    # POST method to upload a new file
    def post(self, request, results_size=5):
        # Check if the request is valid
        files = request.FILES.getlist('files')
        if not files:
            return Response({"error": "No files provided."}, status=status.HTTP_400_BAD_REQUEST)

        # Create a serializer instance with the request data and run the file prediction
        results = []
        for file in files:
            file_instance = File.objects.create(file=file)
            # Run file prediction
            file_path = os.path.join(MEDIA_ROOT,"uploads", file.name)
            results.append(self.runFilePrediction(file_path, results_size))
            # Delete the File instance from db and storage
            file_instance.delete()

        return Response(json.dumps(results), status=status.HTTP_201_CREATED)

    def runFilePrediction(self, file_path, results_size):
        '''
        Run file prediction script using HDHGN and return the results.

        Returns:
        dict object: {
            file_type: str, 
            file_lang: str, 
            results: [(
                label: str, 
                similarity_value: [float], 
                probability: [float]
            )], 
            files_contents: [(
                file_name: str, 
                file_content: str
            )]
        }
        '''
        results, file_lang = HDHGN.PredictFile.predict(file_path)
        
        files_contents = []
        results_contents = []
        if (results is not None):
            for i in range(len(results) if len(results) < results_size else results_size):
                file_name = results[i][0] + (".c" if file_lang == "C" else ".py")
                new_path = os.path.join(BASE_DIR, "HDHGN", "data", f"txt_{file_lang.lower()}_files", file_name)
                with open(new_path, 'r') as file:
                    file_content = file.read()
                    files_contents.append((file_name, file_content))
                results_contents.append((results[i][0], results[i][1], results[i][2]))
        
        if results is not None:
            results_dict = {
                "file_name": os.path.basename(file_path),
                "file_lang": file_lang,
                "results": results_contents,
                "files_contents": files_contents
            }
        else:
            results_dict = None
            
        return results_dict
    