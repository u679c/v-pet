import pygame
pygame.init()

class Food():
    def __init__(self, name, nutrition, happiness, health, price, experience, img_fp):
        '''
            - name: 食物名
            - nutrition: 营养值
            - happiness: 幸福值
            - health: 健康值
            - price: 价格
            - experience: 经验值
            - img_fp: 食物图片
        '''
        self.name = name # 食物名
        self.nutrition = nutrition # 营养值
        self.happiness = happiness # 幸福值
        self.health = health # 健康值
        self.experience = experience
        self.price = price # 价格
        self.img = pygame.image.load(img_fp)  # 食物图片
        self.show_items = { # 展示在物品栏里的属性项目
            "营养值": self.nutrition,
            "幸福值": self.experience,
            "健康值": self.health,
            "价格": self.price
        }

    