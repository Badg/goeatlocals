'''Temporarily hard-code places just so we can get things going on the
frontend.
'''

PLACES = [
    {
        'name': 'Drexl',
        'placeID': 1,
        'placeLong': -122.2674272,
        'placeLat': 37.8072493,
        'placePrimaryType': 'liquor',
        'placeDetails': {
            'osmID': 3056134586,
            'hasFood': 0.0,
            'hasBooze': 5.0,
            'hasBeer': 3.0,
            'hasProvisions': 0.0
        }
    },
    {
        'name': '355',
        'placeID': 2,
        'placeLong': -122.2669739,
        'placeLat': 37.8068275,
        'placePrimaryType': 'liquor',
        'placeDetails': {
            'osmID': 1079401457,
            'hasFood': 0.0,
            'hasBooze': 4.0,
            'hasBeer': 3.0,
            'hasProvisions': False
        }
    },
    {
        'name': 'Itani Ramen',
        'placeID': 3,
        'placeLong': -122.2699126,
        'placeLat': 37.8076042,
        'placePrimaryType': 'restaurant',
        'placeDetails': {
            'osmID': 4095991379,
            'hasFood': 5.0,
            'hasBooze': 0.0,
            'hasBeer': 2.0,
            'hasProvisions': 0.0
        }
    },
    {
        'name': 'The Telegraph',
        'placeID': 4,
        'placeLong': -122.2685736,
        'placeLat': 37.8128233,
        'placePrimaryType': 'beerwine',
        'placeDetails': {
            'osmID': 3470332401,
            'hasFood': 4.0,
            'hasBooze': 1.0,
            'hasBeer': 4.0,
            'hasProvisions': 0.0
        }
    },
    {
        'name': 'Duende',
        'placeID': 5,
        'placeLong': -122.2695932,
        'placeLat': 37.8081307,
        'placePrimaryType': 'restaurant',
        'placeDetails': {
            'osmID': 3470332399,
            'hasFood': 5.0,
            'hasBooze': 3.0,
            'hasBeer': 3.0,
            'hasProvisions': 0.0
        }
    },
    {
        'name': 'The Lunch Box',
        'placeID': 6,
        'placeLong': -122.2680771,
        'placeLat': 37.8065924,
        'placePrimaryType': 'restaurant',
        'placeDetails': {
            'osmID': 1186413873,
            'hasFood': 4.0,
            'hasBooze': None,
            'hasBeer': None,
            'hasProvisions': 0.0
        }
    },
    {
        'name': 'Howden Market',
        'placeID': 7,
        'placeLong': -122.2672438,
        'placeLat': 37.8055483,
        'placePrimaryType': 'grocery',
        'placeDetails': {
            'osmID': 3927998690,
            'hasFood': 0.0,
            'hasBooze': 0.0,
            'hasBeer': 1.0,
            'hasProvisions': 3.0
        }
    }
]


PLACES_FROM_ID = {place['placeID']: place for place in PLACES}
