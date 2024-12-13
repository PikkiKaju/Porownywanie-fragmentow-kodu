from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from . models import *
from . serializer import *

class ReactView(APIView):
  
  serializer_class = ReactSerializer

  def get(self, request):
    detail = [ {"id":detail.id, "inputText": detail.inputText} for detail in React.objects.all()]
    return Response(detail)

  def post(self, request):
    serializer = ReactSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
      serializer.save()
      return  Response(serializer.data)
      
  def delete(self, request, pk):
    try:
      react_object = React.objects.get(pk=pk)
      react_object.delete()
      return Response(status=status.HTTP_204_NO_CONTENT) 
    except React.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)