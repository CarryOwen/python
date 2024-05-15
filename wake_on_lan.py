import socket
import binascii

'''
格式化mac地址，生成魔法唤醒包，然后发送。
mac格式： mac = "A1B2C3D4E5F6"
唤醒包格式： send_data = binascii.unhexlify('FF'*6 + str(mac)*16)
'''
MAC = "047c16d448af"
data = 'FF' * 6 + str(MAC) * 16
print("data:", data)
send_data = binascii.unhexlify(data)
broadcast_address = '121.228.108.161'
port = 9
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.sendto(send_data, (broadcast_address, port))

