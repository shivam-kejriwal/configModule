import json
import uuid

from rest_framework import serializers

from config_app import data


# Serialize a Template
class TemplateSerializer(serializers.Serializer):
    templateID = serializers.CharField(max_length=150)
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

            # all new config fields must added to all existing configs with the default values
            for config_id in data.current_configs:
                if key not in data.current_configs[config_id]['values']:
                    data.current_configs[config_id]['values'][key] = values[key]['default']

        method = self.context.get('method')

        if method == 'POST':

            # update template name
            data.config_template[template_id]['templateName'] = attrs.get('templateName')

            # all new config values should be updated in the template
            data.config_template[template_id]['configFields'].update(values)

            # all new config fields must added to all existing configs with the default values
            for key in values:
                for config_id in data.current_configs:
                    if key not in data.current_configs[config_id]['values']:
                        data.current_configs[config_id]['values'][key] = values[key]['default']

            # update the default config template file
            with open("config_app\\config_template.json", "w") as file:
                json.dump(data.config_template[template_id], file)

            attrs = data.config_template[template_id]

        return super().validate(attrs)


# Serialize a Config
class ConfigSerializer(serializers.Serializer):
    configName = serializers.CharField(max_length=500)
    values = serializers.JSONField()
    templateID = serializers.CharField(max_length=150)

    def validate(self, attrs):

        t_id = attrs['templateID']
        try:
            template = data.config_template[t_id]
        except KeyError as e:
            raise serializers.ValidationError(e)

        for key in attrs['values']:
            try:
                default_value = template['configFields'][key]['default']
                dtype = template['configFields'][key]['type']
            except KeyError as e:
                raise serializers.ValidationError(e)

            if checkForMismatch(attrs['values'][key], default_value):
                raise serializers.ValidationError("Value for the field " + key + " doesn't matches it's dataType")

            if dtype == 'string' and len(attrs['values'][key]) > 100:
                raise serializers.ValidationError(
                    "Value for the field " + key + " exceeds the limit for the Single line Text")

        method = self.context.get('method')
        if method == 'POST':
            config_id = str(uuid.uuid4())
            attrs['configID'] = config_id
            values = attrs['values'].copy()
            attrs['values'] = data.default_values.copy()
            attrs['values'].update(values)
            data.current_configs[config_id] = attrs

        elif method == 'PATCH':
            config_id = self.context.get('config_id')

            # check config id available?
            try:
                data.current_configs[config_id]['values'].update(attrs['values'])
            except KeyError as e:
                raise serializers.ValidationError(e)

            data.current_configs[config_id]['configName'] = attrs.get('configName')
            attrs = data.current_configs[config_id]

        return super().validate(attrs)


def checkForMismatch(data, value):
    if type(data) != type(value):
        return True
    return False
