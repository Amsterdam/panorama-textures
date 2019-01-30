from numpy import squeeze, dsplit, asarray, dstack
from scipy.ndimage import map_coordinates


def get_rgb_channels_from_array_image(array_img):
    """
    Orders the dimensions of the scipy image array around, so that it becomes an array of three color channels

    :param array_img: image array
    :return: reordered image array
    """
    # split image in the 3 RGB channels
    return squeeze(dsplit(array_img, 3))


def get_as_rgb_array(image_file):
    """
    Gets the raw image prepared for calculations.

    :param image_file: loaded image file
    :return: scipy image array, an array of three color channels
    """
    # read image as scipy rgb image array
    panorama_array_image = asarray(image_file, dtype="int32")
    return get_rgb_channels_from_array_image(panorama_array_image)


def sample_rgb_array_image_as_array(coordinates, rgb_array):
    """
    Resampling of the source image

    :param coordinates: meshgrid of numpy arrays where eacht target coordinate is mapped to a coordinateset
    of the source
    :param rgb_array: the source image as a scipy rgb array representation
    :return: the sampled target image as a scipy rgb array representation
    """
    x = coordinates[0]
    y = coordinates[1]

    # resample each channel of the source image
    #   (this needs to be done 'per channel' because otherwise the map_coordinates method
    #    works on the wrong dimension: in rgb_array_images from scipy.misc.fromimage the
    #    first dimension is the channel (r, g and b), and 2nd and 3rd dimensions are y and x,
    #    but map_coordinates expects the the coordinates to map to to be 1st and 2nd, therefore
    #    we extract each channel, so that y and x become 1st and 2nd array), after resampling
    #    we stack the three channels on top of each other, to restore the rgb image array

    r = map_coordinates(rgb_array[0], [y, x], order=1)
    g = map_coordinates(rgb_array[1], [y, x], order=1)
    b = map_coordinates(rgb_array[2], [y, x], order=1)

    # merge channels
    return dstack((r, g, b))
