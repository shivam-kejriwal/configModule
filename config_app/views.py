from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from config_app import data
from .serializers import *


class ConfigAPIView(APIView):

    def post(self, request):
        context = {
            'method': request.method
        }

        serializer = ConfigSerializer(data=request.data, context=context)
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
            return Response({"success": False}, status=status.HTTP_400_BAD_REQUEST)

        return Response(get_template, status=status.HTTP_200_OK)


class ListConfigAPIView(APIView):

    def get(self, request):
        try:
            get_configs = data.current_configs.values()
        except Exception as e:
            return Response({"success": False}, status=status.HTTP_400_BAD_REQUEST)

        return_json = {'count': len(get_configs), 'configs': get_configs}

        return Response(return_json, status=status.HTTP_200_OK)


class CheckConfigAPIView(APIView):

    def get(self, request):
        json_data = {}
        config_id = request.query_params.get('configID', None)
        template_id = request.query_params.get('templateID', None)
        error_response = {
            'success': False 
        }

        if template_id is not None:
            try:
                json_data['template'] = data.config_template[template_id]
            except Exception as e:
                error_response['message'] = 'templateID key not found'
                return Response(error_response, status=status.HTTP_400_BAD_REQUEST)
        else:
            error_response['message'] = 'missing templateID in URL'
            return Response(error_response, status=status.HTTP_404_NOT_FOUND)

        if config_id is not None:
            try:
                json_data['config'] = data.current_configs[config_id]
            except Exception as e:
                error_response['message'] = 'configID key not found'
                return Response(error_response, status=status.HTTP_400_BAD_REQUEST)
        else:
            error_response['message'] = 'missing configID in URL'
            return Response(error_response, status=status.HTTP_404_NOT_FOUND)

        return Response(json_data, status=status.HTTP_200_OK)


class EditConfigAPIView(APIView):
    """

    Edit a Particular Configuration

    """

    def patch(self, request, config_id):
        context = {
            'method': request.method,
            'config_id': str(config_id)
        }

        serializer = ConfigSerializer(data=request.data, context=context)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)


class BulkUpdateAPIView(APIView):

    """

    This API is used to update the template,
    update the given configs a/c to modified template,
    existing configs will be filled with default values.

    """

    def post(self, request):

        try:
            all_configs = request.data['configs']
        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)

        try:
            serializer = TemplateSerializer(data=request.data['templates'], context={'method': request.method})
        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)

        message = []
        if serializer.is_valid(raise_exception=True):

            for config in all_configs:
                msg = {}
                if 'configID' in config:
                    context = {
                        'method': 'PATCH',
                        'config_id': config['configID']
                    }
                    conf_serializer = ConfigSerializer(data=config, context=context)
                    if conf_serializer.is_valid():
                        msg['success'] = True
                        msg['configID'] = config['configID']
                        message.append(msg)

        return Response(message, status=status.HTTP_200_OK)
