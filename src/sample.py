from texture import extract_texture, stitch_texture

# based on https://api.data.amsterdam.nl/gebieden/bouwblok/03630012100975/
paleis = {
    "voorgevel": [
        (121259.16, 487327.24, 25),
        (121262.10, 487407.36, 25),
        (121262.10, 487407.36, 0.5),
        (121259.16, 487327.24, 0.5),
    ],
    "opgang": [
        (121263.99, 487354.34, 25),
        (121265.04, 487379.63, 25),
        (121265.04, 487379.63, 0.5),
        (121263.99, 487354.34, 0.5),
    ]
}

# based on https://api.data.amsterdam.nl/bag/pand/0363100012175378/
tussauds = {
    "rokin": [
        (121325.44, 487281.05, 22),
        (121327.33, 487311.08, 22),
        (121327.33, 487311.08, 0),
        (121325.44, 487281.05, 0),
    ],
    "dam": [
        (121327.33, 487311.08, 22),
        (121284.20, 487314.43, 22),
        (121284.20, 487314.43, 0),
        (121327.33, 487311.08, 0),
    ]
}

resolutie = (1000, 300)
fotopunt = (121348.591054272, 487338.811130636, 2)
input_filename = "input/TMX7316010203-000716_pano_0000_001622.jpg"
output_filename = "sample_output/paleis_voorgevel.jpg"

extract_texture(paleis["voorgevel"], fotopunt, input_filename, output_filename, resolutie)
extract_texture(paleis["opgang"], fotopunt, input_filename, "sample_output/paleis_opgang.jpg", (440, 490))

extract_texture(tussauds["rokin"], fotopunt, input_filename, "sample_output/tussauds_rokin.jpg", (500, 440))
extract_texture(tussauds["dam"], fotopunt, input_filename, "sample_output/tussauds_dam.jpg", (1000, 440))

stitch_texture("sample_output/tussauds.jpg", [("sample_output/tussauds_rokin.jpg", (500, 440)), ("sample_output/tussauds_dam.jpg", (1000, 440))])
