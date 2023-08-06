from panda3d.core import *


class CreatFog:
    def __init__(self, mina, minb):
        self.mina = mina
        self.minb = minb
        disVec = self.minb - self.mina
        center = (self.mina + self.minb) * 0.5
        self.veilColor = (0, 0, 0, 0.8)
        imgSize = 128
        self.img = PNMImage(imgSize, imgSize, 4)
        self.tex = Texture()
        # 创建纹理卡片
        cd = CardMaker('square')
        cd.setFrame(self.mina.x, self.minb.x, self.mina.y, self.minb.y)
        cd.setColor(1, 1, 1, 1)
        card = cd.generate()
        self.spuare = render.attachNewNode(card)
        self.spuare.setTransparency(True)
        self.spuare.setP(-90)
        self.spuare.setPos(0, 0, 320)
        # 设置画笔
        brush = PNMBrush.makeSpot((0, 0, 0, 1), 3, True)
        self.painter = PNMPainter(self.img)
        self.painter.setPen(brush)
        # 创建纹理层
        veilTS = TextureStage('')
        self.spuare.setTexture(veilTS, self.tex)
        self.spuare.setTexGen(veilTS, RenderAttrib.MWorldPosition)
        self.spuare.setTexScale(veilTS, (1 / disVec[0], 1 / disVec[1]))
        self.spuare.setTexOffset(
            veilTS, -0.5 + center[0] / disVec[0], -0.5 - center[1] / disVec[1])

    def update_fog(self, pos):
        self.pos = pos.xy - self.mina.xy
        self.pos.x /= self.minb.x - self.mina.x
        self.pos.y /= self.minb.y - self.mina.y
        self.painter.drawPoint(
            self.pos.x * self.img.getXSize(), (1 - self.pos.y) * self.img.getYSize())
        self.tex.load(~self.img * self.veilColor)
