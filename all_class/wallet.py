import random, pygame, json
pygame.init()

class Wallet:
    def __init__(self, img_fp, money=None):
        self.money = money or random.randint(0, 200)
        self.img = pygame.image.load(img_fp)
    
    @staticmethod
    def load_data(img_fp, fp):
        with open(fp, "r", encoding="utf8") as f:
            dict = json.loads(f.read())
        return Wallet(img_fp, dict["money"])
    
    @staticmethod
    def save_data(obj, fp):
        with open(fp, "w", encoding="utf8") as f:
            f.write(json.dumps({"money": obj.money}))
    
    @property
    def show_items(self):
        return {
            "¥":self.show_value
        }
    
    @property
    def show_value(self):
        return self.money if self.money else "0"
        
    def pay(self, money):
        self.money -= money
        
    def get(self, money):
        self.money += money
        
    def affordable(self, money):
        if self.money < money:
            return False
        return True
    