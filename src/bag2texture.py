import json
from io import BytesIO

import requests

from PIL import Image
from math import cos, sin, pi, sqrt, acos
from functools import reduce
from numpy import linspace, float64, meshgrid, full, int32
from array_math import get_vector, cartesian2cylindrical
from array_image import get_as_rgb_array, sample_rgb_array_image_as_array
from osgeo import ogr, osr
from geojson_rewind import rewind

X, Y = 0, 1

SOURCE_WIDTH = 8000  # pixels
PANO_ASPECT = 2  # width over height
PANO_HEIGHT = SOURCE_WIDTH / PANO_ASPECT

camera_height = 2
resolution = 10  # in pixels per m of the object


def vector(from_2d, to_2d):
    return to_2d[X] - from_2d[X], to_2d[Y] - from_2d[Y]


def vector_length(vector_2d):
    return sqrt(vector_2d[X]**2 + vector_2d[Y]**2)


def main(pano_id, output_hoogte, filename, pand_id=None, blok_id=None):
    hoogte = output_hoogte

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

    if not pand_id is None:
        bag_url = f"https://api.data.amsterdam.nl/bag/pand/{pand_id}/"
    elif not blok_id is None:
        bag_url = f"https://api.data.amsterdam.nl/gebieden/bouwblok/{blok_id}/"
    assert bag_url

    with requests.get(bag_url) as response:
        geometrie = json.loads(response.content)['geometrie']

    if geometrie['type'] == 'Polygon':
        geometrie['coordinates'] = [geometrie['coordinates'][0]]
    else:
        geometrie['type'] = 'Polygon'
        geometrie['coordinates'] = [geometrie['coordinates'][0][0]]

    # not all geometrie's are right-hand-wound.
    geometrie = rewind(geometrie)
    ogr_geom = ogr.CreateGeometryFromJson(json.dumps(geometrie))
    simplified = ogr_geom.Simplify(2)
    simple_json = simplified.ExportToJson()
    geometrie = json.loads(simple_json)
    geometrie = rewind(geometrie)
    polygon = geometrie['coordinates'][0]

    lines = []
    ny = int(round(hoogte * resolution))

    for i, point in enumerate(list(reversed(polygon))):
        vertices = [polygon[i], polygon[0]] if i+1 == len(polygon) else [polygon[i], polygon[i+1]]

        line = {
            'from': vertices[0],
            'to': vertices[1],
            'vector': vector(vertices[0], vertices[1])
        }
        line['length'] = vector_length(line['vector'])

        cs = cos(0.5*pi)
        sn = sin(0.5*pi)

        p_x = line['vector'][X] * cs - line['vector'][Y] * sn
        p_y = line['vector'][X] * sn + line['vector'][Y] * cs

        perpendicular = (p_x, p_y)
        compare = (line['from'][X]+perpendicular[X], line['from'][Y]+perpendicular[Y])
        line['forward_facing'] = vector_length(vector(pov, line['from'])) < vector_length(vector(pov, compare))

        midpoint = ((vertices[0][X]+vertices[0][X])/2, (vertices[0][Y]+vertices[0][Y])/2)
        to_midpoint = vector(pov, midpoint)
        if vector_length(perpendicular) == 0 or vector_length(to_midpoint) == 0:
            line['viewing_angle'] = 0
        else:
            line['viewing_angle'] = acos((-1 * perpendicular[X]*to_midpoint[Y] - perpendicular[Y]*to_midpoint[X]) /
                                    (vector_length(perpendicular)*vector_length(to_midpoint)))

        nx = int(round(line['length'] * resolution))

        x = linspace(line['from'][X], line['to'][X], nx, dtype=float64)
        y = linspace(line['from'][Y], line['to'][Y], nx, dtype=float64)
        z = linspace(hoogte, 0, ny, dtype=float64)

        gevel_x, _ = meshgrid(x, z)
        gevel_y, gevel_z = meshgrid(y, z)

        line['x-mesh'] = gevel_x
        line['y-mesh'] = gevel_y
        line['z-mesh'] = gevel_z

        lines.append(line)

    facades = []
    for facade in lines:
        nx = int(round(facade['length'] * resolution))
        if nx > 0:
            if 1.8*pi > facade['viewing_angle'] > 0.2*pi : # or facade['viewing_angle'] > 1.25*pi:
                facades.append({'width': nx, 'image_array': full((ny, nx, 3), 128, dtype=int32)})
            else:
                vector_x, vector_y, vector_z = get_vector((facade['x-mesh'], facade['y-mesh'], facade['z-mesh']), pov)
                image_x, image_y = cartesian2cylindrical((vector_y, vector_x, vector_z), source_width=SOURCE_WIDTH,
                                                         source_height=PANO_HEIGHT, r_is_1=False)

                with requests.get(image_url) as response:
                    source_file = Image.open(BytesIO(response.content))

                source_rgb_array = get_as_rgb_array(source_file)

                image = sample_rgb_array_image_as_array((image_x, image_y), source_rgb_array)
                facades.append({'width': nx, 'image_array': image})

    img_width = reduce(lambda x, facade: facade['width'] + x, facades, 0)
    img_height = ny

    width_index = 0
    result = Image.new('RGB', (img_width, img_height))
    for facade in facades:
        image_file = Image.fromarray(facade['image_array'].astype('uint8'), 'RGB')
        result.paste(im=image_file, box=(width_index, 0))
        width_index = width_index + facade['width']

    result.save(f'textmap_output/{filename}', 'jpeg')


pano_ids = ["TMX7316010203-000720_pano_0000_000290", "TMX7316010203-000720_pano_0000_000056", "TMX7316010203-000720_pano_0000_000045",
            "TMX7316010203-000720_pano_0000_000032", "TMX7316010203-000720_pano_0000_000019", "TMX7316010203-000716_pano_0000_001497"]
bag_pand_id = "0363100012167579"
bag_blok_id = "03630012100975"
filename = "paleis_simple_"
hoogte = 32

if __name__ == "__main__":
    for i, pano_id in enumerate(pano_ids):
        main(pano_id, hoogte, f"{filename}_{i}.jpg", pand_id=bag_pand_id, blok_id=bag_blok_id)
