import json
import uuid

from rest_framework import serializers

from config_app import data


class TemplateSerializer(serializers.Serializer):
    templateID = serializers.CharField(max_length=500)
    templateName = serializers.CharField(max_length=500)
    configFields = serializers.JSONField()

    def validate(self, attrs):

        template_id = str(attrs.get('templateID'))

        if template_id not in data.config_template.keys():
            return serializers.ValidationError('Requested Template ID does not exist')

        values = attrs.get('configFields')

        # all new config fields added must have type and default
        for key in values:
            if 'default' not in values[key]:
                raise serializers.ValidationError('Must include default')
            if 'type' not in values[key]:
                raise serializers.ValidationError('Must include type')

        # all new config values should be updated in the template
        data.config_template[template_id].update(attrs)

        # update the default config template file
        with open("config_app\\config_template.json", "w") as file:
            json.dump(data.config_template[template_id], file, indent=2)

        return super().validate(attrs)


class ConfigSerializer(serializers.Serializer):
    configName = serializers.CharField(max_length=500)
    values = serializers.JSONField()
    templateID = serializers.CharField(max_length=500)

    def validate(self, attrs):

        config_id = uuid.uuid4()
        t_id = attrs.get('templateID')
        try:
            template = data.config_template[t_id]
        except KeyError as e:
            raise serializers.ValidationError(e)

        for key in attrs.get('values'):
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
