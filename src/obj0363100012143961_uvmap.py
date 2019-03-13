from math import floor, ceil, sqrt, acos, pi
from PIL import Image
from array_math import uvmap


def vector_length(vector):
    return sqrt(vector[0] ** 2 + vector[1] ** 2 + vector[2] ** 2)


def remove_uvmap(vertex):
    if len(vertex) == 0:
        return vertex

    f_vertices = vertex.split("/")
    return f"{f_vertices[0]}//{f_vertices[2]}"


def add_uvmap(vertex, fotopunt, length, index):
    if len(vertex) == 0:
        return vertex

    f_vertices = vertex.split("/")

    n_vertex = n_vertices[int(f_vertices[2]) - 1]
    f_vertex = vertices[int(f_vertices[0]) - 1]
    ref_vertex = (f_vertex[0] - fotopunt[0], f_vertex[1] - fotopunt[1], f_vertex[2] - fotopunt[2])

    dot_product = ref_vertex[0] * n_vertex[0] + ref_vertex[1] * n_vertex[1] + ref_vertex[2] * n_vertex[2]
    cos_theta = dot_product / (vector_length(n_vertex) * vector_length(ref_vertex))

    angle = acos(cos_theta)

    if angle < 0.45 * pi:
        f_vertices[1] = str(int(f_vertices[0]) + length * index)

    return "/".join(f_vertices)


def in_facade(face, idx, length):
    if has_no_texture(face):
        return False
    vt_index = int(face[1].split("/")[1])
    return idx * length < vt_index <= (idx + 1) * length


def has_no_texture(face):
    return len(face[1].split("/")[1]) == 0


# facades = [
#     {
#         'mtl': "0363100012143961.000",
#         'fotopunt': (123392.71505322, 487997.599548511, 8.05939939245582),
#         'file': "input/TMX7316010203-000724_pano_0000_000057.jpg"
#     }
# ]

facades = [
    {
        'mtl': "0363100012143961.001",
        'fotopunt': (123410.2, 488003.2, 2.49),
        'file': "input/TMX7316010203-000724_pano_0000_000149.jpg"
    },
    {
        'mtl': "0363100012143961.002",
        'fotopunt': (123400.9, 488027.6, 6.84),
        'file': "input/TMX7316010203-000724_pano_0000_000063.jpg"
    }
]

vertices = []
n_vertices = []
faces = []

with open("input/0363100012143961.obj") as f:
    for line in f:
        if line.startswith("v "):
            _, x, y, z = line.rstrip('\n').split(" ")
            vertices.append((float(x), float(y), float(z),))
        elif line.startswith("f "):
            faces.append(line.rstrip('\n').split(" ")[1:])
        elif line.startswith("vn "):
            _, x, y, z = line.rstrip('\n').split(" ")
            n_vertices.append((float(x), float(y), float(z),))

faces = [[remove_uvmap(vertex) for vertex in face] for face in faces]

uvmapping = {}
for i, facade in enumerate(facades):
    uvmapping[facade['mtl']] = [uvmap(vertex, facade['fotopunt']) for vertex in vertices]

    pix_xs = [uv[0] for uv in uvmapping[facade['mtl']]]
    pix_ys = [uv[1] for uv in uvmapping[facade['mtl']]]

    min_x = floor(min(pix_xs))
    min_y = floor(min(pix_ys))
    max_x = ceil(max(pix_xs))
    max_y = ceil(max(pix_ys))

    width = max_x - min_x
    height = max_y - min_y

    img = Image.open(facade['file'])
    texture = img.crop((min_x, min_y, max_x, max_y))
    texture.save(f"textmap_output/{facade['mtl']}.jpg")

    uvmapping[facade['mtl']] = [(uv[0] - min_x, uv[1] - min_y) for uv in uvmapping[facade['mtl']]]
    uvmapping[facade['mtl']] = [(uv[0] / width, 1 - uv[1] / height) for uv in uvmapping[facade['mtl']]]

    faces = [[add_uvmap(vertex, facade['fotopunt'], len(vertices), i) for vertex in face] for face in faces]

    for uv in uvmapping[facade['mtl']]:
        print(f"vt {uv[0]} {uv[1]}")

print("usemtl basis\ns 1")
for face in faces:
    if has_no_texture(face):
        print(f"f {' '.join(face)}")


for i, facade in enumerate(facades):
    print(f"usemtl {facade['mtl']}\ns 1")
    for face in faces:
        if in_facade(face, i, len(vertices)):
            print(f"f {' '.join(face)}")
