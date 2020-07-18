import functools
import json

import asks
import trio
from hypercorn.config import Config
from hypercorn.trio import serve
from quart import abort
from quart import jsonify
from quart_trio import QuartTrio

from goeatlocals.places import PLACES
from goeatlocals.places import PLACES_FROM_ID
from goeatlocals.mapstyles import MAPSTYLES
from goeatlocals.mapstyles import FONTS_STATIC_PATH
from goeatlocals.mapstyles import TILES_STATIC_PATH

app = QuartTrio(__name__)


@app.route('/api/')
async def index():
    return b'Hello. World?'


@app.route('/api/places')
async def get_all_places():
    return jsonify(PLACES)


@app.route('/api/places/<place_id>')
async def get_place_details(place_id):
    place_id = int(place_id)
    if place_id in PLACES_FROM_ID:
        return jsonify(PLACES_FROM_ID[place_id])
    else:
        return jsonify({
            'clientStatusHint': 404,
            'clientErrorMessage':
                "We don't have a record of that place. " +
                'Is it in another castle?'
        }), 404


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
    trio.run(functools.partial(serve, app, config))


if __name__ == '__main__':
    run_app()
