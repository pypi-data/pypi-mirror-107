"""
Render jinja data
"""
import tempfile

import _jsonnet


async def render(hub, data):
    """
    Render the given data through jsonnet
    """
    if not isinstance(data, (str, bytes, bytearray)):
        data = data.read()
    with tempfile.NamedTemporaryFile("w+") as fp:
        fp.write(data)
        fp.flush()
        ret = _jsonnet.evaluate_file(fp.name)

    return hub.rend.json.render(ret)
