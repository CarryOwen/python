
from tkinter import *
from tkinter import ttk
import time
import threading
import serial
import serial.tools.list_ports
import inspect
import  sys,os
import datetime
from PIL import Image,ImageTk
import csv
import ctypes
from decimal import Decimal
import matplotlib.pyplot as plt
import pandas as pd
global serial_com
global ser
port_serial = " "
bitrate_serial = " "
temperature = [
[-40,210.5283,202.2693,194.3148],
[-39,198.7519,191.0637,183.6545],
[-38,187.7137,180.5546,173.6511],
[-37,177.3629,170.6944,164.2601],
[-36,167.6522,161.4387,155.44],
[-35,158.5379,152.7468,147.1525],
[-34,149.9798,144.5807,139.362],
[-33,141.9402,136.9052,132.0356],
[-32,134.3847,129.6879,125.1427],
[-31,127.2809,122.8985,118.655],
[-30,120.5991,116.5089,112.5462],
[-29,114.3116,110.4932,106.7917],
[-28,108.3927,104.8272,101.3688],
[-27,102.8185,99.4883,96.2564],
[-26,97.5669,94.4558,91.4348],
[-25,92.6171,89.7101,86.8857],
[-24,87.9501,85.2332,82.592],
[-23,83.5479,81.0082,78.5378],
[-22,79.394,77.0194,74.7084],
[-21,75.4728,73.2523,71.0899],
[-20,71.77,69.6931,67.6695],
[-19,68.272,66.3291,64.4351],
[-18,64.9663,63.1485,61.3754],
[-17,61.8412,60.1402,58.4802],
[-16,58.8858,57.2939,55.7394],
[-15,56.0899,54.5998,53.144],
[-14,53.4439,52.049,50.6855],
[-13,50.9389,49.633,48.3557],
[-12,48.5666,47.3439,46.1473],
[-11,46.3192,45.1743,44.0532],
[-10,44.1895,43.1172,42.0668],
[-9,42.1705,41.1663,40.182],
[-8,40.2558,39.3153,38.393],
[-7,38.4396,37.5587,36.6943],
[-6,36.7162,35.891,35.081],
[-5,35.0802,34.3074,33.548],
[-4,33.5269,32.8029,32.0914],
[-3,32.0515,31.3734,30.7065],
[-2,30.6497,30.0145,29.3896],
[-1,29.3174,28.7225,28.1368],
[0,28.0508,27.4936,26.9448],
[1,26.8464,26.3245,25.8102],
[2,25.7006,25.2119,24.73],
[3,24.6103,24.1527,23.701],
[4,23.5726,23.1442,22.7213],
[5,22.5846,22.1835,21.7874],
[6,21.6436,21.2682,20.8973],
[7,20.7472,20.3959,20.0486],
[8,19.8931,19.5644,19.2392],
[9,19.0789,18.7714,18.467],
[10,18.3027,18.0151,17.7303],
[11,17.5624,17.2935,17.027],
[12,16.8561,16.6048,16.3556],
[13,16.1823,15.9475,15.7145],
[14,15.5391,15.3198,15.102],
[15,14.9251,14.7203,14.5168],
[16,14.3387,14.1475,13.9576],
[17,13.7786,13.6003,13.4229],
[18,13.2434,13.0772,12.9117],
[19,12.732,12.5771,12.4228],
[20,12.2431,12.0988,11.955],
[21,11.7756,11.6413,11.5074],
[22,11.3286,11.2037,11.079],
[23,10.9009,10.7848,10.6689],
[24,10.4917,10.3839,10.2762],
[25,10.1,10,9.9],
[26,9.7323,9.6324,9.5325],
[27,9.38,9.2802,9.1806],
[28,9.0424,8.9428,8.8435],
[29,8.7186,8.6195,8.5206],
[30,8.4082,8.3096,8.2113],
[31,8.1105,8.0124,7.9147],
[32,7.8249,7.7275,7.6305],
[33,7.5508,7.4541,7.3579],
[34,7.2878,7.1919,7.0965],
[35,7.0353,6.9403,6.8458],
[36,6.7929,6.6987,6.6052],
[37,6.5601,6.4669,6.3744],
[38,6.3364,6.2442,6.1527],
[39,6.1216,6.0304,5.94],
[40,5.9151,5.825,5.7357],
[41,5.7167,5.6276,5.5394],
[42,5.5259,5.438,5.3509],
[43,5.3425,5.2557,5.1698],
[44,5.1661,5.0804,4.9957],
[45,4.9964,4.9119,4.8283],
[46,4.8331,4.7498,4.6674],
[47,4.6761,4.5939,4.5127],
[48,4.5249,4.4439,4.3639],
[49,4.3793,4.2995,4.2207],
[50,4.2392,4.1605,4.083],
[51,4.1042,4.0268,3.9504],
[52,3.9742,3.898,3.8228],
[53,3.849,3.7739,3.7],
[54,3.7283,3.6544,3.5817],
[55,3.6121,3.5393,3.4677],
[56,3.5,3.4284,3.358],
[57,3.3919,3.3215,3.2523],
[58,3.2877,3.2185,3.1504],
[59,3.1872,3.1191,3.0522],
[60,3.0903,3.0234,2.9575],
[61,2.9968,2.931,2.8663],
[62,2.9066,2.8419,2.7783],
[63,2.8196,2.7559,2.6934],
[64,2.7355,2.6729,2.6115],
[65,2.6544,2.5929,2.5325],
[66,2.5761,2.5156,2.4563],
[67,2.5004,2.441,2.3827],
[68,2.4274,2.369,2.3117],
[69,2.3568,2.2994,2.2432],
[70,2.2886,2.2322,2.177],
[71,2.2227,2.1673,2.1131],
[72,2.159,2.1046,2.0513],
[73,2.0974,2.044,1.9917],
[74,2.0379,1.9854,1.934],
[75,1.9804,1.9288,1.8783],
[76,1.9247,1.874,1.8245],
[77,1.8709,1.8211,1.7725],
[78,1.8188,1.7699,1.7221],
[79,1.7685,1.7204,1.6735],
[80,1.7197,1.6725,1.6264],
[81,1.6725,1.6262,1.5809],
[82,1.6269,1.5813,1.5369],
[83,1.5827,1.5379,1.4943],
[84,1.5399,1.4959,1.4531],
[85,1.4984,1.4553,1.4132],
[86,1.4583,1.4159,1.3746],
[87,1.4194,1.3778,1.3372],
[88,1.3817,1.3408,1.301],
[89,1.3452,1.3051,1.266],
[90,1.3099,1.2704,1.232],
[91,1.2756,1.2368,1.1991],
[92,1.2424,1.2043,1.1673],
[93,1.2102,1.1728,1.1364],
[94,1.1789,1.1422,1.1065],
[95,1.1487,1.1126,1.0775],
[96,1.1193,1.0839,1.0494],
[97,1.0908,1.056,1.0222],
[98,1.0632,1.029,0.9958],
[99,1.0364,1.0028,0.9702],
[100,1.0104,0.9774,0.9453]
]
def findTemperature(var):
    varLen=0
    length=len(temperature)
    # print("varLen:",varLen)
    # print("length:",length)
    print("var:",var)
    while varLen<length:
        # 如果值为1.08
        if var < temperature[varLen][1] and var > temperature[varLen][3]:
            # print("temperature[varLen][1] :",temperature[varLen][1] )
            if var < temperature[varLen+1][1]:
                # 找到更接近参考值的温度
                if abs(var - temperature[varLen][2] )< abs(var - temperature[varLen+1][2]) :
                    # print("Got temperature:",temperature[varLen][0])
                    return temperature[varLen][0]
                else:
                    # print("Got temperature:",temperature[varLen+1][0])
                    return temperature[varLen+1][0]
            else:
                # print("Got temperature:",temperature[varLen][0])
                return temperature[varLen][0]
            break
        # 如果不在已知区间，取中间值
        if var > temperature[varLen+1][1]: 
            # print("Got temperature:",(temperature[varLen+1][0]+temperature[varLen][0])/2)
            return (temperature[varLen+1][0]+temperature[varLen][0])/2
            break
        else: 
            varLen=varLen+1
