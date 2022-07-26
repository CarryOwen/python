import win32gui
import win32api
import win32con
import sys, os
from tkinter import *
from tkinter import ttk
import time
import random
import xlwt
from PIL import Image,ImageTk
global Serial
global batch
global sn
def GotVersion():
    return cmb.get()
def Got_Windows():
    classname = "BartendWindowClass"
    titlename = "BarTender Professional - [demo.btw *]"
    #获取句柄
    hwnd= win32gui.FindWindow(classname, titlename)
    win32gui.SetForegroundWindow(hwnd)


def Got_Tool():
    classname = "TkTopLevel"
    titlename = "SN打印工具     v1.0.1"
    #获取句柄
    hwnd= win32gui.FindWindow(classname, titlename)
    win32gui.SetForegroundWindow(hwnd)

def Gerate_SN(Serial):
    global batch
    this_dir = os.path.split(sys.argv[0])[0] #获取当前路径
    source=os.path.join(this_dir, "source.txt")
    source_backup=os.path.join(this_dir, "backe_file.txt")
    print("patch:",source)
    randomInt=random.randint(0,9)
    f = open(source,'w',encoding='utf-8')
    f_backup = open(source_backup,'a',encoding='utf-8')
    auxiliary=sum([int(i) for i in list(batch)])
    auxiliary1=sum([int(i) for i in list(Serial)])
    print("auxiliary auxiliary1",auxiliary,auxiliary1)
    lrc=sum([int(i) for i in list(batch)]) +sum([int(i) for i in list(Serial)])+randomInt+1
    print("randomInt",randomInt)
    print("lrc:",lrc)
    print("batch:",batch)
    version =GotVersion()
    print("version:",version)
    if version=="单4G版本":
        f.write('demo'+"\r"+"E01"+batch+Serial+str(randomInt)+str(lrc)[-1])
        f_backup.write("E01"+batch+Serial+str(randomInt)+str(lrc)[-1]+'\n')
    else:
        f.write('demo'+"\r"+"https://cloudspeaker.chinaums.com/airkiss.html?sn=E01"+batch+Serial+str(randomInt)+str(lrc)[-1])
        f_backup.write("https://cloudspeaker.chinaums.com/airkiss.html?sn=E01"+batch+Serial+str(randomInt)+str(lrc)[-1]+'\n')
    f.close()
    f_backup.close()
    print(source)

# 返回批次号
def inputBatch_click():
    global batch
    print("返回批次号")
    batch = inputBatch.get()
# 返回流水号
def inputSerial_click():
    global Serial
    print("返回流水号")
    Serial= inputSerial.get()
def inputSNtrue():
    global sn
    print("返回SN")
    sn= inputSN.get()

def PrintSN_click():
    global Serial,sn
    Serial=str(int(Serial)+1).zfill(5)
    print("Serial:",Serial)
    Gerate_SN(Serial)

def Gerate_SNde(Serial):
    global batch
    this_dir = os.path.split(sys.argv[0])[0] #获取当前路径
    source=os.path.join(this_dir, "source.txt")
    print("patch:",source)
    randomInt=random.randint(0,9)
    f = open(source,'w',encoding='utf-8')
    auxiliary=sum([int(i) for i in list(batch)])
    auxiliary1=sum([int(i) for i in list(Serial)])
    print("auxiliary auxiliary1",auxiliary,auxiliary1)
    lrc=sum([int(i) for i in list(batch)]) +sum([int(i) for i in list(Serial)])+randomInt+1
    print("randomInt",randomInt)
    print("lrc:",lrc)
    print("batch:",batch)
    version =GotVersion()
    print("version:",version)
    if version=="单4G版本":
        f.write('demo'+"\r"+"E01"+batch+Serial+str(randomInt)+str(lrc)[-1])
    else:
        f.write('demo'+"\r"+"https://cloudspeaker.chinaums.com/airkiss.html?sn=E01"+batch+Serial+str(randomInt)+str(lrc)[-1])
    f.close()
    print(source)

def AutoprintDe():
    global Serial
    Serial=str(int(Serial)+1).zfill(5)
    print("Serial:",Serial)
    Gerate_SNde(Serial)
    Got_Windows()
    time.sleep(1)
    win32api.keybd_event(17,0,0,0)      # Contrl
    time.sleep(1)
    win32api.keybd_event(80,0,0,0)     # P
    time.sleep(1)
    win32api.keybd_event(80,0,win32con.KEYEVENTF_KEYUP,0)  #释放按键
    time.sleep(1)
    win32api.keybd_event(17,0,win32con.KEYEVENTF_KEYUP,0)
    time.sleep(5)
    win32api.keybd_event(13,0,0,0)     # enter
    time.sleep(1)
    win32api.keybd_event(13,0,win32con.KEYEVENTF_KEYUP,0)
    time.sleep(5)
    Got_Tool()
