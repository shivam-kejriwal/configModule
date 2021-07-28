import json

config_template = {}

current_configs = {}

default_values = {}


def CreateDefaultObject(template_object):
    newly_added = {}
    for key in template_object['configFields']:
        if key not in default_values:
            newly_added[key] = template_object['configFields'][key]['default']

        default_values[key] = template_object['configFields'][key]['default']

    return newly_added

# Note on Bulk Update, Change config_template.json file
with open("config_app/config_template.json", "rb") as file:
    template = json.load(file)
    template_id = template['templateID']
    config_template[template_id] = template
    CreateDefaultObject(config_template[template_id])