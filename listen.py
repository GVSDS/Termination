from pynput import keyboard, mouse
from threading import Thread
import time


# 键盘记录
def on_press(key):
    print(key.char if hasattr(key, "char") else key)

# 鼠标记录
def on_click(x, y, button, pressed):
    action = '按下' if pressed else '释放'
    print(f'鼠标{button}在({x}, {y}){action}')

# 启动监听线程
a=Thread(target=lambda: keyboard.Listener(on_press=on_press).start())
b=Thread(target=lambda: mouse.Listener(on_click=on_click).start())



a.start()
b.start()
time.sleep(100000)