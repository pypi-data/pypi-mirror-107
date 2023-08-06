{
    'ébauches': {
        'required': True,
        'type': 'dict',
    },
    'tests': {
        'required': True,
        'type': 'list',
        'schema': {
            'required': True,
            'type': 'dict',
            'schema': {
                'nom': {
                    'required': True,
                    'type': 'string'
                },
                'entrée': {
                    'required': True,
                    'type': ['string', 'integer']
                },
                'sortie': {
                    'required': True,
                    'type': ['string', 'integer']
                },
                'rétroactions': {
                    'required': False,
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
        }
    }
}
