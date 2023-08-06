{
    'type': {
        'required': True,
        'type': 'string',
        'regex': '^(?i)(prog|sys|bd)$'
    },
    'titre': {
        'required': False,
        'type': 'string'
    },
    'description': {
        'required': False,
        'type': 'string'
    },
    'énoncé': {
        'required': False,
        'type': 'string'
    },
    'rétroactions': {
        'required': True,
        'type': 'dict',
        'schema': {
            'positive': {
                'required': False,
                'type': 'string'
            },
            'négative': {
                'required': False,
                'type': 'string'
            },
            'erreur': {
                'required': False,
                'type': 'string'
            }
        }
    }
}