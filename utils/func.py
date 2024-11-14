import pygame
def experience_needed(level):
    ''' 
        使用多项式公式计算所需经验值
        - level : 宠物等级
        - return : 所需经验值
    '''
    exp = 1.3 * level**2 + 1.41 * level + 10.23
    return int(exp)

def draw_image(surface, image, position,size = (1,1)):
    '''
        用于画图
        - surface : 画布
        - image : 图片
        - position : 图片位置接收一个元组(x,y)
        - size : 图片大小，默认为(1,1)
    '''
    x, y = position
    width, height = image.get_size()
    width, height = width * size[0], height * size[1]
    surface.blit(pygame.transform.scale(image, (width, height)), (x, y))
    

def draw_text(surface, text, position, font = None, color=(0, 0, 0), size=30):
    '''
        用于画文字
        - surface : 画布
        - text : 文字内容
        - position : 文字位置接收一个元组(x,y)
        - color : 文字颜色，默认为黑色
        - size : 文字大小，默认为30
    '''
    font = font if font else pygame.font.Font(
        "static/font/Alibaba-PuHuiTi-Regular.otf", size)
    text_surface = font.render(text, True, color)
    x, y = position
    surface.blit(text_surface, (x, y))
    
if __name__ == "__main__":
    data = list(enumerate([experience_needed(i) for i in range(1, 31)]))
    print(data)