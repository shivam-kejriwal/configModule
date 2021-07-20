from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ConfigSerializer

# Create your views here.

class ConfigAPIView(APIView):
    
    def post(self,request):
        serializer = ConfigSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.validated_data , status = status.HTTP_201_CREATED)