# v-pet虚拟宠物游戏

这是一个简单的宠物照顾游戏，你可以在这个游戏中照顾你的虚拟宠物，喂食、给药、清洁等等。

## 前提条件

- 在您的系统上安装了Python 3.8或更高版本。
- 已安装`pip`包管理器。

## 设置


2. **创建虚拟环境**

   推荐使用虚拟环境来管理依赖项。运行：

   ```bash
   python -m venv .venv
   ```

3. **激活虚拟环境**

   - 在Windows上：
     ```bash
     .\.venv\Scripts\activate
     ```
   - 在macOS和Linux上：
     ```bash
     source .venv/bin/activate
     ```

4. **安装依赖**

   激活虚拟环境后，安装所需的依赖项：

   ```bash
   pip install -r requirements.txt
   ```

5. **运行游戏**

   安装完所有依赖项后，您可以运行游戏：

   ```bash
   python main.py
   ```

现在您应该能够看到并开始玩这个虚拟宠物游戏了！如果您遇到任何问题，请检查上述步骤是否正确执行，并确保所有依赖项都已成功安装。

## 目录
```
.
├── README.md
├── all_class # 各种类
│   ├── __init__.py
│   ├── __pycache__
│   ├── animation_class.py
│   ├── food_class.py
│   ├── pet_class.py
│   ├── player_class.py
│   ├── stuff_class.py
│   ├── tool_class.py
│   └── wallet.py
├── data # 保存的数据
│   ├── pet_data.csv
│   └── player_data.csv
├── main.py # 程序入口
├── requirements.txt # 依赖
├── static # 静态资源
│   ├── font
│   │   ├── Alibaba-PuHuiTi-Regular.otf
│   │   ├── 方正像素12.TTF
│   │   └── 经典行楷简.TTF
│   ├── img
│   │   ├── apple.png
│   │   ├── background.png
│   │   ├── brush.png
│   │   ├── bubbles.png
│   │   ├── medicine.png
│   │   ├── microphone.png
│   │   ├── pet.png
│   │   ├── pet_cute.png
│   │   ├── pet_dirty.png
│   │   ├── pet_enjoy.png
│   │   ├── pet_grievance.png
│   │   ├── pet_sick.png
│   │   ├── sad.png
│   │   ├── soap.png
│   │   └── wallet.png
│   ├── sounds
│   │   ├── background_music.mp3
│   │   ├── bubbles.mp3
│   │   ├── eat.mp3
│   │   ├── get_money.mp3
│   │   ├── pay.mp3
│   │   ├── soap.mp3
│   │   └── true_music.mp3
│   └── user_data.json
└── utils # 工具包
    ├── __init__.py
    ├── __pycache__
    ├── func.py
    └── utils.py
```

## 作者
[u679c](https://github.com/u679c)（点击打开github个人主页）