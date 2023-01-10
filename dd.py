
from ctypes import *
import time
from win32com.client import Dispatch
import time
import commandSend as mouse
import sys, os
print("Load DD!")

dd_dll = windll.LoadLibrary('D:\DD94687.64.dll')
time.sleep(2)

st = dd_dll.DD_btn(0) #DD Initialize
if st==1:
    print("OK")
else:
    print("Error")
    exit(101)


print("Keyboard Left win")
#LWin is 601 in ddcode, 1=down, 2=up.
# dd_dll.DD_key(601, 1)
# dd_dll.DD_key(601, 2)
# time.sleep(2)

print("Mouse move abs.")
dd_dll.DD_mov(200, 200)
time.sleep(2)
op = Dispatch("op.opsoft")
# run all test
print("test begin")
this_dir = os.path.split(sys.argv[0])[0] 
dm_ret = op.SetPath(this_dir)
op_ret = op.SetDict(0, "dm_soft.txt")
# print("Mouse move rel.")
# dd_dll.DD_movR(50, 50)
# time.sleep(2)

print("Mouse Right button ")
#1==L.down, 2==L.up, 4==R.down, 8==R.up, 16==M.down, 32==M.up
dd_dll.DD_btn(4)
dd_dll.DD_btn(8)
time.sleep(2)
