from rest_framework import serializers
from config_app import data
import uuid


class ConfigSerializer(serializers.Serializer):
    configName = serializers.CharField()
    values = serializers.JSONField()
    templateID = serializers.CharField()

    def validate(self, attrs):

        config_id = uuid.uuid4()
        t_id = attrs['templateID']
        try:
            template = data.config_template[t_id]
        except KeyError as e:
            raise serializers.ValidationError(e)

        for key in attrs['values']:
            try:
                default_value = template['configFields'][key]['default']
            except KeyError as e:
                raise serializers.ValidationError(e)

            if checkForMismatch(attrs['values'][key], default_value):
                raise serializers.ValidationError("Value for the field " + key + " doesn't matches it's dataType")

        attrs['configID'] = config_id
        data.current_configs[config_id] = attrs

        return super().validate(attrs)


def checkForMismatch(data, value):
    if type(data) != type(value):
        return True
    return False
