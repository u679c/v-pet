import random
import time
import pandas as pd
from .food_class import Food
from utils import EXPN
import pygame
import math
import threading
from utils import breathing_animation


class Pet:
    def __init__(self, name, x, y, size=1):
        """
        初始化宠物属性。

        参数:
        - name: 宠物的名称。

        初始化了宠物的各种状态，包括饥饿度、快乐度、健康状况、等级、经验值、清洁度等，并记录是否生病以及上次互动的时间。
        """
        self.load_img()

        self.name = name
        self.hunger = random.randint(50, 100)     # 饥饿度，0-100，初始随机值
        self.happiness = random.randint(50, 100)  # 快乐度，0-100，初始随机值
        self.health = random.randint(50, 100)     # 健康状况，0-100，初始随机值
        self.level = 1                            # 等级
        self.experience = 0                       # 经验值
        self.cleanliness = 100                    # 清洁度
        self.is_sick = False                      # 是否生病
        self.last_interaction_time = time.time()  # 记录上次互动时间
        self.max_health = 100                     # 最大健康值
        self.max_happiness = 100                  # 最大快乐值
        self.max_hunger = 100                     # 最大饥饿值
        self.need_exp = EXPN(1)                   # 所需经验值
        self.img = self.imgs.get("pet_normal")
        self.x = x
        self.y = y
        self.init_size = size
        self.size = size
        self.size_width = size
        self.size_height = size
        self.width = self.img.get_width() * self.size_width
        self.height = self.img.get_height() * self.size_height
        self.animation = False
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.is_hovered = False
        self.index = 0
        self.happy_reactions = [
            "好开心，谢谢你！",
            "真高兴见到你！",
            "你的抚摸真舒服！",
            "和你在一起真好！",
            "你的关心让我幸福！",
            "每次见你都很开心！",
            "你真好，谢谢！",
            "你的陪伴让我快乐！",
            "喜欢和你一起玩！",
            "你的笑容让我开心！",
            "有你真好，谢谢！",
            "你的支持让我幸福！",
            "每次见面都很愉快！",
            "你的鼓励让我开心！",
            "你的陪伴真温馨！",
            "和你在一起真好！",
            "你的关心真温暖！",
            "你的抚摸真舒服！",
            "喜欢你的陪伴！",
            "你的笑容真美！"
        ]
        self.sick_reactions = [
            "我有点不舒服。",
            "身体好虚弱。",
            "好想休息一下。",
            "感觉不太对劲。",
            "头好痛啊。",
            "肚子不舒服。",
            "没力气玩了。",
            "需要休息一下。",
            "好累，想睡觉。",
            "感觉好疲惫。",
            "不想动了。",
            "需要你的帮助。",
            "好想喝水。",
            "身体好重。",
            "心口好闷。",
            "需要看看医生。",
            "感觉好冷。",
            "需要温暖。",
            "好难受啊。",
            "需要安静。"
        ]
        self.hungry_reactions = [
            "我好饿呀。",
            "想吃东西。",
            "肚子好饿。",
            "给我点吃的吧。",
            "饿得不行了。",
            "好想吃饭。",
            "肚子咕咕叫。",
            "快饿晕了。",
            "需要食物。",
            "好饿，喂我吧。",
            "肚子好空。",
            "饿得难受。",
            "快点喂我。",
            "饿得没力气。",
            "好想吃零食。",
            "肚子好饿哦。",
            "快给我点吃的。",
            "饿得发慌。",
            "好想喝牛奶。",
            "饿得走不动。"
        ]
        self.unhappy_reactions = [
            "陪我玩嘛。",
            "好无聊啊。",
            "想出去玩。",
            "陪我一会儿。",
            "快陪我玩。",
            "不想一个人。",
            "陪我玩会儿。",
            "好想出去。",
            "快陪陪我。",
            "好寂寞啊。",
            "想玩游戏。",
            "陪我玩吧。",
            "好无聊哦。",
            "陪我玩一会儿。",
            "不想待着。",
            "快陪我玩。",
            "好想出去走走。",
            "陪我玩一会儿。",
            "好想出去玩。",
            "陪我玩会儿吧。"
        ]
        self.debounce_delay = 2.4
        self.last_click_time = 0

        # 检查本地文件中是否有数据，如果有则加载数据
        try:
            data = pd.read_csv("data/pet_data.csv")
            self.load_data(data)
            print("已加载本地数据。")
        except FileNotFoundError:
            print("未找到本地数据，使用默认数据。")
            self.save_data()
        except Exception as e:
            print("加载数据时发生错误已重置：", e)
            self.save_data()

    def load_img(self):
        pet_image_size = 0.9
        pet_image = pygame.image.load('static/img/pet.png')
        pet_image = pygame.transform.scale(pet_image, (pet_image.get_width(
        )*pet_image_size, pet_image.get_height()*pet_image_size)).convert_alpha()  # 调整图片大小

        pet_enjoy = pygame.image.load('static/img/pet_enjoy.png')
        pet_enjoy = pygame.transform.scale(pet_enjoy, (pet_enjoy.get_width(
        )*pet_image_size, pet_enjoy.get_height()*pet_image_size)).convert_alpha()

        pet_cute = pygame.image.load('static/img/pet_cute.png')
        pet_cute = pygame.transform.scale(pet_cute, (pet_cute.get_width(
        )*pet_image_size, pet_cute.get_height()*pet_image_size)).convert_alpha()

        pet_dirty = pygame.image.load('static/img/pet_dirty.png')
        pet_dirty = pygame.transform.scale(pet_dirty, (pet_dirty.get_width(
        )*pet_image_size, pet_dirty.get_height()*pet_image_size)).convert_alpha()

        pet_sick = pygame.image.load('static/img/pet_sick.png')
        pet_sick = pygame.transform.scale(pet_sick, (pet_sick.get_width(
        )*pet_image_size, pet_sick.get_height()*pet_image_size)).convert_alpha()

        pet_grievance = pygame.image.load('static/img/pet_grievance.png')
        pet_grievance = pygame.transform.scale(pet_grievance, (pet_grievance.get_width(
        )*pet_image_size, pet_grievance.get_height()*pet_image_size)).convert_alpha()

        self.imgs = {
            "pet_normal": pet_image,
            "pet_enjoy": pet_enjoy,
            "pet_cute": pet_cute,
            "pet_dirty": pet_dirty,
            "pet_sick": pet_sick,
            "pet_grievance": pet_grievance
        }

    def move_to_(self, position, speed):
        tx, ty = position
        while True:
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
            if self.x < tx:
                self.x += speed
            if self.y < ty:
                self.y += speed
            if self.x >= tx and self.y >= ty:
                break
            time.sleep(0.01)  # 控制移动速度，避免CPU占用过高

    def move_to(self, position, ticks=200):
        tx, ty = position
        stretch = math.sqrt((tx - self.x) ** 2 + (ty - self.y) ** 2)
        speed = stretch / ticks
        t = threading.Thread(target=self.move_to_, args=(position, speed))
        t.start()

    def enjoy_(self, ticks):
        index = self.index
        while True:
            if self.index >= index + ticks:
                self.img = self.imgs.get("pet_normal")
                break
            else:
                self.img = self.imgs.get("pet_enjoy")
            time.sleep(0.01)

    def enjoy(self, ticks=200):
        t = threading.Thread(target=self.enjoy_, args=(ticks,))
        t.start()
        # 从happy_reactions中随机选一个返回
        return random.choice(self.happy_reactions)

    def sick(self, ticks=200):
        # 从sick_reactions中随机选一个返回
        return random.choice(self.sick_reactions)
    
    # 日常闲逛
    def walk(self, surface):
        # TODO 会出界 待修复
        # 确保宠物至少有一定偏移量
        x_offset = random.randint(-300, 300)
        y_offset = random.randint(-300, 300)
        new_x = self.x + x_offset
        new_y = self.y + y_offset
        # 检测边界
        if new_x < 0 or new_x > surface.get_width() or new_y < 0 or new_y > surface.get_height():
            return
        self.move_to((new_x, new_y), 40)
        print("闲逛")

    def draw(self, surface, animation=True):
        self.index += 1
        # if self.index % 100 == 0:
        self.check_all()

        self.animation = animation
        if self.animation:
            drawimg = pygame.transform.scale(
                self.img, (self.width*self.size_width, self.height*self.size_height)).convert_alpha()
            surface.blit(
                drawimg, (self.x + (self.width - self.width*self.size_width) // 2,
                          self.y + (self.height - self.height*self.size_height)))
            speed = 30  # 越大呼吸速度越慢
            # 根据index通过改变size创建呼吸动画
            self.size_height = breathing_animation(
                (self.index / speed), W=0.05)
            self.size_width = breathing_animation(
                (self.index / speed) - 15.1, W=0.05)
        else:
            drawimg = pygame.transform.scale(
                self.img, (self.width*self.size_width, self.height*self.size_height)).convert_alpha()
            surface.blit(drawimg, (self.x, self.y))

    def feed(self, food: Food):
        if self.hunger >= self.max_hunger:
            print ("宠物很饱了")
        self.hunger += food.nutrition
        self.happiness += food.happiness
        self.health += food.health
        self.experience += food.experience
        self.check_all()

    def play(self, play_type):
        # 与宠物玩耍，影响快乐度
        if play_type == "fetch":
            self.happiness += 10
            self.experience += 5
        elif play_type == "cuddle":
            self.happiness += 15
            self.experience += 10
        elif play_type == "exercise":
            self.hunger -= 10
            self.health += 10
            self.experience += 15
        elif play_type == "tenjoy":
            self.happiness += 5
            self.experience += 5
        else:
            print("未知玩耍方式！")

        # 限制属性的范围
        self.hunger = max(0, self.hunger)
        self.happiness = min(100, self.happiness)
        self.health = min(100, self.health)
        self.check_level_up()
        self.check_all()

    def clean(self):
        # 清洁宠物
        self.cleanliness = 100
        print(f"{self.name} 已被清洁干净！")
        self.check_all()

    def heal(self):
        # 治疗宠物
        if self.is_sick:
            self.is_sick = False
            self.health += 20
            print(f"{self.name} 已恢复健康！")
        else:
            print(f"{self.name} 不需要治疗。")
        self.check_all()

    def check_level_up(self):
        # 检查并提升等级
        if self.experience >= self.need_exp:
            self.level += 1
            self.experience -= self.need_exp
            self.need_exp = EXPN(self.level)
            print(f"恭喜！{self.name} 升级到等级 {self.level}！")

    def check_all(self):
        # 限制属性的范围
        self.hunger = min(self.hunger, self.max_hunger)
        self.happiness = min(self.happiness, self.max_happiness)
        self.health = min(self.health, self.max_health)

        self.check_level_up()
        self.check_status()
        self.check_if_sick()
        
    last_hunger_decrease_time = 0
    last_happiness_decrease_time = 0
    last_cleanliness_decrease_time = 0

    def check_status(self):
        current_time = time.time()
        time_since_last_interaction = current_time - self.last_interaction_time

        # 计算下次状态值减少的时间
        next_hunger_decrease = 60 - (time_since_last_interaction % 60)
        next_happiness_decrease = 120 - (time_since_last_interaction % 120)
        next_cleanliness_decrease = 180 - (time_since_last_interaction % 180)
        # 饥饿减少防抖
        if int(next_hunger_decrease) == 0 and (current_time - Pet.last_hunger_decrease_time) >= 10:
            self.hunger = max(0, self.hunger - 5)
            Pet.last_hunger_decrease_time = current_time

        # 快乐减少防抖
        if int(next_happiness_decrease) == 0 and (current_time - Pet.last_happiness_decrease_time) >= 10:
            self.happiness = max(0, self.happiness - 10)
            Pet.last_happiness_decrease_time = current_time

        # 清洁度减少防抖
        if int(next_cleanliness_decrease) == 0 and (current_time - Pet.last_cleanliness_decrease_time) >= 10:
            self.cleanliness = max(0, self.cleanliness - 15)
            Pet.last_cleanliness_decrease_time = current_time

    def check_if_sick(self):
        # 根据状态检查宠物是否生病
        if self.cleanliness < 20 or self.hunger < 20:
            self.is_sick = True
            self.img = self.imgs["pet_sick"]
    def get_status(self):
        return "生病" if self.is_sick else "健康"
    def save_data(self):
        data = {
            "name": self.name,
            "level": self.level,
            "hunger": self.hunger,
            "happiness": self.happiness,
            "health": self.health,
            "cleanliness": self.cleanliness,
            "experience": self.experience,
            "is_sick": self.is_sick,
        }
        pd.DataFrame(data, index=[0]).to_csv(
            "./data/pet_data.csv", index=False)

    def load_data(self, data):
        row = data.iloc[0]  # 获取第一行数据
        self.name = row["name"]
        self.level = row["level"]
        self.hunger = row["hunger"]
        self.happiness = row["happiness"]
        self.health = row["health"]
        self.cleanliness = row["cleanliness"]
        self.experience = row["experience"]
        self.is_sick = row["is_sick"]

    def attention(self):
        self.index = 0
        self.width = self.img.get_width() * self.init_size
        self.height = self.img.get_height() * self.init_size
        self.experience += 0.3
        self.happiness += 1
        self.check_all()
        if self.is_sick:
            return self.sick()
        return self.enjoy()

    def check_hover(self, mouse_pos):
        # 检查鼠标是否在按钮上
        if self.rect.collidepoint(mouse_pos):
            if not self.is_hovered:  # 如果光标刚进入按钮区域，改变光标形状
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                self.is_hovered = True
        else:
            if self.is_hovered:  # 如果光标刚离开按钮区域，恢复默认光标
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                self.is_hovered = False

    def is_clicked(self, mouse_pos, mouse_click):
        current_time = time.time()
        if self.rect.collidepoint(mouse_pos) and mouse_click[0]:
            # 检查上次点击时间和当前时间的差值是否大于防抖延迟时间
            if current_time - self.last_click_time > self.debounce_delay:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                self.last_click_time = current_time
                return True
        return False

    def get_name(self):
        if isinstance(self.name, pd.Series) and not self.name.empty:
            return str(self.name.iloc[0])
        else:
            return str(self.name)


if __name__ == "__main__":
    print(111)
