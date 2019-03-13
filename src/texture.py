from PIL import Image
from numpy import linspace, float64, meshgrid

from array_image import get_as_rgb_array, sample_rgb_array_image_as_array
from array_math import get_rd_vector, cartesian2cylindrical

SOURCE_WIDTH = 8000  # pixels
PANO_ASPECT = 2  # width over height
PANO_HEIGHT = SOURCE_WIDTH / PANO_ASPECT


def extract_texture(obj, pov, input_filename, output_filename, output_resolution):
    """ Extract the texture of a 3D plane from a panorama image

    :param obj: a 3D plane, an array of 4 3D points (x, y, z): [left-top, right-top, right-bottom, left-bottom]
    :param pov: a 3D point, center of the panorama
    :param input_filename: filename of the panorama
    :param output_filename: target filename of the texture
    :param output_resolution: target resolution (x, y) of the texture
    """

    left_top_x = obj[0][0]
    right_bottom_x = obj[2][0]

    left_top_y = obj[0][1]
    right_bottom_y = obj[2][1]

    left_top_z = obj[0][2]
    right_bottom_z = obj[2][2]

    nx, ny = output_resolution
    x = linspace(left_top_x, right_bottom_x, nx, dtype=float64)
    y = linspace(left_top_y, right_bottom_y, nx, dtype=float64)
    z = linspace(left_top_z, right_bottom_z, ny, dtype=float64)

    gevel_x, _ = meshgrid(x, z)
    gevel_y, gevel_z = meshgrid(y, z)

    vector_x, vector_y, vector_z = get_rd_vector((gevel_x, gevel_y, gevel_z), pov)

    image_x, image_y = cartesian2cylindrical((vector_y, vector_x, vector_z), source_width=SOURCE_WIDTH,
                                             source_height=PANO_HEIGHT, r_is_1=False)

    source_file = Image.open(input_filename)
    source_rgb_array = get_as_rgb_array(source_file)

    image = sample_rgb_array_image_as_array((image_x, image_y), source_rgb_array)

    image_file = Image.fromarray(image.astype('uint8'), 'RGB')

    image_file.save(output_filename, 'jpeg')


def stitch_texture(target, sources):
    """Stitches multiple images horizontally

    :param target: target image file name
    :param sources: array of images, left to right, to stitch. Formatted like: (filename, (size_x, size_y))
    """

    result_width = 0
    result_height = 0
    for source in sources:
        result_width = result_width + source[1][0]
        result_height = max(result_height, source[1][1])

    width_index = 0
    result = Image.new('RGB', (result_width, result_height))
    for source in sources:
        image = Image.open(source[0])
        result.paste(im=image, box=(width_index, 0))
        width_index = width_index + source[1][0]

    result.save(target, 'jpeg')
