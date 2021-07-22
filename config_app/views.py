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
    Get the Default Template

    """

    def get(self, request):
        try:
            get_template = data.config_template.values()
        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)

        return Response(get_template, status=status.HTTP_200_OK)


class ListConfigAPIView(APIView):

    def get(self, request):
        try:
            get_configs = data.current_configs.values()
        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)

        return_json = {'count': len(get_configs), 'configs': get_configs}

        return Response(return_json, status=status.HTTP_200_OK)
