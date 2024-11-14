import pandas as pd


class Player():
    def __init__(self, name, money, pet_list):
        if self.load_data():
            return
        
        self.name = name
        self.money = money
        self.pet_list = pet_list

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
        
        
        