from direct.gui.DirectGui import *
from panda3d.core import *
from NightWind3DLib3.Actor import LoadActor


class Friend(LoadActor):
    def __init__(self, ModelName, AnimsName, pos, ColliderName, MaxSpeed, MaxHealth):
        # 初始化营救对象类
        super().__init__(ModelName, AnimsName, pos, ColliderName, MaxSpeed, MaxHealth)

        # 设置初始数据
        self.actor.setScale(0.6)

        # 添加冰封效果
        self.ice_solid = CollisionBox((0, 0, 60), 45, 40, 80)
        self.ice_node = CollisionNode("codemao")
        self.ice_node.addSolid(self.ice_solid)
        self.ice = self.actor.attachNewNode(self.ice_node)
        self.ice.show()

        mask = BitMask32()
        mask.setBit(2)
        self.ice_node.setFromCollideMask(mask)

        # 设置机关
        organ_solid = CollisionSphere(0, 0, 0, 20)
        organ_node = CollisionNode("organ")
        organ_node.addSolid(organ_solid)
        self.organ = render.attachNewNode(organ_node)
        self.organ.setPos(480, -200, 0)
        mask = BitMask32()
        organ_node.setIntoCollideMask(mask)
        self.CreateOrganTitle()
        self.CreateSafeHouse()

        # 为冰封效果添加碰撞体
        self.ice_queue = CollisionHandlerQueue()
        mask = BitMask32()
        self.collider.node().setIntoCollideMask(mask)
        self.collider.node().setFromCollideMask(mask)

        # 为机关添加碰撞处理机制
        self.organ_queue = CollisionHandlerQueue()

        # 其他属性
        self.organ_state = False
        self.delay_time = 0
        self.talk_time = 0
        self.walk_time = 2
        self.walk_state = False
        self.got_into_house = False
        self.organ_crack_state = False
        self.health = 20
        self.text = "恭喜你打开机关！\n是否让 codemao 逃向安全屋？"
        self.ChooseDialog = YesNoDialog(
            text=self.text,
            text_fg=(210 / 255, 91 / 255, 69 / 255, 1),
            text_scale=0.06,
            pos=(0, 0, 0),
            command=self.ChooseCommand,
            frameColor=(178 / 255, 200 / 255, 217 / 255, 1),
            text_font=loader.loadFont("font.ttc")
        )
        self.ChooseDialog.hide()
        self.direction = Vec2(0, -1)
        self.choose_dialog_state = False
        self.searching_safe_house = False

    def CreateOrganTitle(self):
        self.title_dialog = DirectDialog(
            frameSize=(-1.41, 1.41, -1.01, -0.7),
            pos=(0, 0, 0),
            color=(0.2, 0.2, 0.2, 1)
        )
        self.title_dialog["text_font"] = loader.loadFont("font.ttc")
        self.title_dialog["text_pos"] = (-1.3, -0.8)
        self.title_dialog["text"] = "请输入计算结果：2csc30°sin15°cos15°"
        self.title_dialog["text_fg"] = (255 / 255, 220 / 255, 99 / 255, 1)
        self.input_box = DirectEntry(scale=0.05, command=self.judge_result,
                                     pos=(0.1, 0, -0.91), parent=self.title_dialog)

        self.prompt_dialog = DirectDialog(
            frameSize=(0, 0.6, 0, 0.1),
            pos=(0.65, 0, -0.95),
            color=(0.7, 0.9, 1, 1)
        )
        self.prompt_dialog["text_font"] = loader.loadFont("font.ttc")
        self.prompt_dialog["text_pos"] = (0.06, 0.03)
        self.prompt_dialog["text"] = "按下Enter提交答案"
        self.prompt_dialog["text_fg"] = (25 / 255, 164 / 255, 236 / 255, 1)
        self.title_dialog.hide()
        self.prompt_dialog.hide()

    def judge_result(self, result):
        self.organ.hide()
        self.organ_state = False
        if result == str(1):
            self.ice.hide()
            self.prompt_dialog["text"] = "机关已打开！"
            self.delay_time = 1
            self.organ_crack_state = True
            self.ChooseDialog.show()
            self.choose_dialog_state = True
        else:
            self.prompt_dialog["text"] = "密令输入错误！"
            self.delay_time = 1

    def agency_judgement(self, player, dt, woodmen):
        woodmen.organ_crack_state = self.organ_crack_state
        if self.ice_queue.getNumEntries() > 0:
            self.ice_queue.sortEntries()
            if self.ice_queue.getEntry(0).getIntoNodePath() == player.collider:
                self.talk_time += dt
                if self.talk_time > 1:
                    self.organ.show()
                    self.organ_state = True
                    self.talk_time = 0

        if self.organ_queue.getNumEntries() > 0 and self.organ_state:
            self.organ_queue.sortEntries()
            if self.organ_queue.getEntry(0).getIntoNodePath() == player.collider:
                self.title_dialog.show()
                self.prompt_dialog.show()

        if self.delay_time >= 0:
            self.delay_time -= dt
            if self.delay_time <= 0:
                self.title_dialog.hide()
                self.prompt_dialog.hide()

        if self.safe_house_queue.getNumEntries() > 0:
            self.safe_house_queue.sortEntries()
            if self.safe_house_queue.getEntry(0).getIntoNodePath() == self.collider:
                self.walk_time -= dt
                if self.walk_time < 0:
                    self.walk_state = False

            if self.safe_house_queue.getEntry(0).getIntoNodePath() == self.collider and \
                    self.safe_house_queue.getEntry(1).getIntoNodePath() == player.collider:
                self.got_into_house = True

        if self.choose_dialog_state and self.health >= 80:
            self.choose_dialog_state = False
            self.safe_house.show()

        if self.walk_state:
            self.move(dt)
            self.velocity = self.safe_vevtor * 400 * dt
            walking_control = self.actor.getAnimControl("walk")
            if not walking_control.isPlaying():
                self.actor.loop("walk")

        else:
            standControl = self.actor.getAnimControl("walk")
            if not standControl.isPlaying():
                self.actor.loop("stand")

    def CreateSafeHouse(self):
        safe_house_solid = CollisionSphere(0, 0, 0, 55)
        safe_house_node = CollisionNode("safe_house")
        safe_house_node.addSolid(safe_house_solid)
        self.safe_house = render.attachNewNode(safe_house_node)
        self.safe_house.setPos(-620, -100, 0)
        mask = BitMask32()
        safe_house_node.setIntoCollideMask(mask)
        self.safe_house_queue = CollisionHandlerQueue()

    def ChooseCommand(self, choose):
        if choose:
            self.safe_vevtor = self.safe_house.getPos() - self.actor.getPos()
            codemao_safe_vevtor = self.safe_vevtor.getXy()
            heading = self.direction.signedAngleDeg(codemao_safe_vevtor)
            self.actor.setH(heading)
            mask = BitMask32()
            mask.setBit(5)
            self.collider.node().setIntoCollideMask(mask)
            self.ChooseDialog.hide()
            self.walk_state = True
            self.searching_safe_house = True

        else:
            self.ChooseDialog.hide()
            self.ice.show()
            self.safe_house.hide()