def encryptWindow():
    top=Toplevel()
    top.title("结果")

    # 居中
    screenwidth = top.winfo_screenwidth()
    screenheight = top.winfo_screenheight()
    size = '%dx%d+%d+%d' % (200, 50, (screenwidth - 200) / 2, (screenheight - 80) / 2)
    top.geometry(size)
    s1 = Scrollbar(top,orient=VERTICAL)
    # encryptWord=Text(top,width=14,height=2,yscrollcommand=s1.set,wrap=WORD,font=("宋体",14))
    encryptWord = Label(top,text="SIM卡数据获取成功！",height=2)
    encryptWord.pack()
    # encryptWord.insert("insert","SIM卡数据获取成功！")
    top.after(1500, top.destroy)

def strTobytes(data:str):
    byte=bytes.fromhex(data)
    return byte
def bytesTostr(data:bytes):
    string=data.hex()
    return string
"""
串口数据接受线程
"""
def thread_recv():
    global ser
    global text1
    global sendT
    IISOTIMEFORMAT = '%m/%d %H:%M:%S'
    while True:
        read  = ser.read(100)
        read=bytesTostr(read)
        print("len:",len(read))
        if len(read) > 5:
            if read[2:6]=="010a":
                print("read:",int(read[0:2],16))
                text1.insert(END,read)
                text1.insert(END,b'\n')
            theTime = datetime.datetime.now().strftime(IISOTIMEFORMAT)
            f = open('SIM_Card_Data.csv','a',encoding='utf-8',newline='')
            csv_writer = csv.writer(f)
            csv_writer.writerow([int(read[0:2],16),theTime])
            f.close()
        if sendT:
            break
        #     # A01202111150000622
        #     if read[:8]==b"deviceSn":
        #         f = open('SIM_Card_Data.csv','a',encoding='utf-8')
        #         csv_writer = csv.writer(f)
        #         csv_writer.writerow([read.decode()])
        #         # print("test",read[46:66].decode())
        #         f.close()
        #         encryptWindow()
