import keyboard
import tkinter
from tkinter import *
import tkinter.ttk
import threading
from tkinter.filedialog import (askopenfilename, 
                                    askopenfilenames, 
                                    askdirectory, 
                                    asksaveasfilename)
import tkinter.ttk
import time
global structureNumber

import pynput.mouse as pm
import threading
def on_click(x, y, button, pressed):
    # 监听鼠标点击
    if pressed:
        print("按下坐标")
        keyboard.press_and_release('ctrl+alt+.')
        mxy="{},{}".format(x, y)
        print(mxy)
        print(button)
    if not pressed:
        # Stop listener
        return False
def on_scroll(x, y, dx, dy):
    if dy >0:
        keyboard.press_and_release('ctrl+alt+.')
    else:
        keyboard.press_and_release('ctrl+alt+,')
def thread_recv():
    global structureNumber
    while(structureNumber):
        with pm.Listener(on_click=on_click,
                         on_scroll=on_scroll
                         ) as pmlistener:
            pmlistener.join()
def Start():
    global structureNumber
    structureNumber =True
    recv_data = threading.Thread(target=thread_recv)
    recv_data.start()
    
def Stop():
    global structureNumber
    structureNumber =False
root =Tk()
root.title('NOVAL TEST     v1.0.1')
button =Button(root, text="Start",command=Start,font=('微软雅黑',12),fg='green')
button.place(relx=0.1, rely=0.45, relwidth=0.3, relheight=0.15)

button =Button(root, text="Stop",command=Stop,font=('微软雅黑',12),fg='green')
button.place(relx=0.6, rely=0.45, relwidth=0.3, relheight=0.15)

screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
size = '%dx%d+%d+%d' % (300, 200, (screenwidth - 300) / 2, (screenheight - 200) / 2)
root.geometry(size)
canvas = Canvas(root, width=200, height=100)
canvas.place(x=344,y=266)
root.mainloop()