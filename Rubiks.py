from direct.gui.OnscreenText import OnscreenText
from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
from direct.interval.IntervalGlobal import LerpHprInterval, Func, Sequence

import CubeCreator

class Rubiks(ShowBase):

    def __init__(self):

        ShowBase.__init__(self)

        walls = {}
        pivots = {}
        rotations = {}
        cubeMembership = {}
        wallIDs = ("front", "back", "left", "right", "bottom", "top")
        hprs = {}
        hprs["front"] = hprs["back"] = VBase3(0., 0., 90.)
        hprs["left"] = hprs["right"] = VBase3(0., 90., 0.)
        hprs["bottom"] = hprs["top"] = VBase3(90., 0., 0.)
        wallOrders = {}
        wallOrders["front"] = wallOrders["back"] = ["left", "top", "right", "bottom"]
        wallOrders["left"] = wallOrders["right"] = ["back", "top", "front", "bottom"]
        wallOrders["bottom"] = wallOrders["top"] = ["left", "front", "right", "back"]

        for wallID in wallIDs:
            walls[wallID] = []
            pivots[wallID] = self.render.attachNewNode('pivot_%s' % wallID)
            rotations[wallID] = {"hpr": hprs[wallID], "order": wallOrders[wallID]}

        for i in range(27):
            CubeCreator.createCube(self.render, i, cubeMembership, walls)

        self.directionalLight = DirectionalLight('directionalLight')
        self.directionalLightNP = self.cam.attachNewNode(self.directionalLight)
        self.directionalLightNP.setHpr(-20., -20., 0.)
        self.render.setLight(self.directionalLightNP)
        self.cam.setPos(-7., -10., 4.)
        self.cam.lookAt(0., 0., 0.)

        def reparentCubes(wallID):
            pivot = pivots[wallID]
            children = pivot.getChildren()
            children.wrtReparentTo(self.render)
            pivot.clearTransform()
            children.wrtReparentTo(pivot)
            for cube in walls[wallID]:
                cube.wrtReparentTo(pivot)

        def updateCubeMembership(wallID, negRotation=False):
            wallOrder = rotations[wallID]["order"]
            if not negRotation:
                wallOrder = wallOrder[::-1]
            for cube in walls[wallID]:
                oldMembership = cubeMembership[cube]
                newMembership = set()
                cubeMembership[cube] = newMembership
                for oldWallID in oldMembership:
                    if oldWallID in wallOrder:
                        index = wallOrder.index(oldWallID)
                        newWallID = wallOrder[index-1]
                        newMembership.add(newWallID)
                    else:
                        newMembership.add(oldWallID)
                for oldWallID in oldMembership - newMembership:
                    walls[oldWallID].remove(cube)
                for newWallID in newMembership - oldMembership:
                    walls[newWallID].append(cube)

        self.seq = Sequence()

        def addInterval(wallID, negRotation=False):
            self.seq.append(Func(reparentCubes, wallID))
            rot = rotations[wallID]["hpr"]
            if negRotation:
                rot = rot * -1.
            self.seq.append(LerpHprInterval(pivots[wallID], 0.0025, rot))
            self.seq.append(Func(updateCubeMembership, wallID, negRotation))
            print "Added " + ("negative " if negRotation else "") + wallID + " rotation."

        def acceptInput():
            self.accept("s", lambda: addInterval("front"))
            self.accept("shift-s", lambda: addInterval("front", True))
            self.accept("w", lambda: addInterval("back"))
            self.accept("shift-w", lambda: addInterval("back", True))
            self.accept("a", lambda: addInterval("left"))
            self.accept("shift-a", lambda: addInterval("left", True))
            self.accept("d", lambda: addInterval("right"))
            self.accept("shift-d", lambda: addInterval("right", True))
            self.accept("q", lambda: addInterval("bottom"))
            self.accept("shift-q", lambda: addInterval("bottom", True))
            self.accept("e", lambda: addInterval("top"))
            self.accept("shift-e", lambda: addInterval("top", True))
            self.accept("enter", startSequence)

        def ignoreInput():
            self.ignore("f")
            self.ignore("shift-f")
            self.ignore("b")
            self.ignore("shift-b")
            self.ignore("l")
            self.ignore("shift-l")
            self.ignore("r")
            self.ignore("shift-r")
            self.ignore("o")
            self.ignore("shift-o")
            self.ignore("t")
            self.ignore("shift-t")
            self.ignore("enter")

        def startSequence():
            ignoreInput()
            self.seq.append(Func(acceptInput))
            self.seq.start()
            print "Sequence started."
            self.seq = Sequence()

        OnscreenText(text="A: Left Wall Rotation",
                     style=1, fg=(1, 1, 1, 1), pos=(0.06, -0.08),
                     align=TextNode.ALeft, scale=.05,
                     parent=self.a2dTopLeft)
        OnscreenText(text="D: Right Wall Rotation",
                     style=1, fg=(1, 1, 1, 1), pos=(0.06, -0.14),
                     align=TextNode.ALeft, scale=.05,
                     parent=self.a2dTopLeft)
        OnscreenText(text="S: Front Wall Rotation",
                     style=1, fg=(1, 1, 1, 1), pos=(0.06, -0.20),
                     align=TextNode.ALeft, scale=.05,
                     parent=self.a2dTopLeft)
        OnscreenText(text="W: Back Wall Rotation",
                     style=1, fg=(1, 1, 1, 1), pos=(0.06, -0.26),
                     align=TextNode.ALeft, scale=.05,
                     parent=self.a2dTopLeft)
        OnscreenText(text="Q: Bottom Wall Rotation",
                     style=1, fg=(1, 1, 1, 1), pos=(0.06, -0.32),
                     align=TextNode.ALeft, scale=.05,
                     parent=self.a2dTopLeft)
        OnscreenText(text="E: Top Wall Rotation",
                     style=1, fg=(1, 1, 1, 1), pos=(0.06, -0.38),
                     align=TextNode.ALeft, scale=.05,
                     parent=self.a2dTopLeft)
        OnscreenText(text="Shift + Key: Negative Wall Rotation",
                     style=1, fg=(1, 1, 1, 1), pos=(0.06, -0.44),
                     align=TextNode.ALeft, scale=.05,
                     parent=self.a2dTopLeft)
        OnscreenText(text="Middle mouse button: Camera Rotation",
                     style=4, fg=(1, 1, 1, 1), pos=(0.06, -0.56),
                     align=TextNode.ALeft, scale=.06,
                     parent=self.a2dTopLeft)
        OnscreenText(text="Enter: Start Sequence",
                     style=4, fg=(1, 1, 1, 1), pos=(0.06, -0.62),
                     align=TextNode.ALeft, scale=.06,
                     parent=self.a2dTopLeft)

        acceptInput()


app = Rubiks()
app.run()