def thread_send():
    global ser
    global sendT 
    global circuit
    circuit=1
    IISOTIMEFORMAT = '%H:%M:%S'
    addr=0x19
    cell_H=0
    temperature_H=0
    current_H=0
    sumVoltage=0
    TR=0
    f1 = open('Volt.csv','a',encoding='utf-8',newline='')
    csv_writer = csv.writer(f1)
    csv_writer.writerow(["Volt(mv)","Time"])
    f1.close()
    f1 = open('Volt_Cells.csv','a',encoding='utf-8',newline='')
    csv_writer = csv.writer(f1)
    csv_writer.writerow(["0x4f","0x51","0x53","0x55","0x57","0x59","0x5b","0x5d","0x5f","0x61","0x63","0x65","0x67","0x69","Time"])
    f1.close()
    
    #用来存储各个电芯数据
    list_save=[]
    while True:
        print("addr:0x%02x" % addr)
        ser.write(b'\x35'+bytes([addr])+b'\x01')
        time.sleep(0.05)
        read  = ser.read(100)
        read=bytesTostr(read)
        # print("read:",read)
        if len(read) > 5:
            if read[2:6]=="010a":
                if addr==0x4f or addr==0x51 or addr==0x53 or addr==0x53 or addr==0x55 or addr==0x57 or addr==0x59 or addr==0x5b or addr==0x5d or addr==0x5f or addr==0x61 or addr==0x63 or addr==0x65 or addr==0x67 or addr==0x69:
                    cell_L=int(read[0:2],16)
                    cell_H=cell_H<<8
                    print("cell_L+cell_H: %02x"%(cell_L+cell_H))
                    volt=(cell_L+cell_H)*5/32
                    #去掉小数点
                    volt=volt/1000
                    volt=Decimal(volt).quantize(Decimal("0.00"))
                    sumVoltage=volt+sumVoltage
                    #输出到text区域
                    text1.insert(END,"Cells Address:")
                    text1.insert(END,hex(addr))
                    text1.insert(END," Value:")
                    text1.insert(END,volt)
                    text1.insert(END,b'\n')
                    if volt<2 or volt>5 :
                        addr=0x4d
                        list_save.clear()
                        cell_L=0
                        cell_H=0
                        print("We may get error data")
                    else:
                        list_save.append(volt)
                        if addr==0x69:
                            # save the cells volt
                            theTime = datetime.datetime.now().strftime(IISOTIMEFORMAT)
                            list_save.append(theTime)
                            ff = open('Volt_Cells.csv','a',encoding='utf-8',newline='')
                            csv_writer = csv.writer(ff)
                            csv_writer.writerow(list_save)
                            list_save.clear()
                            ff.close()
                            #save the sumVoltage
                            print("sumVoltage:",sumVoltage)
                            theTime = datetime.datetime.now().strftime(IISOTIMEFORMAT)
                            f = open('Volt.csv','a',encoding='utf-8',newline='')
                            csv_writer = csv.writer(f)
                            csv_writer.writerow([sumVoltage,theTime])
                            f.close()
                            sumVoltage=0
                elif addr==0x19:
                    TR=int(read[0:2],16)&0x3f  #取低7位
                    #输出到text区域
                    text1.insert(END,"TR Address:")
                    text1.insert(END,hex(addr))
                    text1.insert(END," Value:")
                    text1.insert(END,TR)
                    text1.insert(END,b'\n')
                    addr=0x3f
                    # print("TR:0x%02X"%TR)
                elif addr==0x4a: #温度高8位
                    temperature_H=int(read[0:2],16)
                    # print("temperature_H:0x%02X"% temperature_H)
                elif addr==0x4b: #温度低8位
                    temperature_L=int(read[0:2],16)
                    # print("temperature_L:0x%02X"% temperature_L)
                    temperature_H=temperature_H<<8
                    temperature=temperature_L+temperature_H
                    Rt1=temperature*(6.8+0.05*TR)/(32768-temperature)
                    temperature=findTemperature(Rt1)
                    #输出到text区域
                    text1.insert(END,"Temperature Address:")
                    text1.insert(END,hex(addr))
                    text1.insert(END," Value:")
                    text1.insert(END,temperature)
                    text1.insert(END,b'\n')

                    theTime = datetime.datetime.now().strftime(IISOTIMEFORMAT)
                    f = open('Temperature.csv','a',encoding='utf-8',newline='')
                    csv_writer = csv.writer(f)
                    csv_writer.writerow([temperature,theTime])
                    f.close()

                    print("temperature:",temperature)
                elif addr==0x4c: #电流高8位
                    current_H=int(read[0:2],16)
                    if current_H==0xff:
                        print("Error current_H")
                        addr=0x4b
                    print("current_H:0x%02X"%current_H)
                elif addr==0x4d: #电流低8位
                    current_L=int(read[0:2],16)
                    current_H=current_H<<8
                    current=current_L+current_H
                    current=(current*200)/(26837*0.00125)
                    current=Decimal(current).quantize(Decimal("0.00"))

                    theTime = datetime.datetime.now().strftime(IISOTIMEFORMAT)
                    f = open('Current.csv','a',encoding='utf-8',newline='')
                    csv_writer = csv.writer(f)
                    csv_writer.writerow([current,theTime])
                    f.close()

                    #输出到text区域
                    text1.insert(END,"Current Address:")
                    text1.insert(END,hex(addr))
                    text1.insert(END," Value(mA):")
                    text1.insert(END,current)
                    text1.insert(END,b'\n')
                    print("current:",current)
                    current_L=0
                    current_H=0
                else:
                    cell_H=int(read[0:2],16)
        addr=addr+1
        if addr==0x6a: 
            addr=0x19
            # time.sleep(circuit*60)
        if addr==0x40:
            addr=0x4a
            # time.sleep(circuit*60)
        time.sleep(0.05)
        if sendT:
            break 
