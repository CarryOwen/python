#若该键盘鼠标的操作被检测到了，可以使用pip install pywinio模块，制作驱动级别的键鼠模拟

from ctypes import windll, byref, c_ubyte
from ctypes.wintypes import RECT, HWND
import numpy as np
import win32api
import win32gui, win32ui, win32con
import cv2
# import pyautogui
import time
import threading
selfList = []
last_img = None
class Poker:
    def __init__(self, name, img, num=24):
        self.num = num
        self.name = name
        # h, w = img.shape

        # 手牌
        self.selfImg = img
        self.isUpOut = False
        self.isDownOut = False
        # self.otherImg =img
        # self.handImg =img
        # # 出牌
        # if name == '王':
        #     self.otherImg = cv2.resize(img, (int(w / 1.8), int(h / 1.8)))
        #     # 底牌
        #     self.handImg = cv2.resize(img, (int(w / 4.1), int(h / 4.1)))
        # elif name == '8' or name == '9':
        #     self.otherImg = cv2.resize(img, (int(w / 1.3), int(h / 1.3)))
        #     # 底牌
        #     self.handImg = cv2.resize(img, (int(w / 1.9), int(h / 1.9)))
        # else:
        #     self.otherImg = cv2.resize(img, (int(w / 1.3), int(h / 1.3)))
        #     # 底牌
        #     self.handImg = cv2.resize(img, (int(w / 1.8), int(h / 1.8)))

    def setNum(self, num):
        self.num = num

    def init(self):
        if self.name == '大王':
            self.num = 6
        elif self.name == '小王':
            self.num = 6
        else:
            self.num = 24
PokerList =  [
    Poker('大王', cv2.imread('dawang.png', 0), 6),
    Poker('小王', cv2.imread('xiaowang.png', 0), 6),
    Poker('2', cv2.imread('2.png', 0)),
    Poker('A', cv2.imread('A.png', 0)),
    Poker('K', cv2.imread('K.png', 0)),
    Poker('Q', cv2.imread('Q.png', 0)),
    Poker('J', cv2.imread('J.png', 0)),
    Poker('10', cv2.imread('10.png', 0)),
    Poker('9', cv2.imread('9.png', 0)),
    Poker('8', cv2.imread('8.png', 0)),
    Poker('7', cv2.imread('7.png', 0)),
    Poker('6', cv2.imread('6.png', 0)),
    Poker('5', cv2.imread('5.png', 0)),
    Poker('4', cv2.imread('4.png', 0)),
]
PokerList_chu =  [
    Poker('大王', cv2.imread('dawang1.bmp', 0), 6),
    Poker('小王', cv2.imread('xiaowang1.bmp', 0), 6),
    Poker('2', cv2.imread('22.bmp', 0)),
    Poker('A', cv2.imread('AA.bmp', 0)),
    Poker('K', cv2.imread('KK.bmp', 0)),
    Poker('Q', cv2.imread('QQ.bmp', 0)),
    Poker('J', cv2.imread('JJ.bmp', 0)),
    Poker('10', cv2.imread('1010.bmp', 0)),
    Poker('9', cv2.imread('99.bmp', 0)),
    Poker('8', cv2.imread('88.bmp', 0)),
    Poker('7', cv2.imread('77.bmp', 0)),
    Poker('6', cv2.imread('66.bmp', 0)),
    Poker('5', cv2.imread('55.bmp', 0)),
    Poker('4', cv2.imread('44.bmp', 0)),
]
def screen():
    hWnd = win32gui.FindWindow(None, "雷电模拟器")
    left, top, right, bot = win32gui.GetWindowRect(hWnd)
    width = right - left
    height = bot - top
    # 窗口隐藏或最小化，无法截图
    if top < 0:
        return None
    # 返回句柄窗口的设备环境，覆盖整个窗口，包括非客户区，标题栏，菜单，边框
    hWndDC = win32gui.GetWindowDC(hWnd)
    # 创建设备描述表
    mfcDC = win32ui.CreateDCFromHandle(hWndDC)
    # 创建内存设备描述表
    saveDC = mfcDC.CreateCompatibleDC()
    # 创建位图对象准备保存图片
    saveBitMap = win32ui.CreateBitmap()
    # 为bitmap开辟存储空间
    saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
    # 将截图保存到saveBitMap中
    saveDC.SelectObject(saveBitMap)
    saveDC.BitBlt((0, 0), (width, height), mfcDC, (0, 0), win32con.SRCCOPY)
    # 保存截图
    # saveBitMap.SaveBitmapFile(saveDC, "img_Winapi.bmp")
    signedIntsArray = saveBitMap.GetBitmapBits(True)
    img = np.fromstring(signedIntsArray, np.uint8)
    img.shape = (height, width, 4)
    # 保存bitmap到内存设备描述表
    img = cv2.resize(img, (1040, 629), interpolation=cv2.INTER_CUBIC)
    img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
    # 显示转换的图片1s钟
    # cv2.imshow('Match Template', img)
    # cv2.waitKey(1000)
    # cv2.imwrite('screen.png', img)
    # 返回一张可以给opencv 使用的图片
    return img
