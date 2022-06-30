
from win32com.client import Dispatch
import time
class Demo:
    def __init__(self):
        #创建com对象
        self.op=op=Dispatch("op.opsoft");
        # self.op.SetPath(R"C:\Users\YWOU\Desktop")
        # self.hwnd=0;
        # self.send_hwnd=0;
        print("init");
    def findBloodFog(self):
        co=self.op.FindMultiColor(1,38,359,357,'0156d6','-3|0|bbdffb,-2|5|ed453b,5|7|02d503,12|6|516e78',1,0)
        print(co[1]/1.25,co[2]/1.25,co)
        self.op.MoveTo(co[1]/1.25,co[2]/1.25)
        
def test_all():
    demo=Demo();
    demo.findBloodFog();

    return 0;
op=Dispatch("op.opsoft")
#run all test
print("test begin");
# while True :
co=op.FindMultiColor(345,179,1259,883,'05fc81','20|15|16c861-163632',1,0)
print(co[1]/1.25,co[2]/1.25,co)
op.MoveTo(co[1],co[2])
        # time.sleep(1)
print("test end");

