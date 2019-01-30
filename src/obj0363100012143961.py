from texture import extract_texture, stitch_texture

pand_0363100012143961 = {
    "gevel0": [
        (123412.58, 488027.02, 30),
        (123408.85, 488014.62, 30),
        (123408.85, 488014.62, 0),
        (123412.58, 488027.02, 0),
    ],
    "gevel1": [
        (123408.85, 488014.62, 30),
        (123419.35, 488011.69, 30),
        (123419.35, 488011.69, 0),
        (123408.85, 488014.62, 0),
    ]
}

resolutie0 = (260, 600)
resolutie1 = (220, 600)

fotopunt = (123392.719592802, 487997.60068834, 8)
input_filename = "input/TMX7316010203-000724_pano_0000_000057.jpg"

extract_texture(pand_0363100012143961["gevel0"], fotopunt, input_filename, "obj_output/0363100012143961_gevel0.jpg",
                resolutie0)
extract_texture(pand_0363100012143961["gevel1"], fotopunt, input_filename, "obj_output/0363100012143961_gevel1.jpg",
                resolutie1)

stitch_texture("obj_output/0363100012143961.jpg", [("obj_output/0363100012143961_gevel0.jpg", resolutie0),
                                                   ("obj_output/0363100012143961_gevel1.jpg", resolutie1)])
