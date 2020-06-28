import functools

import trio
from hypercorn.config import Config
from hypercorn.trio import serve
from quart_trio import QuartTrio

app = QuartTrio(__name__)


@app.route('/api/')
async def index():
    return b'Hello. World?'


def run_app():
    config = Config()
    config.bind = ['0.0.0.0:8000']
    trio.run(functools.partial(serve, app, config))


if __name__ == '__main__':
    run_app()