def PrintTrue():
    global sn
    print("SN:",sn)
    sn=int(sn)
    bar=120/sn
    bar_d=bar
    print("bar:",bar)
    while sn>0:
        PrintSN_click()
        print("Gerate")
        x.set(str(round(bar/1.2,2)) + '%')
        canvas.coords(fill_rec, (5, 5,bar, 55))
        bar=bar+bar_d
        time.sleep(0.2)
        root.update()
        sn=sn-1
    x.set("完成")
def AutoPrint():
    global sn
    print("SN:",sn)
    sn=int(sn)
    bar=120/sn
    bar_d=bar
    while sn>0:
        AutoprintDe()
        print("Gerate")
        x.set(str(round(bar/1.2,2)) + '%')
        canvas.coords(fill_rec, (5, 5,bar, 55))
        time.sleep(5)
        sn=sn-1
    x.set("完成")
root =Tk()
root.title('SN打印工具     v1.0.1')
screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
size = '%dx%d+%d+%d' % (600, 400, (screenwidth - 600) / 2, (screenheight - 400) / 2)
root.geometry(size)
canvas = Canvas(root, width=200, height=44)
canvas.place(x=277,y=366)
this_dir = os.path.split(sys.argv[0])[0] #获取当前路径
source=os.path.join(this_dir, "logo.png")
print("Picture Path:",source)
photoimage = ImageTk.PhotoImage(file=source)
canvas.create_image(0, 0,anchor=NW,image=photoimage)#NW指示图片的摆放位置以左上角坐标为基准，不加则使用图片中心位置坐标为基准

lb1 = Label(root, text='批次(日期):',bg='#d3fbfb',fg='blue',font=('微软雅黑',15))
lb1.place(relx=0.1, rely=0.2, relwidth=0.2, relheight=0.1)
inputBatch=Entry(root)
inputBatch.place(relx=0.3, rely=0.2, relwidth=0.5, relheight=0.1)

lb1 = Label(root, text='起始流水号:',bg='#d3fbfb',fg='blue',font=('微软雅黑',15))
lb1.place(relx=0.1, rely=0.4, relwidth=0.2, relheight=0.1)
inputSerial=Entry(root)
inputSerial.place(relx=0.3, rely=0.4, relwidth=0.5, relheight=0.1)

lb1 = Label(root, text='SN数量 :',bg='#d3fbfb',fg='blue',font=('微软雅黑',15))
lb1.place(relx=0.08, rely=0.6, relwidth=0.2, relheight=0.1)
inputSN=Entry(root)
inputSN.place(relx=0.28, rely=0.6, relwidth=0.2, relheight=0.1)

lb1 = Label(root, text='生成进度:',bg='#d3fbfb',fg='blue',font=('微软雅黑',15))
lb1.place(relx=0.5, rely=0.6, relwidth=0.2, relheight=0.1)
canvas = Canvas(root, width=50, height=22, bg="white")
canvas.place(relx=0.7, rely=0.6, width=120, height=44)

#可变字符串绑定到标签上
x = StringVar()
Label(root,textvariable = x).place(x=555, y=248)
fill_rec = canvas.create_rectangle(5,5,1,50,outline = "",width = 0,fill = "green")

button =Button(root, text="生成txt",command=lambda:[inputBatch_click(),inputSerial_click(),inputSNtrue(),PrintTrue()],font=('微软雅黑',20),fg='black')
button.place(relx=0.2, rely=0.75, relwidth=0.25, relheight=0.15)

button =Button(root, text="自动打印",command=lambda:[inputBatch_click(),inputSerial_click(),inputSNtrue(),AutoPrint()],font=('微软雅黑',20),fg='black')
button.place(relx=0.6, rely=0.75, relwidth=0.25, relheight=0.15)

note =Label(root,text="注意：",font=('微软雅黑',12))
note.place(relx=0, rely=0.9, width=50, relheight=0.1)
note1 =Label(root,text="批次格式为年月日,例:20210708",font=('微软雅黑',10))
note1.place(relx=0.1, rely=0.9, width=194, relheight=0.1)
lb1 = Label(root, text='Author:Ou Yiwen',font=('微软雅黑',8))
lb1.place(relx=0.8, rely=0.9, relwidth=0.2, relheight=0.1)

lb1 = Label(root, text='选择版本:',bg='#d3fbfb',fg='blue',font=('微软雅黑',15))
lb1.place(relx=0.1, rely=0, relwidth=0.2, relheight=0.1)
cmb=ttk.Combobox(root,font=('微软雅黑',15),state= "readonly",justify="center",)
cmb.place(relx=0.3, rely=0, relwidth=0.5, relheight=0.1)
# combostyle = ttk.Style()
# combostyle.theme_create('combostyle', parent='alt',
#                                 settings={'TCombobox':
#                                     {'configure':
#                                         {
                                            # 'foreground': 'black',  # 前景色
                                            # 'selectbackground': 'blue',  # 选择后的背景颜色
                                            # 'fieldbackground': 'white',  # 下拉框颜色
                                            # 'background': 'pink',  # 下拉按钮颜色
#                                         }}}
#                                 )
# combostyle.theme_use('combostyle')
cmb['value'] = ('单4G版本','4G+WIFI版本')
cmb.bind("<<ComboboxSelected>>",GotVersion)


root.mainloop()
