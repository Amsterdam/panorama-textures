import argparse
from panorama_texture import export_composite_to_texture


def split_to_nums(in_str):
    return list(map(float, in_str.split(',')))


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("from_pano_id", type=str, help="Id of the first panorama in a row to project")
    parser.add_argument("to_pano_id", type=str, help="Id of the first panorama in a row to project (should be same )")
    parser.add_argument("left", type=str, help="comma-separated x,y in RD: left bottom point of the plane to project on")
    parser.add_argument("right", type=str, help="comma-separated x,y in RD: right bottom point of the plane to project on")
    parser.add_argument("filename", type=str, help="output filename")

    parser.add_argument("--steps", type=int, help="Sample one in every steps panorama (defaults to 1)")
    parser.add_argument("--resolution", type=int, help="Resolution in pixels per meter (defaults to 10)")
    parser.add_argument("--height", type=int, help="Height of the facade in meters (defaults to 30)")

    args = parser.parse_args()
    line = [split_to_nums(args.left), split_to_nums(args.right)]
    resolution = 10 if not args.resolution else args.resolution
    height = 30 if not args.height else args.height
    steps = 1 if not args.steps else args.steps

    image_file = export_composite_to_texture(args.from_pano_id, args.to_pano_id, line, resolution, height, steps)
    image_file.save(f'textmap_output/{args.filename}', 'jpeg')


if __name__ == '__main__':
    main()
