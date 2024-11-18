import pygame, math, time
import sys
from all_class import Button, Tooltip, Pet, ProgressBar, Food, Item, Stuff, AnimationWipe, Wallet
from utils import draw_image, draw_text
import random
from multiprocessing import Process

pygame.init()
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode(
    (screen_width, screen_height), pygame.DOUBLEBUF)
pygame.display.set_caption("v-pet")
clock = pygame.time.Clock()
font = pygame.font.Font('./static/font/Alibaba-PuHuiTi-Regular.otf', 36)

# 初始化按钮
start_button = Button(300, 400, 200, 60, "开始游戏",
                    font, (0, 128, 0), (0, 255, 0))
quit_button = Button(300, 500, 200, 60, "退出游戏", font, (128, 0, 0), (255, 0, 0))

# 提示类对象列表
tooltips = []   
# 进度条类对象
progress_bars = {}
# pygame加载图片
bg_img = pygame.image.load("static/img/background.png").convert_alpha() 

# 宠物对象
main_pet = Pet("小猫", 300, 150)
main_pet.animation = True
# 游戏主循环
game_loop = True
debug = False
index = 0
if debug:
    start_game = True
    main_pet.move_to((300, 350),30)
else:
    start_game = False



def draw_panel(x,y,pet):
    # 左上角画一个矩形显示面板，圆角
    panel_x = x
    panel_y = y
    pygame.draw.rect(screen, (255, 255, 255), (panel_x, panel_y, 200, 225), 0, 30)
    draw_text(screen, f"{pet.get_name()}(Lv.{pet.level})", (panel_x+55, panel_y+8), size=20)
    
    progress_bars["experience_bar"] = ProgressBar(
        screen, direction=True, text_pos="left",
        position=(panel_x+150, panel_y+50),
        long=60,
        value=int(pet.experience),
        max_value=int(pet.need_exp),
        color= "#008000",
        title="经验值",
        font=pygame.font.Font('./static/font/Alibaba-PuHuiTi-Regular.otf', 14)
    )
    
    progress_bars["happiness_bar"] = ProgressBar(
        screen, direction=True, text_pos="left",
        position=(panel_x+150, panel_y+75),
        long=60,
        value=int(pet.happiness),
        max_value=int(pet.max_happiness),
        color="#FFD700",
        title="幸福值",
        font=pygame.font.Font('./static/font/Alibaba-PuHuiTi-Regular.otf', 14)
    )
    progress_bars["hanger_bar"] = ProgressBar(
        screen, direction=True, text_pos="left",
        position=(panel_x+150, panel_y+100),
        long=60,
        value=int(pet.hunger),
        max_value=int(pet.max_hunger),
        color="#FF2B2B",
        title="饥饿值",
        font=pygame.font.Font('./static/font/Alibaba-PuHuiTi-Regular.otf', 14)
    )
    
    progress_bars["cleanliness_bar"] = ProgressBar(
        screen, direction=True, text_pos="left",
        position=(panel_x+150, panel_y+125),
        long=60,
        value=int(pet.cleanliness),
        max_value=int(100),
        color="#00FFFF",
        title="清洁度",
        font=pygame.font.Font('./static/font/Alibaba-PuHuiTi-Regular.otf', 14)
    )
    progress_bars["health_bar"] = ProgressBar(
        screen, direction=True, text_pos="left",
        position=(panel_x+150, panel_y+150),
        long=60,
        value=int(pet.health),
        max_value=int(100),
        color="#00FF00",
        title="健康值",
        font=pygame.font.Font('./static/font/Alibaba-PuHuiTi-Regular.otf', 14)
    )
    draw_text(screen, f"状态:{pet.get_status()}", (panel_x+60, panel_y+175), size=14)
    
    # progress_bars["sick"]

items = [
    Item(Food("苹果", nutrition=10,
                    happiness=15,
                    health=5,
                    price=10,
                    experience=10,
                    img_fp = "static/img/apple.png"
                )
    ),
    Item(Stuff("药",
                    happiness=10,
                    health=20,
                    price=10,
                    experience=10,
                    img_fp = "static/img/medicine.png"
                    ,audio_fp="static/sounds/pay.mp3")
    ),
    Item(Stuff("肥皂",
                    happiness=10,
                    health=20,
                    price=10,
                    experience=10,
                    cleanliness=30,
                    img_fp = "static/img/soap.png",
                    audio_fp="static/sounds/bubbles.mp3")
    ),
    Item(Stuff("刷子",
                    happiness=10,
                    health=20,
                    price=10,
                    experience=10,
                    cleanliness=30,
                    img_fp = "static/img/brush.png"
                    ,audio_fp="static/sounds/soap.mp3")
    ),
    Item(Stuff("麦克风",
                    happiness=5,
                    health=-2,
                    experience=5,
                    cleanliness=-2,
                    money=20,
                    img_fp="static/img/microphone.png")
    )
]
animations = []
animation_index = 0

wallet = Wallet.load_data("static/img/wallet.png", "static/user_data.json")
wallet_item = Item(wallet)
wallet_item.height = 60

pygame.mixer.music.load("static/sounds/background_music.mp3") 
pygame.mixer.music.play(-1)  # 无限循环播放
pygame.mixer.music.set_volume(0.2)  # 设置音量

def cash_not_enough():
    tooltips.append(Tooltip(
                            f"金币不足", 
                            position=mouse_pos,
                            background_color=(255,0,0,0),
                            display_time=1000,
                            font=pygame.font.Font('./static/font/Alibaba-PuHuiTi-Regular.otf', 14),
                            is_border=False,
                            color="black"
                        ))
    