"""
串口打开关闭函数
"""
def  usart_ctrl(var,port_,bitrate_):
    global ser
    global sendT 
    sendT=False
    print(__file__,sys._getframe().f_lineno,port_,bitrate_,var.get())
    if var.get() == "Open Port":
        var.set("Close Port")
        ser = serial.Serial(
            port = port_,
            baudrate=int(bitrate_),
            parity=serial.PARITY_NONE,
            timeout=0.2,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS)

        #ser.open()
        # recv_data= threading.Thread(target=thread_recv)
        send_data = threading.Thread(target=thread_send)
        # recv_data.start()
        send_data.start()
    else :
        var.set("Open Port")
        sendT=True
        ser.close()
#总电量显示
def Graphics():
    data = pd.read_csv('Volt.csv')
    xdata = []
    ydata = []
    xdata = data.loc[:,'Time']   #将csv中列名为“列名1”的列存入xdata数组中
                                #如果ix报错请将其改为loc
    #xdata = data.iloc[:,num]   num处写要读取的列序号，0为csv文件第一列
    ydata = data.loc[:,'Volt(mv)']   #将csv中列名为“列名2”的列存入ydata数组中

    plt.plot(xdata,ydata,'bo-',label=u'',linewidth=1,marker=".")

    plt.title(u"Voltage Monitor",size=10)   #设置表名为“表名”
    # plt.tight_layout()  #自动填充，减少空白
    plt.grid(True)   #添加网格
    plt.legend()
    plt.xlabel(u'Time',size=10)   #设置x轴名为“x轴名”
    plt.ylabel(u'Volt',size=10)   #设置y轴名为“y轴名”
    plt.show()
