import argparse
from panorama_texture import export_line_to_texture


def split_to_nums(in_str):
    return list(map(float, in_str.split(',')))


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("pano_id", type=str, help="Id of the panorama to project on a plane")
    parser.add_argument("left", type=str, help="comma-separated x,y in RD: left bottom point of the plane to project on")
    parser.add_argument("right", type=str, help="comma-separated x,y in RD: right bottom point of the plane to project on")
    parser.add_argument("filename", type=str, help="output filename")

    parser.add_argument("--resolution", type=int, help="Resolution in pixels per meter (defaults to 10)")
    parser.add_argument("--height", type=int, help="Height of the facade in meters (defaults to 30)")

    args = parser.parse_args()
    line = [split_to_nums(args.left), split_to_nums(args.right)]
    resolution = 10 if not args.resolution else args.resolution
    height = 30 if not args.height else args.height

    image_file = export_line_to_texture(args.pano_id, line, resolution, height)
    image_file.save(f'textmap_output/{args.filename}', 'jpeg')


if __name__ == '__main__':
    main()
