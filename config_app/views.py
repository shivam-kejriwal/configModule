from os import error
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ConfigSerializer
from config_app import data

from config_app import serializers


class ConfigAPIView(APIView):

    def post(self, request):
        print(request.data)
        serializer = ConfigSerializer(data=request.data , context = {'method' : request.method} )
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
            return Response({"success" : False}, status=status.HTTP_400_BAD_REQUEST)

        return Response(get_template, status=status.HTTP_200_OK)


class ListConfigAPIView(APIView):

    def get(self, request):
        try:
            get_configs = data.current_configs.values()
        except Exception as e:
            return Response({"success" : False}, status=status.HTTP_400_BAD_REQUEST)

        return_json = {'count': len(get_configs), 'configs': get_configs}

        return Response(return_json, status=status.HTTP_200_OK)


class CheckConfigAPIView(APIView):

    def get(self , request):
        json_data = {}
        config_id = request.query_params.get('configID' , None)
        template_id = request.query_params.get('templateID' , None) 
        error_message = {'success' : False}

        if template_id is not None :
            try : 
                json_data['template'] = data.config_template[template_id]
            except Exception as e:
                error_message['message'] = 'templateID key not found'
                return Response(error_message , status=status.HTTP_400_BAD_REQUEST)
        else:
            error_message['message'] = 'missing templateID in URL'
            return Response(error_message, status = status.HTTP_404_NOT_FOUND)

        if config_id is not None :
            try :
                json_data['config'] = data.current_configs[config_id]
            except Exception as e:
                error_message['message'] = 'configID key not found'
                return Response(error_message , status=status.HTTP_400_BAD_REQUEST)
        else:
            error_message['message'] = 'missing configID in URL'
            return Response(error_message, status = status.HTTP_404_NOT_FOUND)


        return Response(json_data , status = status.HTTP_200_OK) 