#各个电芯电量显示图
def Cells_Graphics():
    data = pd.read_csv('Volt_Cells.csv')
    xdata = []
    xdata = data.loc[:,'Time']
    plt.plot(xdata,data["0x4f"], marker='*', linestyle='-', label='Cell-1')
    plt.plot(xdata, data["0x51"], marker='*', linestyle='-', label='Cell-2')
    plt.plot(xdata, data["0x53"], marker='*', linestyle='-', label='Cell-3')
    plt.plot(xdata, data["0x55"],  marker='*', linestyle='-', label='Cell-4')
    plt.plot(xdata, data["0x57"],  marker='*', linestyle='-', label='Cell-5')
    plt.plot(xdata, data["0x59"],  marker='*', linestyle='-', label='Cell-6')
    plt.plot(xdata, data["0x5b"],  marker='*', linestyle='-', label='Cell-7')
    plt.plot(xdata, data["0x5d"],  marker='*', linestyle='-', label='Cell-8')
    plt.plot(xdata, data["0x5f"],  marker='*', linestyle='-', label='Cell-9')
    plt.plot(xdata, data["0x61"],  marker='*', linestyle='-', label='Cell-10')
    plt.plot(xdata, data["0x63"],  marker='*', linestyle='-', label='Cell-11')
    plt.plot(xdata, data["0x65"],  marker='*', linestyle='-', label='Cell-12')
    plt.plot(xdata, data["0x67"],  marker='*', linestyle='-', label='Cell-13')
    plt.plot(xdata, data["0x69"],  marker='*', linestyle='-', label='Cell-14')

    plt.title("Cells Monitor", fontsize=18) ## 标题
    # plt.tight_layout()  #自动填充，减少空白
    plt.grid(True)   #添加网格
    plt.legend()
    plt.xlabel(u'Time',size=10)   #设置x轴名为“x轴名”
    plt.ylabel(u'Volt',size=10)   #设置y轴名为“y轴名”
    plt.legend() 

    # 显示图表
    plt.show()
"""
串口发送函数
"""
def usart_sent():
    x = ser.isOpen()
    if x == True:
        ser.write(b'\x35\x4e\x01')
        time.sleep(0.1)
        ser.write(b'\x35\x4f\x01')
        time.sleep(0.1)
    #print("-->",writedata)

"""
串口号改变回调函数
"""
def combo1_handler(var):
    port_serial = var
    print(__file__,sys._getframe().f_lineno,var,port_serial)

"""
串口波特率改变回调函数
"""
def combo2_handler(var):
    bitrate_serial = var
    print(__file__,sys._getframe().f_lineno,var,bitrate_serial)
def combo6_handler(var):
    print("Time:",var)
    global circuit
    circuit=1
    circuit=int(var[:-4])
    print("circuit",circuit)

