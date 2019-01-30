from texture import extract_texture, stitch_texture

pand_0363100012115783 = {
    "gevel0": [
        (123422.05, 488024.75, 30),
        (123423.89, 488029.21, 30),
        (123423.89, 488029.21, 0),
        (123422.05, 488024.75, 0),
    ],
    "gevel1": [
        (123423.89, 488029.21, 30),
        (123423.26, 488035.67, 30),
        (123423.26, 488035.67, 0),
        (123423.89, 488029.21, 0),
    ],
    "gevel2": [
        (123423.26, 488035.67, 30),
        (123410.54, 488039.40, 30),
        (123410.54, 488039.40, 0),
        (123423.26, 488035.67, 0),
    ],
    "gevel3": [
        (123410.54, 488039.40, 30),
        (123412.59, 488026.96, 30),
        (123412.59, 488026.96, 0),
        (123410.54, 488039.40, 0),
    ]
}

resolutie0 = (100, 600)
resolutie1 = (130, 600)
resolutie2 = (266, 600)
resolutie3 = (254, 600)

fotopunt0 = (123442.230211847, 488047.259717303, 6)
input0 = "input/TMX7316010203-000724_pano_0000_001219.jpg"

fotopunt1 = (123392.719592802, 487997.60068834, 8)
input1 = "input/TMX7316010203-000724_pano_0000_000057.jpg"

extract_texture(pand_0363100012115783["gevel0"], fotopunt0, input0, "obj_output/0363100012115783_gevel0.jpg",
                resolutie0)
extract_texture(pand_0363100012115783["gevel1"], fotopunt0, input0, "obj_output/0363100012115783_gevel1.jpg",
                resolutie1)
extract_texture(pand_0363100012115783["gevel2"], fotopunt0, input0, "obj_output/0363100012115783_gevel2.jpg",
                resolutie2)
extract_texture(pand_0363100012115783["gevel3"], fotopunt1, input1, "obj_output/0363100012115783_gevel3.jpg",
                resolutie3)

stitch_texture("obj_output/0363100012115783.jpg", [("obj_output/0363100012115783_gevel0.jpg", resolutie0),
                                                   ("obj_output/0363100012115783_gevel1.jpg", resolutie1),
                                                   ("obj_output/0363100012115783_gevel2.jpg", resolutie2),
                                                   ("obj_output/0363100012115783_gevel3.jpg", resolutie3)])
