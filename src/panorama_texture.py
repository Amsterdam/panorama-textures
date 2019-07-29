import json
from io import BytesIO

import requests

from PIL import Image
from math import cos, sin, pi, sqrt, acos, atan2
from functools import reduce
from numpy import linspace, float64, meshgrid, full, int32
from array_math import get_vector, cartesian2cylindrical
from array_image import get_as_rgb_array, sample_rgb_array_image_as_array
from osgeo import ogr, osr
from geojson_rewind import rewind

# helper constants for readability
X, Y = 0, 1

SOURCE_WIDTH = 8000  # pixels
PANO_ASPECT = 2  # width over height
PANO_HEIGHT = SOURCE_WIDTH / PANO_ASPECT

# postulated height of the camera on the car
camera_height = 2


def vector(from_2d, to_2d):
    return to_2d[X] - from_2d[X], to_2d[Y] - from_2d[Y]


def vector_length(vector_2d):
    return sqrt(vector_2d[X]**2 + vector_2d[Y]**2)


def export_to_texture(pano_id, height, resolution, filename, simplify, force, pand_id=None, blok_id=None):
    source_file, pov = _get_pano_image(pano_id)
    polygon = _extract_bag_polygon(blok_id, pand_id, simplify)
    img_height = int(round(height * resolution))

    lines = []
    # ny = int(round(hoogte * resolution))

    for i, point in enumerate(list(polygon)):
        vertices = [polygon[i], polygon[0]] if i+1 == len(polygon) else [polygon[i], polygon[i+1]]
        lines.append(_create_line(height, img_height, resolution, pov, vertices))

    facades = []
    for facade in lines:
        facade_projection = _project_facade(facade, pov, source_file, img_height, resolution, force=force)
        if facade_projection is not None:
            facades.append(facade_projection)

    img_width = reduce(lambda x, facade: facade['width'] + x, facades, 0)

    width_index = 0
    result = Image.new('RGB', (img_width, img_height))
    for facade in facades:
        image_file = Image.fromarray(facade['image_array'].astype('uint8'), 'RGB')
        result.paste(im=image_file, box=(width_index, 0))
        width_index = width_index + facade['width']

    result.save(f'textmap_output/{filename}', 'jpeg')


def _project_facade(facade, pov, source_file, img_height, resolution, force=False):
    nx = int(round(facade['length'] * resolution))
    if nx > 0:
        if not facade['forward_facing'] or (not 0.7 * pi > facade['viewing_angle'] > 0.3 * pi and not force):
            imarray = {'width': nx, 'image_array': full((img_height, nx, 3), 128, dtype=int32)}
        else:
            vector_x, vector_y, vector_z = get_vector((facade['x-mesh'], facade['y-mesh'], facade['z-mesh']), pov)
            image_x, image_y = cartesian2cylindrical((vector_y, vector_x, vector_z), source_width=SOURCE_WIDTH,
                                                     source_height=PANO_HEIGHT, r_is_1=False)
            source_rgb_array = get_as_rgb_array(source_file)

            image = sample_rgb_array_image_as_array((image_x, image_y), source_rgb_array)
            imarray = {'width': nx, 'image_array': image}
    else:
        imarray = None
    return imarray


def _extract_bag_polygon(blok_id, pand_id, simplify):
    if not pand_id is None:
        bag_url = f"https://api.data.amsterdam.nl/bag/pand/{pand_id}/"
    elif not blok_id is None:
        bag_url = f"https://api.data.amsterdam.nl/gebieden/bouwblok/{blok_id}/"
    assert bag_url
    with requests.get(bag_url) as response:
        geometrie = json.loads(response.content)['geometrie']
    if geometrie['type'] == 'Polygon':
        # Read outer ring of Polygon
        geometrie['coordinates'] = [geometrie['coordinates'][0]]
    else:
        geometrie['type'] = 'Polygon'
        # Read outer ring of first Polygon from MultiPolygon
        geometrie['coordinates'] = [geometrie['coordinates'][0][0]]
    # not all geometrie's are right-hand-wound.
    geometrie = rewind(geometrie)
    if simplify:
        ogr_geom = ogr.CreateGeometryFromJson(json.dumps(geometrie))
        simplified = ogr_geom.Simplify(simplify)
        simple_json = simplified.ExportToJson()
        geometrie = json.loads(simple_json)
        geometrie = rewind(geometrie)
    return geometrie['coordinates'][0]


