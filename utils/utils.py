import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider



# 定义计算 y 的函数
def breathing_animation(x, k=0.3, t=6, n=1,T=6,W = 0.1):
    x = x % T
    y = ((0.5 * np.sin((np.pi / (k * t)) * ((x - k * t / 2) - (n - 1) * t)) + 0.5) *
         ((x >= (n - 1) * t) & (x < (n - (1 - k)) * t)) +
         ((0.5 * np.sin((np.pi / ((1 - k) * t)) * ((x - (3 - k) * t / 2) - (n - 1) * t)) + 0.5) ** 2) *
         ((x >= (n - (1 - k)) * t) & (x < n * t))) * W
    return y+1

if __name__ == '__main__':

    # 初始化参数
    x = np.arange(0, 20, 0.0001)
    y = breathing_animation(x)

    # 创建图形
    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.25)  # 为滑块留出空间

    # 初始 a 值
    a = 17
    x1 = np.arange(0, 20, 0.0001)
    y1 = breathing_animation(x1 - a)

    # 绘制初始曲线
    line1, = plt.plot(x1, y1, label='Shifted')
    line2, = plt.plot(x, y, label='Original')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('breathing_animation')
    plt.grid(True)
    plt.legend()

    # 创建滑块
    ax_a = plt.axes([0.25, 0.1, 0.65, 0.03])
    slider_a = Slider(ax_a, 'a', valmin=0, valmax=30, valinit=a)
    W = 0.2
    ax_W = plt.axes([0.25, 0.15, 0.65, 0.03])
    slider_W = Slider(ax_W, 'W', valmin=0, valmax=1, valinit=W)
    # 更新函数


    def update(val):
        a = slider_a.val
        w = slider_W.val
        y1 = breathing_animation(x1 - a,W=w)
        line1.set_ydata(y1)
        fig.canvas.draw_idle()


    # 绑定滑块到更新函数
    slider_a.on_changed(update)
    slider_W.on_changed(update)
    plt.show()
