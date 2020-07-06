import functools

import trio
from hypercorn.config import Config
from hypercorn.trio import serve
from quart import abort
from quart import jsonify
from quart_trio import QuartTrio

from goeatlocals.places import PLACES
from goeatlocals.places import PLACES_FROM_ID

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


def run_app():
    config = Config()
    config.bind = ['0.0.0.0:8000']
    trio.run(functools.partial(serve, app, config))


if __name__ == '__main__':
    run_app()
