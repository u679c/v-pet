import pygame

class Stuff():
    def __init__(self, name, happiness=0, health=0, price=0, experience=0, cleanliness=0, money=0, img_fp=None, audio_fp=None):
        '''
            - name: 物品名
            - nutrition: 营养值
            - happiness: 幸福值
            - health: 健康值
            - price: 价格
            - experience: 经验值
            - cleanliness: 清洁值
        '''
        self.name = name # 物品名
        self.happiness = happiness # 幸福值
        self.health = health # 健康值
        self.experience = experience
        self.price = price # 价格
        self.cleanliness = cleanliness # 清洁值
        self.money = money
        self.img = pygame.image.load(img_fp)  # 图片
        self.audio = pygame.mixer.Sound(audio_fp) if audio_fp else None
        self.show_items = {
            "幸福值":self.happiness,
            "健康值":self.health,
            "经验值":self.experience,
            "清洁值":self.cleanliness,
            "收益值":self.money,
        }