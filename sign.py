from hashlib import md5
import sys
device_sn = ""
# 单播
if len(sys.argv)==4:
    if sys.argv[1]=="1":
        print ('Iput ' ,"msg_content: "+sys.argv[2])
        print ('Iput ' ,"device's SN: "+sys.argv[3])
        device_sn = sys.argv[3]
        content="content={\"type\":\"audio\",\"info\":{\"msg_content\":\""+sys.argv[2]+"\",\"msg_id\":\"0f3a9a96-6de6-47c7-a672-ed16c6b029db\",\"voice_speed\": \"50\",\"stop\":\"\",\"stop\":\"\",\"stop\":\"\"}}"
# 循环播报
if len(sys.argv)==4:
    if sys.argv[1]=="2":
        print ('Iput ' ,"msg_content: "+sys.argv[2])
        print ('Iput ' ,"device's SN: "+sys.argv[3])
        device_sn = sys.argv[3]
        content="content={\"type\":\"audio\",\"cirInfo\":{\"cirInfo_content\":\""+sys.argv[2]+"\",\"interTime\":\"1\",\"brodTime\":\"3\",\"voice_speed\":\"50\",\"stop\":\"\",\"stop\":\"\",\"stop\":\"\"}}"
# 单播+循环播报
if sys.argv[1]=="3":
    if len(sys.argv)==5:
        print ('Iput ' ,"msg_content: "+sys.argv[2])
        print ('Iput ' ,"circle: "+sys.argv[3])
        print ('Iput ' ,"device's SN: "+sys.argv[4])
        device_sn = sys.argv[4]
        content="content={\"type\":\"audio\",\"info\":{\"msg_content\": \""+sys.argv[2]+"\",\"msg_id\":\"0f3a9a96-6de6-47c7-a672-ed16c6b029db\",\"voice_speed\": \"50\"},\"cirInfo\":{\"cirInfo_content\":\""+sys.argv[3]+"\",\"interTime\":\"1\",\"brodTime\":\"3\",\"voice_speed\":\"50\",\"stop\":\"\"}}"
# 循环播报终止
if sys.argv[1]=="4":
    content="content={\"type\":\"audio\",\"cirInfo\":{\"stop\":\"1\"}}"


proKey = "proKey=a1U46T2gXgf"
reqTime="reqTime=2023-07-03 17:05:44"
signType="signType=MD5"
topicName="topicName=/a1U46T2gXgf/"+device_sn+"/user/report"
userId="userId=16fa6fae-50c2-4e4f-999e-befbb8368e87"
version="version=1.0"
key="key=12345qwert"
sign=content+"&"+proKey+"&"+reqTime+"&"+signType+"&"+topicName+"&"+userId+"&"+version+"&"+key
print("To be signed string = ",sign)
md5_url = md5(sign.encode('utf8')).hexdigest().upper()
print("Sign MD5 = ",md5_url)