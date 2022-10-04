import serial
import binascii
import time


class KeyenceSZ16Dping:

    def __init__(self):
        try:
            self.obj_port = serial.Serial('/dev/ttyS1', 9600, 8, 'N', 1, None)
        except serial.SerialException as error:
            print("ERROR: check if already have another device on this port!")
            serial.close()

    def tick(self):
        points = []
        value = []
        upper_level = 0
        try:
            self.obj_port.write(b'\x90\x00\x18\xEB')
        except serial.SerialException:
            print("ERROR: check if already have another device on this port!")
        time.sleep(1)
        while self.obj_port.in_waiting > 0:
            try:
                serial_data = self.obj_port.read() 
                value.append(binascii.hexlify(serial_data).decode('utf-8'))
            except serial.SerialException:
                print("ERROR: check if already have another device on this port!")
        
        list = value[9:-2]
        list_int = [int(item, 16) for item in list]
        for i in range(len(list_int)):
            if i % 2 == 0:
                upper_level = (list_int[i] & 63) << 8
            else:
                lower_level = upper_level + list_int[i]
                points.append(lower_level)
        points_f = []
        for i in range(len(points)):
            points_f.append(float(points[i]))
        return points_f


if __name__ == '__main__':
    app = KeyenceSZ16Dping()
    while True:
        data = app.tick()
        print(data)