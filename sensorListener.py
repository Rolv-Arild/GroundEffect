import serial


def sendMsg(s):
    ser.write(s)
    return ser.readline().decode("utf-8")


ser = serial.Serial("COM3", 9600)
while True:
    dist = int(sendMsg(b"ayyyy"))  # distance in mm.
    print(dist)