from panda3d.core import GeomVertexFormat, GeomVertexData, VBase3
from panda3d.core import Geom, GeomTriangles, GeomVertexWriter
from panda3d.core import GeomNode

def createCube(parent, index, cubeMembership, walls):

    vertexFormat = GeomVertexFormat.getV3n3cp()
    vertexData = GeomVertexData("cube_data", vertexFormat, Geom.UHStatic)
    tris = GeomTriangles(Geom.UHStatic)

    posWriter = GeomVertexWriter(vertexData, "vertex")
    colWriter = GeomVertexWriter(vertexData, "color")
    normalWriter = GeomVertexWriter(vertexData, "normal")

    vertexCount = 0

    for direction in (-1, 1):

        for i in range(3):

            normal = VBase3()
            normal[i] = direction
            rgb = [0., 0., 0.]
            rgb[i] = 1.

            if direction == 1:
                rgb[i-1] = 1.

            r, g, b = rgb
            color = (r, g, b, 0.)

            for a, b in ( (-1., -1.), (-1., 1.), (1., 1.), (1., -1.) ):

                pos = VBase3()
                pos[i] = direction
                pos[(i + direction) % 3] = a
                pos[(i + direction * 2) % 3] = b

                posWriter.addData3f(pos)
                colWriter.addData4f(color)
                normalWriter.addData3f(normal)

            vertexCount += 4

            tris.addVertices(vertexCount - 2, vertexCount - 3, vertexCount - 4)
            tris.addVertices(vertexCount - 4, vertexCount - 1, vertexCount - 2)

    geom = Geom(vertexData)
    geom.addPrimitive(tris)
    node = GeomNode("cube_node")
    node.addGeom(geom)
    cube = parent.attachNewNode(node)
    x = index % 9 // 3 - 1
    y = index // 9 - 1
    z = index % 9 % 3 - 1
    cube.setScale(.4)
    cube.setPos(x * 0.85, y * 0.85, z * 0.85)
    membership = set() # the walls this cube belongs to
    cubeMembership[cube] = membership

    if x == -1:
        walls["left"].append(cube)
        membership.add("left")
    elif x == 1:
        walls["right"].append(cube)
        membership.add("right")
    if y == -1:
        walls["front"].append(cube)
        membership.add("front")
    elif y == 1:
        walls["back"].append(cube)
        membership.add("back")
    if z == -1:
        walls["bottom"].append(cube)
        membership.add("bottom")
    elif z == 1:
        walls["top"].append(cube)
        membership.add("top")

    return cube