from texture import extract_texture, stitch_texture

pand_0363100012066079 = {
    "gevel0": [
        (123432.07, 488073.58, 30),
        (123405.35, 488068.64, 30),
        (123405.35, 488068.64, 0),
        (123432.07, 488073.58, 0),
    ],
    "gevel1": [
        (123405.35, 488068.64, 30),
        (123409.50, 488044.92, 30),
        (123409.50, 488044.92, 0),
        (123405.35, 488068.64, 0),
    ],
    "gevel2": [
        (123409.50, 488044.92, 30),
        (123420.74, 488046.92, 30),
        (123420.74, 488046.92, 0),
        (123409.50, 488044.92, 0),
    ],
    "gevel3": [
        (123420.74, 488046.92, 30),
        (123418.74, 488057.78, 30),
        (123418.74, 488057.78, 0),
        (123420.74, 488046.92, 0),
    ],
    "gevel4": [
        (123418.74, 488057.78, 30),
        (123434.28, 488060.71, 30),
        (123434.28, 488060.71, 0),
        (123418.74, 488057.78, 0),
    ],
}

resolutie0 = (564, 600)
resolutie1 = (482, 600)
resolutie2 = (228, 600)
resolutie3 = (220, 600)
resolutie4 = (316, 600)

fotopunt0 = (123389.966272313, 488091.214142029, 2)
input0 = "input/TMX7316010203-000724_pano_0000_000215.jpg"

fotopunt1 = (123442.230211847, 488047.259717303, 6)
input1 = "input/TMX7316010203-000724_pano_0000_001219.jpg"

extract_texture(pand_0363100012066079["gevel0"], fotopunt0, input0, "obj_output/0363100012066079_gevel0.jpg",
                resolutie0)
extract_texture(pand_0363100012066079["gevel1"], fotopunt0, input0, "obj_output/0363100012066079_gevel1.jpg",
                resolutie1)
extract_texture(pand_0363100012066079["gevel2"], fotopunt1, input1, "obj_output/0363100012066079_gevel2.jpg",
                resolutie2)
extract_texture(pand_0363100012066079["gevel3"], fotopunt1, input1, "obj_output/0363100012066079_gevel3.jpg",
                resolutie3)
extract_texture(pand_0363100012066079["gevel4"], fotopunt1, input1, "obj_output/0363100012066079_gevel4.jpg",
                resolutie4)

stitch_texture("obj_output/0363100012066079.jpg", [("obj_output/0363100012066079_gevel0.jpg", resolutie0),
                                                   ("obj_output/0363100012066079_gevel1.jpg", resolutie1),
                                                   ("obj_output/0363100012066079_gevel2.jpg", resolutie2),
                                                   ("obj_output/0363100012066079_gevel3.jpg", resolutie3),
                                                   ("obj_output/0363100012066079_gevel4.jpg", resolutie4)])



