import pandas as pd


class Player():
    """

    如果存在已保存的数据，则直接加载数据并返回，以避免重复初始化。
    否则，使用传入的参数初始化类的成员变量。

    - 参数:
        - name: 用户名称。
        - money: 用户的余额。
        - pet_list: 用户的宠物列表, 默认为空列表

    返回: 无返回值。
    """
    def __init__(self, name, money, pet_list =[]):
        if self.load_data():
            return
        
        self.name = name
        self.money = money
        self.pet_list = pet_list
    def save_data(self, file_path="data/player_data.csv"):
        data = pd.DataFrame({"name": [self.name], "money": [self.money], "pet_list": [",".join(self.pet_list)]})
        data.to_csv(file_path, index=False)
        
    def load_data(self ,file_path="data/player_data.csv"):
        try:
            data = pd.read_csv(file_path)
            row = data.iloc[0]
            self.name = row["name"]
            self.money = row["money"]
            self.pet_list = row["pet_list"].split(",")
            return True
        except Exception as e:
            print("加载用户数据异常:\n"+e)
            return False
        
        
        