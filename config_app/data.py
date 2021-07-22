import json

config_template = {}

# Note on Bulk Update, Change config_template.json file
with open("config_app\\config_template.json", "rb") as file:
    template = json.load(file)
    template_id = template['templateID']
    config_template[template_id] = template

current_configs = {}
