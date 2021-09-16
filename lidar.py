import serial

ser = serial.Serial('/dev/tty.usbserial-0001')
ser.baudrate = 230400

# 1 byte - header
# 1 byte - ver_len?
# 2 byte - speed
# 2 byte - start angle
# 12*3 - Point Data
# 2 byte - end angle
# 2 byte - timestamp
# 1 byte - crc8

l = 0
data = []
distance_readings = [0]*360

def prettyPrintDistance():
    print("=======================")
    for i in range(0, 360, 5):
        print("(" + str(i) + ") " + str(distance_readings[i]))

def parsePacket():
    if (len(data) < 47):
        return
    d = [ord(x) for x in data]

    header = d[0]
    ver_len = d[1]
    speed = d[3] << 8 | d[2]

    start_angle = d[5] << 8 | d [4]
    end_angle = d[43] << 8 | d[42]

    diff = end_angle - start_angle
    if (diff < 0):
        diff += 36000
    step = diff / 12-1 / 100.0

    for i in range(0, 12):
        angle = round((start_angle + step*i) / 100.0)
        distance = d[6+3*i + 1] << 8 | d[6+3*i]
        if (angle < 360):
            distance_readings[angle] = distance
 
    timestamp = d[45] << 8 | d[44]
    crc8 = d[46]

    prettyPrintDistance()


while(1):
    a = ser.read()
    data.append(a)
    l += 1
    if (a == b'\x54'):
        l = 0
        parsePacket()
        data = [a]