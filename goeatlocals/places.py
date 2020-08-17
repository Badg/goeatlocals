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
        'osmID': str(record['osm_id']),
        'status': record['status'],
        'info': {
            'identity': {
                'displayClass': record.get('identity_display_class'),
            },
            'locators': {
                'lat': geojson['coordinates'][1],
                'lon': geojson['coordinates'][0],
                'address': _extract_address(record),
                'phone': record.get('locator_phone'),
                'website': record.get('locator_website'),
            },
            'inventory': {
                'preparedFood': None,
                'fullAlcohol': None,
                'lightAlcohol': None,
                'grocery': None,
            },
        }
    }


def _extract_address(record):
    # Note that the address record might be present but None, so this way we
    # handle both that and a missing record
    address_record = record.get('locator_address') or {}
    return {
        'streetNumber': address_record.get('street_number'),
        'streetName': address_record.get('street_name'),
        'unitNumber': address_record.get('unit_number'),
        'neighborhood': address_record.get('neighborhood'),
        'city': address_record.get('city'),
        'state': address_record.get('state'),
        'country': address_record.get('country'),
        'postalCode': address_record.get('postal_code'),
    }


@aio_as_trio
async def _get_place_record(place_id):
    # TODO: not this!! need a global pool somewhere!
    async with asyncpg.create_pool(**_CONN_KWARGS) as conn_pool:
        async with conn_pool.acquire() as conn:
            record = await conn.fetchrow('''
                SELECT
                    place_id,
                    osm_id,
                    identity_name,
                    identity_display_class,
                    status,
                    locator_website,
                    locator_phone,
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
                    osm_id,
                    identity_name,
                    identity_display_class,
                    status,
                    locator_website,
                    locator_phone,
                    ST_AsGeoJSON(ST_Transform(locator_point, 4326))
                        AS locator_point_json,
                    locator_address
                FROM app_placedata.places placedata
                WHERE ST_Contains(
                    ST_Transform(
                        ST_MakeEnvelope($1, $2, $3, $4, 4326),
                        3857
                    ),
                    placedata.locator_point)
                ORDER BY identity_name;
                ''', left, bottom, right, top)

            return [dict(record) for record in records]
