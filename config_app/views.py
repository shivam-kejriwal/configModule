from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ConfigSerializer
from config_app import data


class ConfigAPIView(APIView):

    def post(self, request):
        serializer = ConfigSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)


class TemplateAPIView(APIView):
    """
    Get, Create the template

    """

    def get(self, request):
        try:
            get_template = data.config_template[1]
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(get_template, status=status.HTTP_200_OK)
