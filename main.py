import pygame
import sys
from all_class import Button, Tooltip, Pet, ProgressBar
from utils import draw_image, draw_text
import random 

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
debug = True
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
    pygame.draw.rect(screen, (255, 255, 255), (panel_x, panel_y, 200, 200), 0, 30)
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
        color="#00FF00",
        title="清洁度",
        font=pygame.font.Font('./static/font/Alibaba-PuHuiTi-Regular.otf', 14)
    )
    
    draw_text(screen, f"状态:{pet.get_status()}", (panel_x+60, panel_y+150), size=14)
    
    # progress_bars["sick"]



while game_loop:
    if index ==65535:
        index = 0
    index += 1
    clock.tick(120) # 设置帧率
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()
    # 事件处理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
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
    pygame.display.update()

pygame.quit()
