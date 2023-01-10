
from win32com.client import Dispatch
import time
import commandSend as mouse
from ctypes.wintypes import HWND, POINT
from ctypes import c_ulong, windll, byref
getMousePos = windll.user32.GetCursorPos
from ctypes import *
import sys, os
import threading
dd_dll = windll.LoadLibrary('D:\DD94687.64.dll')
time.sleep(2)
st = dd_dll.DD_btn(0) #DD Initialize
op = Dispatch("op.opsoft")

this_dir = os.path.split(sys.argv[0])[0] 
dm_ret = op.SetPath(this_dir)
op_ret = op.SetDict(0, "dm_soft.txt")
finded = False

def attack():
    global lock
    while True:
        lock.acquire()
        co = op.FindStr(310, 110, 1100, 700, "贼偷", "fd7024-151515", 0.8)
        if co[1]<0:
            co=op.FindPic(310, 110, 1100, 700,"zeitou.bmp","101010",0.8,0);
        elif co[1]>0:
            print("Find Monster In:",co[1], co[2])
            dd_dll.DD_mov(co[1]+16, co[2]+55)
            time.sleep(0.1)
            dd_dll.DD_btn(1)
            dd_dll.DD_btn(2)
            co = op.FindStr(310, 110, 1100, 700, "贼偷", "fd7024-151515", 0.8)
            if co[1]<0:
                co=op.FindPic(310, 110, 1100, 700,"zeitou.bmp","101010",0.8,0);
            dd_dll.DD_mov(co[1]+16, co[2]+55)
            time.sleep(0.1)
            dd_dll.DD_btn(1)
            dd_dll.DD_btn(2)
            time.sleep(9)
            lock.release()
            time.sleep(1)
        if co[1]<0:
            lock.release()
            time.sleep(1)

    
    

def search():
    global lock
    while True:
        lock.acquire()
        print("Searching Monsteres...")
        dd_dll.DD_mov(960,540)
        dd_dll.DD_btn(1)
        dd_dll.DD_btn(2)
        dd_dll.DD_movR(20,0)
        dd_dll.DD_btn(1)
        dd_dll.DD_btn(2)
        dd_dll.DD_btn(1)
        dd_dll.DD_btn(2)
        lock.release()
        time.sleep(3)
if __name__ == "__main__":
    lock = threading.Lock()
    T1 = threading.Thread(target=attack, name="T1")
    T2 = threading.Thread(target=search, name="T2")
    T1.start()
    T2.start()