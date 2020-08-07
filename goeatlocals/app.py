import functools
import json

import asks
import trio
import trio_asyncio
from hypercorn.config import Config
from hypercorn.trio import serve
from quart import abort
from quart import jsonify
from quart import request
from quart_trio import QuartTrio

from goeatlocals.cities import CITIES
from goeatlocals.cities import CITY_CACHES
from goeatlocals.places import get_place
from goeatlocals.places import get_places_bbox
from goeatlocals.mapstyles import MAPSTYLES
from goeatlocals.mapstyles import FONTS_STATIC_PATH
from goeatlocals.mapstyles import TILES_STATIC_PATH

app = QuartTrio(__name__)


@app.route('/api/')
async def index():
    return b'Hello. World?'


@app.route('/api/places')
async def get_all_places():

    city = request.args.get('city')
    bbox = {
        'top': request.args.get('north'),
        'right': request.args.get('east'),
        'bottom': request.args.get('south'),
        'left': request.args.get('west')
    }

    if city is not None:
        city = city.lower()
        if city not in CITIES:
            return jsonify({
                'clientStatusHint': 404,
                'clientErrorMessage':
                    'Unknown city!'
            }), 404
        elif city in CITY_CACHES:
            return jsonify(CITY_CACHES[city])
        else:
            bbox = CITIES[city]
            response = await get_places_bbox(**bbox)
            CITY_CACHES[city] = response
            return jsonify(response)

    elif any((bbox_value is None for bbox_value in bbox.values())):
        return jsonify({
            'clientStatusHint': 400,
            'clientErrorMessage':
                'Need a city or a proper bounding box!'
        }), 400

    bbox = {key: float(value) for key, value in bbox.items()}
    return jsonify(await get_places_bbox(**bbox))


@app.route('/api/places/<place_id>')
async def get_place_details(place_id):
    place = await get_place(place_id)
    if place is None:
        return jsonify({
            'clientStatusHint': 404,
            'clientErrorMessage':
                "We don't have a record of that place. " +
                'Is it in another castle?'
        }), 404
    else:
        return jsonify(place)


@app.route('/api/maps/styles/<style_id>.json')
async def get_mapstyle(style_id):
    if style_id not in MAPSTYLES:
        return abort(404)
    else:
        json_txt = await MAPSTYLES[style_id].render()
        # this is janky as all fuck but it's faster than looking up how to set
        # the right content type because quart docs are kinda lame
        return jsonify(json.loads(json_txt))


@app.route('/api/maps/tiles.json')
async def get_tiles_def():
    # this is janky as all fuck but it's faster than looking up how to set
    # the right content type because quart docs are kinda lame
    return jsonify(json.loads(await TILES_STATIC_PATH.read_text()))


@app.route('/api/maps/fonts/<fontstack>/<fontrange>.pbf')
async def get_mapstyle_fontstack(fontstack, fontrange):
    # TODO EXTREMELY IMPORTANT: this is unsanitized input being put on the
    # filesystem. This is extremely unsafe! THIS IS AN ATTACK VECTOR!
    # DO NOT SHIP THIS TO PROD!
    fontstack_path = FONTS_STATIC_PATH / fontstack / f'{fontrange}.pbf'
    if await fontstack_path.exists():
        return await fontstack_path.read_bytes()
    else:
        abort(404)


def run_app():
    config = Config()
    config.bind = ['0.0.0.0:8000']
    trio_asyncio.run(functools.partial(serve, app, config))


if __name__ == '__main__':
    run_app()