def _create_line(hoogte, img_height, resolution, pov, vertices):
    line = {
        'from': vertices[0],
        'to': vertices[1],
        'vector': vector(vertices[0], vertices[1])
    }
    line['length'] = vector_length(line['vector'])

    midpoint = ((vertices[0][X] + vertices[0][X]) / 2, (vertices[0][Y] + vertices[0][Y]) / 2)
    to_midpoint = vector(pov, midpoint)

    if line['length'] == 0 or vector_length(to_midpoint) == 0:
        line['viewing_angle'] = 0
    else:
        dot = line['vector'][X]*to_midpoint[X] + line['vector'][Y]*to_midpoint[Y]      # dot product
        det = line['vector'][X]*to_midpoint[Y] - line['vector'][Y]*to_midpoint[X]      # determinant
        line['viewing_angle'] = atan2(det, dot)

    line['forward_facing'] = line['viewing_angle'] > 0

    nx = int(round(line['length'] * resolution))
    x = linspace(line['from'][X], line['to'][X], nx, dtype=float64)
    y = linspace(line['from'][Y], line['to'][Y], nx, dtype=float64)
    z = linspace(hoogte, 0, img_height, dtype=float64)
    gevel_x, _ = meshgrid(x, z)
    gevel_y, gevel_z = meshgrid(y, z)
    line['x-mesh'] = gevel_x
    line['y-mesh'] = gevel_y
    line['z-mesh'] = gevel_z
    return line


def _get_pano_image(pano_id):
    with requests.get(f"https://api.data.amsterdam.nl/panorama/panoramas/{pano_id}/") as response:
        pano_data = json.loads(response.content)
    geom = pano_data['geometry']['coordinates']
    point = ogr.Geometry(ogr.wkbPoint)
    point.AddPoint(geom[0], geom[1], geom[2])
    source = osr.SpatialReference()
    source.ImportFromEPSG(4326)
    target = osr.SpatialReference()
    target.ImportFromEPSG(28992)
    transform = osr.CoordinateTransformation(source, target)
    point.Transform(transform)
    pov = (point.GetX(), point.GetY(), camera_height)
    image_url = pano_data['_links']['equirectangular_full']['href']
    with requests.get(image_url) as response:
        source_file = Image.open(BytesIO(response.content))
    return source_file, pov


def export_line_to_texture(pano_id, line, filename, resolution, height):
    source_file, pano_pov = _get_pano_image(pano_id)
    img_height = int(round(height * resolution))
    plane = _create_line(height, img_height, resolution, pano_pov, line)
    facade = _project_facade(plane, pano_pov, source_file, img_height, resolution, force=True)
    image_file = Image.fromarray(facade['image_array'].astype('uint8'), 'RGB')
    image_file.save(f'textmap_output/{filename}', 'jpeg')


def export_pand_to_texture(pano_id, pand_id, filename, resolution, height, simplify, force):
    export_to_texture(pano_id, height, resolution, filename, simplify, force, pand_id=pand_id)


def export_blok_to_texture(pano_id, blok_id, filename, resolution, height, simplify, force):
    export_to_texture(pano_id, height, resolution, filename, simplify, force, blok_id=blok_id)


if __name__ == "__main__":
    hoogte = 32
    resolution = 10

    export_to_texture("TMX7316010203-001187_pano_0000_001503", hoogte, resolution, "dam_1.jpg", None, True, pand_id="0363100012168052")
    export_to_texture("TMX7316010203-001187_pano_0000_001503", hoogte, resolution, "ya77.jpg", None, True, blok_id="03630012100938")
