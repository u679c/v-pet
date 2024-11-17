import time
import pygame


class Button:
    '''
        按钮类
        - 参数：
            - x, y: 按钮左上角坐标
            - width, height: 按钮宽高
            - text: 按钮文字
            - font: 按钮文字字体
            - color: 按钮颜色
            - hover_color: 鼠标悬停时的颜色
    '''

    def __init__(self, x, y, width, height, text, font, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
        self.is_hovered = False
        self.debounce_delay = 2
        self.last_click_time = 0

    def draw(self, surface):
        '''
            绘制按钮
            - 参数：
                surface: 绘制目标
        '''
        pygame.draw.rect(surface, self.current_color,
                         self.rect, border_radius=10)
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def check_hover(self, mouse_pos):
        '''
            检查鼠标是否在按钮上，并切换颜色
            - 参数：
                mouse_pos: 鼠标坐标 (x, y)
        '''
        # 检查鼠标是否在按钮上，并切换颜色
        if self.rect.collidepoint(mouse_pos):
            self.current_color = self.hover_color
            if not self.is_hovered:  # 如果光标刚进入按钮区域，改变光标形状
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                self.is_hovered = True
        else:
            self.current_color = self.color
            if self.is_hovered:  # 如果光标刚离开按钮区域，恢复默认光标
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                self.is_hovered = False

    # def is_clicked(self, mouse_pos, mouse_click):
    #     # 检查按钮是否被点击
    #     if self.rect.collidepoint(mouse_pos) and mouse_click[0]:
    #         pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    #     return self.rect.collidepoint(mouse_pos) and mouse_click[0]

    def is_clicked(self, mouse_pos, mouse_click):
        current_time = time.time()
        if self.rect.collidepoint(mouse_pos) and mouse_click[0]:
            # 检查上次点击时间和当前时间的差值是否大于防抖延迟时间
            if current_time - self.last_click_time > self.debounce_delay:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                self.last_click_time = current_time
                return True
        return False

class Tooltip:
    """
    初始化消息框对象。
    - 参数:
        - surface -- 绘制消息框的表面对象。
        - text -- 消息框内显示的文本内容。
        - font -- 文本的字体对象。
        - color -- 文本颜色，默认为白色。
        - background_color -- 消息框背景颜色，默认为黑色。
        - position -- 消息框显示的位置，默认为顶部。
        - display_time -- 消息框显示的持续时间（毫秒），默认为2000毫秒（2秒）。
        - is_border -- 是否显示消息框的边框，默认为True。
    """

    def __init__(self, text, font=None, color=(255, 255, 255), background_color=(0, 0, 0), position="top", display_time=2000, is_border=True):
        self.text = text
        self.font = font or pygame.font.Font( "./static/font/Alibaba-PuHuiTi-Regular.otf", 24)
        self.color = color
        self.background_color = background_color
        self.display_time = display_time  # 显示时间（毫秒）
        self.start_time = int(time.time()*1000)  # 记录开始时间
        self.rect = None
        self.width = None
        self.height = None
        self.fade_alpha = 255  # 初始透明度
        self.position = position
        self.is_border = is_border
        # print("Tooltip created with text:", text)

    @classmethod
    def tips(cls, text, position="top", font=None, display_time=2000):
        return cls(
            text=text,
            position=position,
            font=font or pygame.font.Font(
                "./static/font/Alibaba-PuHuiTi-Regular.otf", 24),
            display_time=display_time,
            background_color="#409EFF",
            color="#C0C4CC"
        )
    @classmethod
    def error(cls, text, position="top", font=None, display_time=2000):
        # 使用类初始化方法创建一个错误信息显示对象
        return cls(
            text=text,
            font=font or pygame.font.Font(
                "./static/font/Alibaba-PuHuiTi-Regular.otf", 24),
            color="#C0C4CC",  # 设置文本颜色为红色
            display_time=display_time,
            background_color="#F56C6C",  # 设置背景颜色为白色
            position=position
        )

    def draw(self, surface):
        '''
            绘制悬浮提示
            - 参数：
                surface: 绘制目标
        '''
        text_surface = self.font.render(self.text, True, self.color)

        if self.position == "center":
            center_x = surface.get_width() // 2
            center_y = surface.get_height() // 2
            self.position = (center_x, center_y)
        elif self.position == "top":
            self.position = (surface.get_width() // 2, 50)
        elif self.position == "top-left":
            self.position = (20 + text_surface.get_width() // 2, 50)
        elif self.position == "top-right":
            self.position = (surface.get_width() - 20 -
                            text_surface.get_width() // 2, 50)
        elif self.position == "bottom":
            self.position = (surface.get_width() // 2, surface.get_height() - 50)
            
        try:
            # 渲染文本
            text_rect = text_surface.get_rect(center=self.position)
        except Exception as e :
            self.text = f"提示框参数不应为“{self.position}”"
            text_surface = self.font.render(self.text, True, self.color)
            self.position = (surface.get_width() - 20 -
                             text_surface.get_width() // 2, 50)
            text_rect = text_surface.get_rect(center=self.position)

        self.width = text_rect.width
        self.height = text_rect.height

        # 计算悬浮框的位置
        tooltip_rect = pygame.Rect(
            text_rect.x - 10, text_rect.y - 10, text_rect.width + 20, text_rect.height + 20)

        # 绘制带圆角的背景
        background_surface = pygame.Surface(tooltip_rect.size, pygame.SRCALPHA)
        background_surface.fill((0, 0, 0, 0))  # 先填充透明


        radius = 10 
        # 圆角半径
        if self.is_border:
            border_width = 2 # 边框宽度
            pygame.draw.rect(background_surface, (0, 0, 0), (0 - border_width, 0 - border_width,
                                                            tooltip_rect.width + border_width * 2, tooltip_rect.height + border_width * 2),
                            width=border_width, border_radius=radius)
        # 绘制圆角矩形
        pygame.draw.rect(background_surface, self.background_color, (0, 0,
                        tooltip_rect.width, tooltip_rect.height), border_radius=radius)
        # 设置透明度
        background_surface.set_alpha(self.fade_alpha)  # 设置透明度
        text_surface.set_alpha(self.fade_alpha)
        surface.blit(background_surface, tooltip_rect.topleft)
        surface.blit(text_surface, text_rect)

        # 更新位置
        self.rect = tooltip_rect


    def is_visible(self):
        
        # 判断悬浮框是否在显示时间内，并处理退出动画
        if self.start_time is None:
            return False
        elapsed_time =  int(time.time()*1000) - self.start_time
        # print(elapsed_time)
        if elapsed_time >= self.display_time:
            # 进入退出动画
            self.fade_alpha -= 10  # 逐渐减少透明度
            if self.fade_alpha <= 0:
                del self
                return False  # 透明度为0时不再可见
        return True

    def show(self, surface):
        self.draw(surface, self.position)
        

class ProgressBar:
    '''
        进度条
        - 参数：
            - surface -- 绘制进度条的表面对象。
            - long -- 进度条的长度，默认为200。
            - tall -- 进度条的高度，默认为20。
            - position -- 进度条的显示位置，默认为屏幕中心。
            - color -- 进度条的填充颜色，默认为白色。
            - bg_color -- 进度条的背景颜色，默认为灰色。
            - value -- 当前进度值，默认为0。
            - max_value -- 进度条的最大值，默认为100。
            - direction -- 进度条的填充方向，默认为True，表示从左到右。
            - text_show -- 是否显示文本，默认为True。
            - text_pos -- 文本显示位置，默认为'left'，可选值为'left'、'center'、'right'。
            - text_color -- 文本颜色，默认为黑色。
            - text_size -- 文本字体大小，默认为14。
            - text_offset -- 文本偏移量，默认为(0, 0)。
            - text_show -- 是否显示文本，默认为True。
            - text_pos -- 文本显示位置，默认为'left'，可选值为'left'、'center'、'right'。
            - text_color -- 文本颜色，默认为黑色。
            - text_size -- 文本字体大小，默认为14。
            - text_offset -- 文本偏移量，默认为(0, 0)。
            - font -- 文本字体，默认为None。
            - title -- 进度条标题，默认为'bar'。
    '''
    def __init__(self, surface, long=200, tall=20, position=None, color=(255, 255, 255),
                 bg_color=(192, 192, 192), value=0, max_value=100, direction=True,
                 text_show=True, text_pos='left', text_color=(0, 0, 0), text_size=20,
                 text_offset=(0, 0), font = None,title="bar"):
        self.surface = surface
        self.long = long
        self.tall = tall
        self.position = position if position else (
            surface.get_width() // 2, surface.get_height() // 2)
        self.color = color
        self.bg_color = bg_color
        self.value = value
        self.max_value = max_value
        self.direction = direction
        self.text_show = text_show
        self.text_pos = text_pos
        self.text_color = text_color
        self.text_size = text_size
        self.text_offset = text_offset
        self.title = title
        self.font = font or pygame.font.SysFont(
            "static/font/Alibaba-PuHuiTi-Regular.otf", self.text_size)
    # 计算返回格式化num
    def format_num(self,num)->str :
        num = int(num)
        if num < 1000 :
            return str(num)
        elif num < 10000 :
            return f"{round(num/1000,1)}K"
        elif num < 1000000 :
            return f"{round(num/10000,1)}W"
        return f"{round(num/1000000,1)}M"
    def draw(self):
        # 计算进度条位置
        x, y = self.position
        if self.direction:  # 水平方向
            rect = pygame.Rect(x - self.long // 2, y -
                               self.tall // 2, self.long, self.tall)
            fill_width = (self.value / self.max_value) * self.long
            fill_rect = pygame.Rect(x - self.long // 2, y - self.tall // 2, fill_width, self.tall)
        else:  # 垂直方向
            rect = pygame.Rect(x - self.tall // 2, y - self.long // 2, self.tall, self.long)
            fill_height = (self.value / self.max_value) * self.long
            fill_rect = pygame.Rect( x - self.tall // 2, y + self.long // 2 - fill_height, self.tall, fill_height)

        # 绘制背景
        pygame.draw.rect(self.surface, self.bg_color, rect)
        # 绘制进度条
        pygame.draw.rect(self.surface, self.color, fill_rect)

        # 绘制文本
        if self.text_show:
            text = f"{self.title}:{self.format_num(self.value)}/{self.format_num(self.max_value)}   "
            text_surface = self.font.render(text, True, self.text_color)
            text_rect = text_surface.get_rect()
            if self.direction:  # 水平方向
                if self.text_pos == 'left':
                    text_rect.midright = (x - self.long // 2 , y)
                elif self.text_pos == 'right':
                    text_rect.midleft = (x + self.long // 2 , y)
                else:  # center
                    text_rect.center = (x, y)
            else:  # 垂直方向
                if self.text_pos == 'left':
                    text_rect.midbottom = (x, y - self.long // 2 )
                elif self.text_pos == 'right':
                    text_rect.midtop = (x, y + self.long // 2 )
                else:  # center
                    text_rect.center = (x, y)
                    

            text_rect.move_ip(*self.text_offset)
            self.surface.blit(text_surface, text_rect)

    def update(self, value):
        self.value = max(0, min(value, self.max_value))  # 确保值在有效范围内
