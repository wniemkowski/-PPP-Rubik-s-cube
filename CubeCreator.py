from panda3d.core import GeomVertexFormat, GeomVertexData
from panda3d.core import Geom, GeomTriangles, GeomVertexWriter
from panda3d.core import Texture, GeomNode
from panda3d.core import LVector3

RED = (1,0,0,0)
GREEN = (0,1,0,0)
BLUE = (0,0,1,0)
ORANGE = (1,165.0/255,0,0)
YELLOW = (1,1,0,0)
WHITE = (1,1,1,0)

def normalized(*args):
    myVec = LVector3(*args)
    myVec.normalize()
    return myVec

def makeSquare(x1, y1, z1, x2, y2, z2, wallColor):
    format = GeomVertexFormat.getV3n3cpt2()
    vdata = GeomVertexData('square', format, Geom.UHDynamic)

    vertex = GeomVertexWriter(vdata, 'vertex')
    normal = GeomVertexWriter(vdata, 'normal')
    color = GeomVertexWriter(vdata, 'color')
    texcoord = GeomVertexWriter(vdata, 'texcoord')

    # make sure we draw the sqaure in the right plane
    if x1 != x2:
        vertex.addData3(x1, y1, z1)
        vertex.addData3(x2, y1, z1)
        vertex.addData3(x2, y2, z2)
        vertex.addData3(x1, y2, z2)

        normal.addData3(normalized(2 * x1 - 1, 2 * y1 - 1, 2 * z1 - 1))
        normal.addData3(normalized(2 * x2 - 1, 2 * y1 - 1, 2 * z1 - 1))
        normal.addData3(normalized(2 * x2 - 1, 2 * y2 - 1, 2 * z2 - 1))
        normal.addData3(normalized(2 * x1 - 1, 2 * y2 - 1, 2 * z2 - 1))

    else:
        vertex.addData3(x1, y1, z1)
        vertex.addData3(x2, y2, z1)
        vertex.addData3(x2, y2, z2)
        vertex.addData3(x1, y1, z2)

        normal.addData3(normalized(2 * x1 - 1, 2 * y1 - 1, 2 * z1 - 1))
        normal.addData3(normalized(2 * x2 - 1, 2 * y2 - 1, 2 * z1 - 1))
        normal.addData3(normalized(2 * x2 - 1, 2 * y2 - 1, 2 * z2 - 1))
        normal.addData3(normalized(2 * x1 - 1, 2 * y1 - 1, 2 * z2 - 1))

    # adding different colors to the vertex for visibility
    for i in range(0,4):
        color.addData4f(wallColor)

    texcoord.addData2f(0.0, 1.0)
    texcoord.addData2f(0.0, 0.0)
    texcoord.addData2f(1.0, 0.0)
    texcoord.addData2f(1.0, 1.0)

    # Quads aren't directly supported by the Geom interface
    # you might be interested in the CardMaker class if you are
    # interested in rectangle though
    tris = GeomTriangles(Geom.UHDynamic)
    tris.addVertices(0, 1, 3)
    tris.addVertices(1, 2, 3)

    square = Geom(vdata)
    square.addPrimitive(tris)
    return square

def CreateCube():
    # Note: it isn't particularly efficient to make every face as a separate Geom.
    # instead, it would be better to create one Geom holding all of the faces.
    square0 = makeSquare(-1, -1, -1, 1, -1, 1,RED)
    square1 = makeSquare(-1, 1, -1, 1, 1, 1,GREEN)
    square2 = makeSquare(-1, 1, 1, 1, -1, 1,BLUE)
    square3 = makeSquare(-1, 1, -1, 1, -1, -1,ORANGE)
    square4 = makeSquare(-1, -1, -1, -1, 1, 1,WHITE)
    square5 = makeSquare(1, -1, -1, 1, 1, 1,YELLOW)
    snode = GeomNode('square')
    snode.addGeom(square0)
    snode.addGeom(square1)
    snode.addGeom(square2)
    snode.addGeom(square3)
    snode.addGeom(square4)
    snode.addGeom(square5)

    cube = render.attachNewNode(snode)

    # OpenGl by default only draws "front faces" (polygons whose vertices are
    # specified CCW).
    cube.setTwoSided(True)
    return cube