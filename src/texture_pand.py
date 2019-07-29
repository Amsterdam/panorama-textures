import argparse

from panorama_texture import export_pand_to_texture


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("pano_id", type=str, help="Id of the panorama to project on a plane")
    parser.add_argument("pand_id", type=str, help="The BAG ID of the building on which the panorama is to be projected")
    parser.add_argument("filename", type=str, help="output filename")

    parser.add_argument("--resolution", type=int, help="Resolution in pixels per meter (defaults to 10)")
    parser.add_argument("--height", type=int, help="Height of the facade in meters (defaults to 30)")
    parser.add_argument("--simplify", type=int, help="Smoothing the geometry, in meters (default off)")
    parser.add_argument("--force", action="store_true", help="Force all forward facing sides to be projected, even"
                                                             " those under a shallow angle")

    args = parser.parse_args()
    resolution = 10 if not args.resolution else args.resolution
    height = 30 if not args.height else args.height
    simplify = None if not args.simplify else args.simplify
    force = True if args.force else False

    export_pand_to_texture(args.pano_id, args.pand_id, args.filename, resolution, height, simplify, force)


if __name__ == '__main__':
    main()
