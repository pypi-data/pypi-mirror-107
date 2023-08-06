import random
from direct.directbase.DirectStart import base
from direct.showbase.ShowBaseGlobal import globalClock
from direct.task.TaskManagerGlobal import taskMgr
from direct.gui.DirectGui import *
from panda3d.core import *
from NightWind3DLib3.Friend import Friend
from NightWind3DLib3.Player import Player
from NightWind3DLib3.Woodmen import Woodmen
from NightWind3DLib3.Needle import Needle
from NightWind3DLib3.CreateFog import CreatFog


class Window:
    def __init__(self):
        self.base = base
        self.window = WindowProperties()
        self.window.setSize(1400, 1000)
        self.base.win.requestProperties(self.window)
        self.model = loader.loadModel("FieldForest")
        self.minA, self.minB = self.model.getTightBounds()
        self.StartDialog = self.CreateDialog(FrameSize=(-1.4 + 0.01, 1.4 + 0.01,
                                                        -1 + 0.01, 1 + 0.01),
                                             pos=(0, 0, 0), color=(1, 1, 1, 1),
                                             picture="start.png")
        self.font = loader.loadFont("font.ttc")
        self.CreateButton(pos=(0, 0, -0.8), text="开始游戏",
                          scale=0.15, parent=self.StartDialog,
                          command=self.Start, fg=(255 / 255,
                                                  220 / 255, 99 / 255, 1),
                          frameColor=(147 / 255, 88 / 255, 51 / 255, 1))

        # 创建玩家角色
        self.player = Player(ModelName="aduan",
                             AnimsName={"walk": "aduan_walk",
                                        "stand": "aduan_stand"},
                             pos=(-600, -60, 0), ColliderName="player",
                             MaxSpeed=30, MaxHealth=100)

        # 创建营救对象
        self.friend = Friend(ModelName="codemao",
                             AnimsName={"walk": "codemao_walk",
                                        "stand": "codemao_stand"},
                             pos=(450, 20, 0), ColliderName="friend",
                             MaxSpeed=40, MaxHealth=100)

        # 创建木头人敌人
        self.woodmen = []
        self.max_woodmen = 2
        self.spawn_time = 5
        self.spawn_points = [Vec3(0, 210, 0), Vec3(-200, 220, 0), Vec3(-230, -210, 0),
                             Vec3(-80, -190, 0), Vec3(0, -200, 0), Vec3(-150, 20, 0),
                             Vec3(0, -100, 0), Vec3(150, 20, 0)]
        self.dead_woodmen = []
        self.wait_for_death_woodmen = []
        self.dying_woodmen = []
        self.EndDialog = self.CreateDialog(FrameSize=(-1.41, 1.41, -1.01, 1.01),
                                           pos=(0, 0, 0),
                                           color=(1, 1, 1, 1),
                                           picture="win.png")
        self.EndDialog.hide()
        self.CreateButton(pos=(1.1, 0, -0.8),
                          text="退出游戏",
                          scale=0.1,
                          parent=self.EndDialog,
                          command=self.quit,
                          fg=(25/255, 22/255, 99/255, 1),
                          frameColor=(247/255, 188/155, 51/255, 1))
        # self.Fog()

        # 创建地刺敌人
        self.needle = Needle(ModelName="GroundNeedle",
                             AnimsName={"motion": "GroundNeedle_motion",
                                        "stop": "GroundNeedle_stop"},
                             pos=(270, 0, -2), ColliderName="needle",
                             MaxSpeed=5, MaxHealth=100)

        # 添加键盘事件
        self.KeyState = {"up": False, "left": False,
                         "right": False, "shoot": False}
        self.KeyEvent()

        # 创建碰撞体
        self.base.pusher = CollisionHandlerPusher()
        self.base.cTrav = CollisionTraverser()
        self.base.pusher.setHorizontal(True)
        self.base.pusher.add_in_pattern("%fn-into-%in")
        self.base.pusher.addCollider(self.player.collider, self.player.actor)
        self.base.cTrav.addCollider(self.player.collider, self.base.pusher)
        self.base.cTrav.addCollider(self.friend.ice, self.friend.ice_queue)
        self.base.cTrav.addCollider(self.friend.organ, self.friend.organ_queue)
        self.base.cTrav.addCollider(self.friend.safe_house, self.friend.safe_house_queue)

        # 添加列表处理机制
        self.player.ray_queue = CollisionHandlerQueue()
        self.base.cTrav.addCollider(self.player.ray_collision,
                                    self.player.ray_queue)

        # 添加地刺的碰撞处理机制
        self.needle.hue_queue = CollisionHandlerQueue()
        self.base.cTrav.addCollider(self.needle.needle_1, self.needle.hue_queue)
        self.base.cTrav.addCollider(self.needle.needle_2, self.needle.hue_queue)

        self.base.run()

    def CreateDialog(self, FrameSize, pos, color, picture):
        return DirectDialog(frameSize=FrameSize,
                            pos=pos, frameColor=color,
                            frameTexture=picture)

    def CreateButton(self, text, parent, command, scale, pos, fg, frameColor):
        DirectButton(text=text, parent=parent, command=command, scale=scale,
                     pos=pos, text_font=self.font, text_fg=fg,
                     frameColor=frameColor)

    def CreateLifeBar(self, text, text_fg, text_scale, barColor,
                      value, pos, scale, parent):
        return DirectWaitBar(text=text, text_fg=text_fg, text_scale=text_scale,
                             text_font=self.font, barColor=barColor, value=value,
                             pos=pos, scale=scale, parent=parent)

    # 按下按钮触发此事件
    def Start(self):
        # 调整起始位置
        self.StartDialog.hide()
        self.load_model("FieldForest")
        self.base.cam.setHpr(-90, -4, 0)
        self.base.cam.setPos(-1000, -100, 100)
        self.CreateFence(580, 350, 0, 580, -350, 0, 5)
        self.CreateFence(-580, -350, 0, 580, -350, 0, 5)
        self.CreateFence(-580, -350, 0, -580, -150, 0, 5)
        self.CreateFence(-580, -40, 0, -580, 350, 0, 5)
        self.CreateFence(-580, 350, 0, 580, 350, 0, 5)
        self.base.disableMouse()
        self.CreateHealth()
        taskMgr.add(self.update)

    def ChangeKeyState(self, direction, key_state):
        self.KeyState[direction] = key_state

    def KeyEvent(self):
        # 获取键盘事件
        self.base.accept('w', self.ChangeKeyState, ['up', True])
        self.base.accept('w-up', self.ChangeKeyState, ['up', False])
        self.base.accept('a', self.ChangeKeyState, ['left', True])
        self.base.accept('a-up', self.ChangeKeyState, ['left', False])
        self.base.accept('d', self.ChangeKeyState, ['right', True])
        self.base.accept('d-up', self.ChangeKeyState, ['right', False])
        self.base.accept('woodmen-into-fence', self.ChangeWoodmenState)
        self.base.accept("mouse1", self.ChangeKeyState, ["shoot", True])
        self.base.accept("mouse1-up", self.ChangeKeyState, ["shoot", False])
        self.base.accept("woodmen-into-woodmen", self.ChangeWoodmenState)

    def load_model(self, model):
        self.model = loader.loadModel(model)
        self.model.reparentTo(render)
        self.minA, self.minB = self.model.getTightBounds()

    def CreateFence(self, ax, ay, az, bx, by, bz, r):
        solid = CollisionCapsule(ax, ay, az, bx, by, bz, r)
        node = CollisionNode("fence")
        node.addSolid(solid)
        render.attachNewNode(node)
        mask = BitMask32()
        mask.setBit(0)
        mask.setBit(1)
        node.setIntoCollideMask(mask)

    def update(self, task):
        if self.player.health > 0 and self.friend.health > 0:
            dt = globalClock.getDt()

            self.spawn_time -= dt
            if self.spawn_time <= 0:
                self.spawn_time = 2
                self.SpawnWoodmen()
                for woodmen in self.woodmen:
                    self.base.pusher.addCollider(woodmen.collider, woodmen.actor)
                    self.base.cTrav.addCollider(woodmen.collider, self.base.pusher)

            for woodmen in self.woodmen:
                self.player.PlayerMove(self.KeyState, woodmen, dt)
                woodmen.WoodmenMove(self.player, dt, self.friend)

            self.needle.NeedleAttack(self.player, dt)

            for woodmen in self.woodmen:
                self.friend.agency_judgement(self.player, dt, woodmen)

            self.aduan_life_bar["text"] = "生命值:   " + str(self.player.health)
            self.aduan_life_bar["value"] = self.player.health
            self.friend_life_bar["text"] = "生命值:   " + str(self.friend.health)
            self.friend_life_bar["value"] = self.friend.health
            self.woodmen_life_bar["text"] = "生命值:   " + \
                                            str(self.player.trans_woodmen_life)
            self.woodmen_life_bar["value"] = self.player.trans_woodmen_life

            for woodmen in self.woodmen:
                if woodmen.health <= 0:
                    self.dead_woodmen.append(woodmen)
                    self.woodmen.remove(woodmen)

            for dead_woodmen in self.dead_woodmen:
                dead_woodmen.walking = False
                dead_woodmen.collider.removeNode()
                dead_woodmen.actor.disableBlend()
                dead_woodmen.actor.play("die")

            self.dying_woodmen += self.dead_woodmen
            self.dead_woodmen = []

            for dead_woodmen in self.dying_woodmen:
                DeathAnimationControl = dead_woodmen.actor.getAnimControl("die")
                if not DeathAnimationControl.isPlaying():
                    dead_woodmen.CleanUp()
                    self.friend.CountHealth(5)
                    if self.friend.searching_safe_house:
                        self.friend.walk_state = True
                else:
                    self.wait_for_death_woodmen.append(dead_woodmen)

            self.dying_woodmen = self.wait_for_death_woodmen
            self.wait_for_death_woodmen = []

            if self.friend.got_into_house:
                self.EndDialog.show()
                self.health_dialog.hide()

        else:
            self.EndDialog["frameTexture"] = "lose.png"
            self.health_dialog.hide()
            self.EndDialog.show()

        # self.fog.update_fog(self.player.actor.getPos())

        return task.cont

    def ChangeWoodmenState(self, connect):
        for woodmen in self.woodmen:
            if connect.getFromNodePath() == woodmen.collider:
                woodmen.acceleration = -woodmen.acceleration
                woodmen.change_orientation = -woodmen.change_orientation

    def CreateImage(self, image, pos, scale, parent):
        self.imageObject = OnscreenImage(image=image, pos=pos,
                                         scale=scale, parent=parent)
        self.imageObject.setTransparency(True)

    def CreateHealth(self):
        self.health_dialog = self.CreateDialog(FrameSize=(0, 0, 0, 0),
                                               pos=(0, 0, 0),
                                               color=(0, 0, 0, 0),
                                               picture=None)
        self.CreateImage("aduan_life.png", (-1.13, 0, 0.88), (0.24, 1, 0.09),
                         parent=self.health_dialog)
        self.CreateImage("codemao_life.png", (-0.6, 0, 0.88), (0.24, 1, 0.09),
                         parent=self.health_dialog)
        self.CreateImage("woodmen_life.png", (1.1, 0, 0.88), (0.24, 1, 0.09),
                         parent=self.health_dialog)

        self.aduan_life_bar = self.CreateLifeBar(
            text="生命值   :" + str(self.player.health),
            text_fg=(1, 1, 0, 1),
            text_scale=(0.14, 0.14),
            barColor=(1, 48 / 255, 48 / 255, 1),
            value=self.player.health,
            pos=(-1.03, 0, 0.832),
            scale=(0.125, 0, 0.27),
            parent=self.health_dialog
        )

        self.friend_life_bar = self.CreateLifeBar(
            text="生命值   :" + str(self.friend.health),
            text_fg=(1, 1, 0, 1),
            text_scale=(0.14, 0.14),
            barColor=(1, 48 / 255, 48 / 255, 1),
            value=self.friend.health,
            pos=(-0.5, 0, 0.832),
            scale=(0.125, 0, 0.27),
            parent=self.health_dialog
        )

        self.woodmen_life_bar = self.CreateLifeBar(
            text="生命值   :" + str(self.player.trans_woodmen_life),
            text_fg=(0, 178 / 255, 238 / 255, 1),
            text_scale=(0.14, 0.14),
            barColor=(1, 0, 1, 1),
            value=self.player.trans_woodmen_life,
            pos=(1.2, 0, 0.842),
            scale=(0.125, 1, 0.27),
            parent=self.health_dialog
        )

    def SpawnWoodmen(self):
        if len(self.woodmen) < self.max_woodmen:
            spawn_point = random.choice(self.spawn_points)
            woodmen = Woodmen(ModelName="woodmen",
                              AnimsName={"walk": "woodmen_walk",
                                         "stand": "woodmen_stand",
                                         "die": "woodmen_die",
                                         "attack": "woodmen_attack"},
                              pos=spawn_point, ColliderName="woodmen",
                              MaxSpeed=30, MaxHealth=100)
            self.woodmen.append(woodmen)

    def quit(self):
        self.player.CleanUp()
        self.friend.CleanUp()
        self.needle.CleanUp()

        for woodmen in self.woodmen:
            woodmen.CleanUp()

        self.base.userExit()

    def Fog(self):
        pointLight = AmbientLight("ambient light")
        pointLight.setColor((0.2, 0.2, 0.2, 1))
        envLight = render.attachNewNode(pointLight)
        render.setLight(envLight)
        self.fog = CreatFog(self.minA, self.minB)


if __name__ == "__main__":
    Window()
