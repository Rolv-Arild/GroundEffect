import serial


def sendMsg(s):
    ser.write(s)
    print(ser.readline())


ser = serial.Serial("COM3", 9600)
while True:
    #sendMsg(b"on")
    sendMsg(b"off")