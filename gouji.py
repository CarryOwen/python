import tkinter
from tkinter import *
import tkinter.ttk
import threading
import keyboard
import pynput.keyboard as pm

from pynput.keyboard import Key,Controller,Listener
from tkinter.filedialog import (askopenfilename, 
                                    askopenfilenames, 
                                    askdirectory, 
                                    asksaveasfilename)
import tkinter.ttk
import time
ying_cnt=6
da_wang=6
xiao_wang=6
card_2=24
card_A=24
card_K=24
card_Q=24
card_J=24
card_10=24
card_9=24
card_8=24   
card_7=24
card_6=24
card_5=24
card_4=24

def on_press(key):
   print("按下",key)

def restart():
    global ying_cnt
    global da_wang
    global xiao_wang
    global card_2
    global card_A
    global card_K
    global card_Q
    global card_J
    global card_1
    global card_10
    ying_cnt=6
    da_wang=6
    xiao_wang=6
    card_2=24
    card_A=24
    card_K=24
    card_Q=24
    card_J=24
    card_10=24
    card_9=24
    card_8=24   
    card_7=24
    card_6=24
    card_5=24
    card_4=24
def on_release(key):
    global ying_cnt
    global da_wang
    global xiao_wang
    global card_2
    global card_A
    global card_K
    global card_Q
    global card_J
    global card_1
    global card_10

    #  记录鹰牌
    if str(key)== r"'\x11'":
         if ying_cnt>0:
            ying_cnt-=1
    #  记录大王
    if str(key)== r"'\x17'":
         if da_wang>0:
            da_wang-=1
    #  记录小王
    if str(key)== r"'\x05'":
         if xiao_wang>0:
            xiao_wang-=1
    # 记录2牌
    if str(key)=="'2'":
         if card_2>0:
            card_2-=1
    if str(key)=="'a'":
         if card_A>0:
            card_A-=1
    if str(key)=="'k'":
         if card_K>0:
            card_K-=1
    if str(key)=="'q'":
         print("Q",card_Q)
         if card_Q>0:
            card_Q-=1
    if str(key)=="'j'":
         if card_J>0:
            card_J-=1
    if str(key)=="'s'":
        if card_10>0:
            card_10-=1
def thread_recv():
    with pm.Listener(on_press=on_press,on_release = on_release
                         ) as pmlistener:
            pmlistener.join()
listhen_thread = threading.Thread(target=thread_recv)
listhen_thread.start()


root =Tk()
root.title('CardRecorder    v1.0.1')
def display():
     while True:
        Label(root, text="鹰:"+str(ying_cnt), font=("黑体", 40, "bold"),relief=RAISED).grid(row=0,column=0,padx=40)
        lab = Label(root, text="大王:"+str(da_wang), font=("黑体", 40, "bold"),relief=RAISED,width=6).grid(row=0, column=1,padx=40)
        lab = Label(root, text="小王:"+str(xiao_wang), font=("黑体", 40, "bold"),relief=RAISED,width=6).grid(row=0, column=2,padx=40)

        lab = Label(root, text="2:"+str(card_2), font=("黑体", 40, "bold"),relief=RAISED,width=6).grid(row=3, column=0,padx=10)
        lab = Label(root, text="A:"+str(card_A), font=("黑体", 40, "bold"),relief=RAISED,width=6).grid(row=3, column=1,padx=10)
        lab = Label(root, text="K:"+str(card_K), font=("黑体", 40, "bold"),relief=RAISED,width=6).grid(row=3, column=2,padx=10,pady=10)

        lab = Label(root, text="Q:"+str(card_Q), font=("黑体", 40, "bold"),relief=RAISED,width=6).grid(row=5, column=0,padx=10,pady=10)
        lab = Label(root, text="J:"+str(card_J), font=("黑体", 40, "bold"),relief=RAISED,width=6).grid(row=5, column=1,padx=10,pady=10)
        lab = Label(root, text="10:"+str(card_10), font=("黑体", 40, "bold"),relief=RAISED,width=6).grid(row=5, column=2,padx=10,pady=10)

        #   lab = Label(root, text=card_A, font=("黑体", 40, "bold")).grid(row=0, column=3)
        #   lab = Label(root, text=card_K, font=("黑体", 40, "bold")).grid(row=0, column=4)width=200,height=90
        #   lab = Label(root, text=card_Q, font=("黑体", 40, "bold")).grid(row=0, column=5)
        #   lab = Label(root, text=card_J, font=("黑体", 40, "bold")).grid(row=0, column=6)
        #   lab = Label(root, text=card_10, font=("黑体", 40, "bold")).grid(row=0, column=7)
        time.sleep(0.1)
display_thread = threading.Thread(target=display)
display_thread.start()
# lab.place(x=500,y=100)
# button =Button(root, text="Start",command=Start,font=('微软雅黑',12),fg='green')
# button.place(relx=0.1, rely=0.45, relwidth=0.3, relheight=0.15)

button =Button(root, text="重新开始",command=restart,font=('微软雅黑',12),fg='green')
button.place(relx=0.3, rely=0.6, relwidth=0.3, relheight=0.15)

screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
size = '%dx%d+%d+%d' % (800, 400, (screenwidth - 300) / 2, (screenheight - 200) / 2)
root.geometry(size)
canvas = Canvas(root, width=200, height=100)
canvas.place(x=344,y=266)
root.mainloop()