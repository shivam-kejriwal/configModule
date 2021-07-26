import json

config_template = {}

current_configs = {}

default_values = {}

def createDefaultObject(template_object):
    for key in template_object['configFields']:
        default_values[key] = template_object['configFields'][key]['default']

# Note on Bulk Update, Change config_template.json file
with open("config_app/config_template.json", "rb") as file:
    template = json.load(file)
    template_id = template['templateID']
    config_template[template_id] = template
    createDefaultObject(config_template[template_id])





    