def show_items_tips(stuff):
    index = 0
    for key, value in stuff.show_items.items():
        if value:
            tooltips.append(Tooltip(
                            f"{key} {'+' if value > 0 else ''}{value}", 
                            position=(mouse_pos[0]-50, mouse_pos[1]+ 10 + (16 * index)),
                            background_color=(255,0,0,0),
                            display_time=1000,
                            font=pygame.font.Font('./static/font/Alibaba-PuHuiTi-Regular.otf', 14),
                            is_border=False,
                            color="black"
                        ))
            index += 1



while game_loop:
    if not main_pet.can_sing:   # 判断唱歌状态是否被打断了
        main_pet.sounds["pet_true_music"].stop()
        main_pet.can_sing = True
        main_pet.is_singing = False
    if index ==65535:
        index = 0
    index += 1
    if animation_index >= math.pi*100:
        animation_index = 0  
    animation_index += 1
    clock.tick(120) # 设置帧率
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()
    # 事件处理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Wallet.save_data(wallet, "static/user_data.json")
            game_loop = False

    # 如果游戏未开始，则显示开始界面
    if not start_game:
        # 显示开始界面
        screen.fill((135, 206, 250))  # 设置背景颜色
        main_pet.draw(screen,False)  # 将图片显示在屏幕中央
        start_button.draw(screen)
        quit_button.draw(screen)
        #  检查鼠标是否悬停在按钮上
        start_button.check_hover(mouse_pos)
        quit_button.check_hover(mouse_pos)
        main_pet.check_hover(mouse_pos)
        
        if start_button.is_clicked(mouse_pos, mouse_click):
            start_game = True  # 开始游戏
            tooltips.append(Tooltip.tips("欢迎使用V-pet", position="top"))
            main_pet.move_to((300, 350),30)
        if quit_button.is_clicked(mouse_pos, mouse_click):
            pygame.quit()
            sys.exit()
    else:
        # 这里放置游戏的主代码
        # TODO 游戏主界面
        
        draw_image(screen,bg_img,(0,0),(0.8,0.6))
        draw_panel(20, 20, main_pet)
        # 画宠物
        main_pet.draw(screen, index)  
        
        # 画钱包
        wallet_item.draw(screen, 240, 30)
        
        # 画物品
        for i in range(len(items)):
            items[i].draw(screen, 650, 50+(Item.height+5)*i)        
            if items[i].is_clicked(mouse_pos, mouse_click):
                if type(items[i].stuff) == Food:
                    if wallet.affordable(items[i].stuff.price):
                        wallet.pay(items[i].stuff.price)
                        main_pet.feed(items[i].stuff)
                        show_items_tips(items[i].stuff)
                        tooltips.append(Tooltip(
                        main_pet.enjoy(), color="black", background_color="white", position=(main_pet.x,  main_pet.y)))
                    else:
                        cash_not_enough()
                if items[i].stuff.name == "药":
                    if wallet.affordable(items[i].stuff.price):
                        wallet.pay(items[i].stuff.price)
                        main_pet.take_medicine(items[i].stuff)
                        show_items_tips(items[i].stuff)
                        tooltips.append(Tooltip(
                        main_pet.take_medicining(), color="black", background_color="white", position=(main_pet.x,  main_pet.y)))
                    else:
                        cash_not_enough()
                if items[i].stuff.name == "肥皂" or items[i].stuff.name == "刷子":
                    if wallet.affordable(items[i].stuff.price):
                        wallet.pay(items[i].stuff.price)
                        main_pet.clean(items[i].stuff)
                        #!TOD0
                        time.sleep(0.2)
                    
                        animations.append(AnimationWipe(300, 400, items[i].stuff.img))
                        items[i].stuff.audio.play()
                        show_items_tips(items[i].stuff)
                        tooltips.append(Tooltip(
                        main_pet.cleaning(), color="black", background_color="white", position=(main_pet.x,  main_pet.y)))
                    else:
                        cash_not_enough()
                if items[i].stuff.name == "麦克风":
                    main_pet.sing()
                    wallet.get(items[i].stuff.money)
                    show_items_tips(items[i].stuff)
                    tooltips.append(Tooltip(
                        main_pet.singing(), color="black", background_color="white", position=(main_pet.x,  main_pet.y)))

        
        if main_pet.is_clicked(mouse_pos, mouse_click):
            # 在鼠标单击处提示经验+0.3
            tooltips.append(Tooltip(
                    "EX + 0.3", 
                    position=mouse_pos,
                    background_color=(0,0,0,0),
                    display_time=1000,
                    font=pygame.font.Font('./static/font/Alibaba-PuHuiTi-Regular.otf', 14),
                    is_border=False,
                    color="black"
                ))
            tooltips.append(Tooltip(
                    "幸福值 +1", 
                    position=(mouse_pos[0],mouse_pos[1]+ 20 ), 
                    background_color=(0, 0, 0, 0),
                    display_time=1000,
                    font= pygame.font.Font('./static/font/Alibaba-PuHuiTi-Regular.otf', 14),
                    is_border=False,
                    color="black"
                ))
            
            tooltips.append(Tooltip(
                main_pet.attention(), color="black", background_color="white", position=(main_pet.x, main_pet.y)))
        
    
    '''
    显示提示
    '''
    if tooltips != []:
        for tooltip in tooltips:
            if not tooltip.is_visible():
                tooltips.remove(tooltip)
            else:
                tooltip.draw(screen)
                
    if progress_bars != {}:
        # 遍历所有值
        for key, value in progress_bars.items():
            value.draw()
    # print("tooltips:", tooltips)
    
    # 显示动画
    if animations:
            for animation in animations:
                animation.draw(screen)
                animation.move(animation_index)
                if animation.is_completed:
                    animations.remove(animation)
                    animation.is_completed = False
    
    pygame.display.update()

pygame.quit()
