
config_template = {
    
    "1" : {
            'templateVersion': 'v1.0.0', 
            'templateName': 'Template For InNote', 
            'configFields': {
                'brokenName': {
                    'type': 'boolean', 
                    'default': True, 
                    'desc': 'Should the name be broken into different parts', 
                    'label': 'Single Name'
                }, 
                'firstName': {
                    'type': 'string', 
                    'default': 'First Name'
                }, 
                'showTermsAndConditions': {
                    'type': 'boolean', 
                    'default': True
                }, 
                'termsAndConditions': {
                    'type': 'text', 
                    'default': 
                    'Terms & Conditions'
                }, 
                'maxLoginFails': {
                    'type': 'number', 
                    'default': 5
                }
            }, 
            'templateID': "1"
        }
}


current_configs = {}