def matchImgNum(bgImg, templeteImg, threshold=0.65):
    '''
    bgImg：截图出来的底片
    templeteImg；模板图片
    threshold：对比精确度
    '''
    res = cv2.matchTemplate(bgImg, templeteImg, cv2.TM_CCOEFF_NORMED)
    tt = bgImg.copy()
    w, h = templeteImg.shape[::-1]
    loc = np.where(res >= threshold)
    num = 0
    last = 0
    if len(loc[0]) != 0:
        # 排序
        loc[1].sort()
        for point in loc[1]:
            if abs(last - point) > 5:
                num += 1
                # if save:
                # print(save)
                # for pt in zip(*loc[::-1]):
                #     cv2.rectangle(tt, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
                # cv2.imshow('Match Template', tt)
                # cv2.waitKey(100)
            last = point
    return num,last
def my_test():
    img = screen()
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)[350:622, 10:1042]
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = img[400:550, 60:900]
    cv2.imshow('Match Template', img)
    cv2.waitKey(100)
    # 读取 模板， 扑克4
    temp = cv2.imread('dawang.png', 0)
    num = matchImgNum(img, temp, 0.75)
    print("dawang:",num);
    temp = cv2.imread('xiaowang.png', 0)
    num = matchImgNum(img, temp, 0.75)
    print("xiaowang:",num);
    temp = cv2.imread('2.png', 0)
    num = matchImgNum(img, temp, 0.75)
    print("2:",num);
    temp = cv2.imread('A.png', 0)
    num = matchImgNum(img, temp, 0.75)
    print("A:",num);
    temp = cv2.imread('K.png', 0)
    num = matchImgNum(img, temp, 0.75)
    print("K:",num);
    temp = cv2.imread('Q.png', 0)
    num = matchImgNum(img, temp, 0.75)
    print("Q:",num);
    temp = cv2.imread('J.png', 0)
    num = matchImgNum(img, temp, 0.75)
    print("J:",num);
    temp = cv2.imread('10.png', 0)
    num = matchImgNum(img, temp, 0.75)
    print("10:",num);

