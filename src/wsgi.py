import io
from flask import Flask, request, send_file

from panorama_texture import export_line_to_texture, export_pand_to_texture, export_blok_to_texture, export_composite_to_texture
from texture_line import split_to_nums

app = Flask(__name__)


def _response_image(image, filename):
    img_io = io.BytesIO()
    image.save(img_io, 'jpeg')
    img_io.seek(0)
    return send_file(img_io, attachment_filename=filename, mimetype='image/jpeg')


# 127.0.0.1:5000/textures/composite?from_pano_id=TMX7316010203-001181_pano_0000_005814&to_pano_id=TMX7316010203-001181_pano_0000_005849&left=121947.89,486581.27&right=122118.38,486632.83&filename=test.jpg&steps=2&height=20&resolution=12
@app.route("/textures/composite")
def composite():
    from_pano_id = request.args['from_pano_id']
    to_pano_id = request.args['to_pano_id']
    left = request.args['left']
    right = request.args['right']
    filename = request.args['filename']

    resolution = 10 if not 'resolution' in request.args else int(request.args['resolution'])
    height = 30 if not 'height' in request.args else int(request.args['height'])
    steps = 1 if not 'steps' in request.args else int(request.args['steps'])
    line = [split_to_nums(left), split_to_nums(right)]

    return _response_image(export_composite_to_texture(from_pano_id, to_pano_id, line, resolution, height, steps), filename)


# 127.0.0.1:5000/textures/line?pano_id=TMX7316010203-001187_pano_0000_001503&left=121386.57,487384.36&right=121440.98,487341.41&filename=test.jpg
@app.route("/textures/line")
def line():
    pano_id = request.args['pano_id']
    left = request.args['left']
    right = request.args['right']
    filename = request.args['filename']

    resolution = 10 if not 'resolution' in request.args else int(request.args['resolution'])
    height = 30 if not 'height' in request.args else int(request.args['height'])
    line = [split_to_nums(left), split_to_nums(right)]

    return _response_image(export_line_to_texture(pano_id, line, resolution, height), filename)


# 127.0.0.1:5000/textures/pand?pano_id=TMX7316010203-001187_pano_0000_001503&pand_id=0363100012168052&filename=test.jpg
@app.route("/textures/pand")
def pand():
    pano_id = request.args['pano_id']
    pand_id = request.args['pand_id']
    filename = request.args['filename']

    resolution = 10 if not 'resolution' in request.args else int(request.args['resolution'])
    height = 30 if not 'height' in request.args else int(request.args['height'])
    simplify = None if not 'simplify' in request.args else int(request.args['simplify'])
    force = 'force' in request.args
    img = export_pand_to_texture(pano_id, pand_id, resolution, height, simplify, force)

    return _response_image(img, filename)


# 127.0.0.1:5000/textures/bouwblok?pano_id=TMX7316010203-001187_pano_0000_001503&blok_id=03630012100938&filename=test.jpg
@app.route("/textures/bouwblok")
def bouwblok():
    pano_id = request.args['pano_id']
    blok_id = request.args['blok_id']
    filename = request.args['filename']

    resolution = 10 if not 'resolution' in request.args else int(request.args['resolution'])
    height = 30 if not 'height' in request.args else int(request.args['height'])
    simplify = None if not 'simplify' in request.args else int(request.args['simplify'])
    force = 'force' in request.args
    img = export_blok_to_texture(pano_id, blok_id, resolution, height, simplify, force)

    return _response_image(img, filename)


@app.route("/status/health")
def health():
    return "<h1 style='color:blue'>Healthy!</h1>"


if __name__ == "__main__":
    app.run()