def main():
    init_window = Tk()
    init_window.title('Voltage Monitor Tool                              v1.0.0')
    #init_window.geometry("800x600")

    frame_root = Frame(init_window)
    frame_left = Frame(frame_root)
    frame_right = Frame(frame_root)

    pw1 = PanedWindow(frame_left,orient=VERTICAL)
    # pw2 = PanedWindow(frame_left,orient=VERTICAL)
    # pw3 = PanedWindow(frame_left,orient=VERTICAL)

    frame1 = LabelFrame(pw1,text="Choose Port",labelanchor="n")
    frame2 = Frame(frame_left)
    # frame3 = LabelFrame(pw2,text="接收设置")
    # frame4 = LabelFrame(pw3,text="发送设置")

    pw1.add(frame1)
    pw1.pack(side=TOP)
    frame2.pack(side=TOP)
    # pw2.add(frame3)
    # pw2.pack(side=TOP)
    # pw3.add(frame4)
    # pw3.pack()
    frame5 = Frame(frame_right)
    frame5.pack(side=TOP)
    frame6 = Frame(frame_right)
    frame6.pack(side=TOP)

    global text1
    text1 = Text(frame5,width=50,height=15)
    text1.grid(column=0,row=0)

    canvas = Canvas(frame6, width=200, height=44)
    canvas.grid(column=0,row=1)
    this_dir = os.path.split(sys.argv[0])[0] #获取当前路径
    source=os.path.join(this_dir, "logo.png")
    photoimage = ImageTk.PhotoImage(file=source)
    canvas.create_image(44, 0,anchor=NW,image=photoimage)#NW指示图片的摆放位置以左上角坐标为基准，不加则使用图片中心位置坐标为基准

    # label0 = Label(frame6,text="Note:Click 'Open Port' to record Msg of Battery",height=2)
    # label0.grid(column=0,row=2)

    button2 = Button(frame6,text="Clear",width=14,height=1)
    button2.bind("<Button-1>",lambda event: text1.delete(1.0,END))
    button2.grid(column=3,row=2)

    button3=Button(frame6,text="Sum Voltage",width=14,height=1)
    button3.bind("<Button-1>",lambda event: Graphics())
    button3.grid(column=1,row=2)

    button4=Button(frame6,text="Cells Voltage",width=14,height=1)
    button4.bind("<Button-1>",lambda event: Cells_Graphics())
    button4.grid(column=0,row=2)

    label1 = Label(frame1,text="Port",height=2)
    label1.grid(column=0,row=0)
    label2 = Label(frame1,text="BaudRate",height=2)
    label2.grid(column=0,row=1)
    label3 = Label(frame1,text="Data Bits",height=2)
    label3.grid(column=0,row=2)
    label4 = Label(frame1,text="Parity",height=2)
    label4.grid(column=0,row=3)
    label5 = Label(frame1,text="Stop Bits",height=2)
    label5.grid(column=0,row=4)
    label6 = Label(frame1,text="Circle Time",height=2)
    label6.grid(column=0,row=5)

    port_list = list(serial.tools.list_ports.comports())
    print(len(port_list))

    portcnt = 0
    portcnt = len(port_list)
    serial_com = []

    varPort = StringVar()
    combo1 = ttk.Combobox(frame1,textvariable = varPort, width=8,height=2,justify=CENTER,state= "readonly")
    for m in range(portcnt):
        port_list_1 = list(port_list[m])
        serial_com.append(port_list_1[0])

    serial_com.append("COM0")
    combo1['values'] = serial_com
    print(__file__,sys._getframe().f_lineno,m,serial_com)

    combo1.bind("<<ComboboxSelected>>",lambda event:combo1_handler(var=varPort.get()))
    combo1.current(0)
    combo1.grid(column=1,row=0)
    varBitrate  = StringVar()
    combo2 = ttk.Combobox(frame1,textvariable = varBitrate,width=8,height=2,justify=CENTER,state= "readonly")
    combo2['values']=("9600","19200","38400","115200")
    combo2.bind("<<ComboboxSelected>>",lambda event:combo2_handler(var=varBitrate.get()))
    combo2.current(0)
    combo2.grid(column=1,row=1)
    combo3 = ttk.Combobox(frame1,width=8,height=2,justify=CENTER,state= "readonly")
    combo3['values']=("5 bit","6 bit","7 bit","8 bit")
    combo3.current(3)
    combo3.grid(column=1,row=2)

    combo4 = ttk.Combobox(frame1,width=8,height=2,justify=CENTER,state= "readonly")
    combo4['values']=("NONE","ODD","EVEN","MARK","SPACE")
    combo4.current(0)
    combo4.grid(column=1,row=3)

    combo5 = ttk.Combobox(frame1,width=8,height=2,justify=CENTER,state= "readonly")
    combo5['values']=("1 bit","1.5 bit","2 bit")
    combo5.current(0)
    combo5.grid(column=1,row=4)

    varMin  = StringVar()
    combo6 = ttk.Combobox(frame1,textvariable = varMin,width=8,height=2,justify=CENTER,state= "readonly")
    combo6['values']=("1 min","5 min"," 10 min","30 min","60 min","120 min","0 min")
    combo6.bind("<<ComboboxSelected>>",lambda event:combo6_handler(var=varMin.get()))
    combo6.current(0)
    combo6.grid(column=1,row=5)

    var1 = StringVar()
    var1.set("Open Port")
    button1 = Button(frame2,textvariable=var1,width=13,height=2)
    button1.bind("<Button-1>",lambda event:usart_ctrl(var=var1,port_=combo1.get(),bitrate_=combo2.get()))
    button1.grid(column=0,row=0)

    combo1.grid(column=1,row=0)
    frame_left.pack(side=LEFT)
    frame_right.pack(side=RIGHT)
    frame_root.pack()
    init_window.mainloop()
if __name__ == "__main__":
    main()
