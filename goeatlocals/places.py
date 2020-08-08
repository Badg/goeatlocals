'''Temporarily hard-code places just so we can get things going on the
frontend.
'''
import json
import uuid

import asyncpg
import base58
from trio_asyncio import aio_as_trio


# TODO: lol not this
_CONN_KWARGS = {
    'host': 'goeatlocals_client_web-postgis',
    'database': 'gis',
    'user': 'postgres',
    # TODO: lol not this; not that it'd work in prod anyways
    'password': 'postgres'
}


async def get_places_bbox(top, right, bottom, left):
    places_from_db = await _get_place_records(top, right, bottom, left)

    if places_from_db is None:
        return []
    else:
        return [_convert_record_to_api(place) for place in places_from_db]


async def get_place(place_id):
    place_uuid = uuid.UUID(bytes=base58.b58decode(place_id.encode()))
    place_from_db = await _get_place_record(place_uuid)

    if place_from_db is not None:
        return _convert_record_to_api(place_from_db)


def _convert_record_to_api(record):
    geojson = json.loads(record['locator_point_json'])
    return {
        'name': record['identity_name'],
        'placeID': base58.b58encode(record['place_id'].bytes).decode(),
        'placeLong': geojson['coordinates'][0],
        'placeLat': geojson['coordinates'][1],
        'placePrimaryType': record.get('identity_display_class'),
        'placeDetails': {
            'hasFood': None,
            'hasBooze': None,
            'hasBeer': None,
            'hasProvisions': None
        }
    }


@aio_as_trio
async def _get_place_record(place_id):
    # TODO: not this!! need a global pool somewhere!
    async with asyncpg.create_pool(**_CONN_KWARGS) as conn_pool:
        async with conn_pool.acquire() as conn:
            record = await conn.fetchrow('''
                SELECT
                    place_id,
                    identity_name,
                    identity_display_class,
                    ST_AsGeoJSON(ST_Transform(locator_point, 4326))
                        AS locator_point_json,
                    locator_address
                FROM app_placedata.places placedata
                WHERE placedata.place_id = $1;
            ''', place_id)

            if record is None:
                return None
            else:
                return dict(record)


@aio_as_trio
async def _get_place_records(top, right, bottom, left):
    # TODO: not this!! need a global pool somewhere!
    async with asyncpg.create_pool(**_CONN_KWARGS) as conn_pool:
        async with conn_pool.acquire() as conn:
            # NOTE THE ORDER CHANGE!! compared to the signature above. We're
            # using CSS ordering in our corosignature, but the postgis
            # function uses left, bottom, right, top instead
            records = await conn.fetch('''
                SELECT
                    place_id,
                    identity_name,
                    identity_display_class,
                    ST_AsGeoJSON(ST_Transform(locator_point, 4326))
                        AS locator_point_json,
                    locator_address
                FROM app_placedata.places placedata
                WHERE ST_Contains(
                    ST_Transform(
                        ST_MakeEnvelope($1, $2, $3, $4, 4326),
                        3857
                    ),
                    placedata.locator_point);
                ''', left, bottom, right, top)

            return [dict(record) for record in records]


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
