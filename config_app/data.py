import json

config_template = {}

# Note on Bulk Update, Change config_template.json file
#back slash was giving error
with open("config_app/config_template.json", "rb") as file:
    config_template['1'] = json.load(file)

current_configs = {}