def monitor():
    global last_img
    templates=PokerList_chu
    img_gray = screen()
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)[350:622, 10:1042]
    img_gray = cv2.cvtColor(img_gray, cv2.COLOR_BGR2GRAY)
    last_img = img_gray.copy()
    while True:
        img_gray = screen()
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)[350:622, 10:1042]
        img_gray = cv2.cvtColor(img_gray, cv2.COLOR_BGR2GRAY)
        shangjia = img_gray[200:390, 70:390]
        xiajia = img_gray[260:390, 670:850]
        shanglian = img_gray[110:250,100:300]
        xialian = img_gray[150:350,700:900]
        duimen = img_gray[30:150,500:900]
        del_num=0
        num, x = matchImgNum(shangjia,  cv2.imread('chupal.bmp', 0))
        if num>0:
            print("上家出牌！")
            cv2.imshow('Match Template', shangjia)
            cv2.waitKey(100)
            img_gray = screen()
            img_gray = cv2.cvtColor(img_gray, cv2.COLOR_BGR2GRAY)
            shangjia = img_gray[200:390, 70:390]
            for pokerObj in templates:
                num, x = matchImgNum(shangjia, pokerObj.selfImg)
                if num>0:
                    print(pokerObj.name+" 张数: ", num,"剩余张数：",selfList[del_num])
                selfList[del_num]=selfList[del_num]-num
                del_num = del_num+1
        num, x = matchImgNum(xiajia,  cv2.imread('chupal.bmp', 0))
        if num>0:
            print("下家出牌！")
            cv2.imshow('Match Template', xiajia)
            cv2.waitKey(100)
            img_gray = screen()
            # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)[350:622, 10:1042]
            img_gray = cv2.cvtColor(img_gray, cv2.COLOR_BGR2GRAY)
            xiajia = img_gray[260:390, 670:850]
            for pokerObj in templates:
                num, x = matchImgNum(xiajia, pokerObj.selfImg)
                if num>0:
                    print(pokerObj.name+" 张数: ", num,"剩余张数：",selfList[del_num])
                selfList[del_num]=selfList[del_num]-num
                del_num = del_num+1
        num, x = matchImgNum(shanglian,  cv2.imread('chupal.bmp', 0))
        if num>0:
            print("上联出牌！")
            cv2.imshow('Match Template', shanglian)
            cv2.waitKey(100)
            img_gray = screen()
            # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)[350:622, 10:1042]
            img_gray = cv2.cvtColor(img_gray, cv2.COLOR_BGR2GRAY)
            shanglian = img_gray[110:250,100:300]
            for pokerObj in templates:
                num, x = matchImgNum(shanglian, pokerObj.selfImg)
                if num>0:
                    print(pokerObj.name+" 张数: ", num,"剩余张数：",selfList[del_num])
                selfList[del_num]=selfList[del_num]-num
                del_num = del_num+1
        num, x = matchImgNum(xialian,  cv2.imread('chupal.bmp', 0))
        if num>0:
            print("下联出牌！")
            cv2.imshow('Match Template', xialian)
            cv2.waitKey(100)
            img_gray = screen()
            # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)[350:622, 10:1042]
            img_gray = cv2.cvtColor(img_gray, cv2.COLOR_BGR2GRAY)
            xialian = img_gray[150:350,700:900]
            for pokerObj in templates:
                num, x = matchImgNum(xialian, pokerObj.selfImg)
                if num>0:
                    print(pokerObj.name+" 张数: ", num,"剩余张数：",selfList[del_num])
                selfList[del_num]=selfList[del_num]-num
                del_num = del_num+1
        num, x = matchImgNum(duimen,  cv2.imread('chupal.bmp', 0))
        if num>0:
            print("对门出牌！")
            img_gray = screen()
            # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)[350:622, 10:1042]
            img_gray = cv2.cvtColor(img_gray, cv2.COLOR_BGR2GRAY)
            duimen = img_gray[30:150,500:900]
            for pokerObj in templates:
                cv2.imshow('Match Template', duimen)
                cv2.waitKey(100)
                cv2.imshow('Match Template', pokerObj.selfImg)
                cv2.waitKey(100)
                num, x = matchImgNum(duimen, pokerObj.selfImg)
                if num>0:
                    print(pokerObj.name+" 张数: ", num,"剩余张数：",selfList[del_num])
                selfList[del_num]=selfList[del_num]-num
                del_num = del_num+1
        time.sleep(0.5)




def main():
    global selfList
    img_rgb = screen()
    if img_rgb is None:
         return
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    outList = {}
    templates = PokerList
     # 自己的手牌区域
    selfCard = img_gray[400:550, 60:900]

    handCard = img_gray[45:400, 900:570]
    selfOutList = []
    handList = []
    for pokerObj in templates:
        num, x = matchImgNum(selfCard, pokerObj.selfImg)
        pokerObj.num = pokerObj.num - num
        # print("剩余张数:",pokerObj.num)
        print(pokerObj.name+" 张数: ", num,"剩余张数：",pokerObj.num)
        selfList.append(pokerObj.num)
    print("selfList:",selfList)
    T1=threading.Thread(target=monitor, name="T1")
    T1.start()
main()


