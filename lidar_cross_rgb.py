# Cross Drawing
#
# This example shows off drawing crosses on the OpenMV Cam.

import sensor, image, time, pyb
from pyb import UART
# from tfmini import TFmini
sensor.reset()
sensor.set_pixformat(sensor.RGB565) # or GRAYSCALE...
sensor.set_framesize(sensor.QVGA) # or QQVGA...
sensor.skip_frames(time = 2000)




def draw_pic_lidar(dis):
    img = sensor.snapshot()

    x = int(img.width()/2)
    y = int(img.height()/2)
    r = 176
    g = 224
    b = 230
    # 淺藍
    img.draw_cross(x, y, color = (r, g, b), size = 3, thickness = 1)

    x = 12
    y = 220
    r = 255
    g = 255
    b = 0
    dis = str(dis)
    img.draw_string(x, y, dis, color = (r, g, b), scale = 2, mono_space = False,
                char_rotation = 0, char_hmirror = False, char_vflip = False,
            string_rotation = 0, string_hmirror = False, string_vflip = False)
    #for x in range(320):
    #    print(img.get_pixel(x,120))

if __name__ == '__main__':
    #sensor.snapshot()
    #sensor.snapshot().save("example.jpg") # or "example.bmp" (or others)
    #print(sensor.get_fb())
    clock = time.clock()
    uart = UART(3, 115200)
    #uart.init(115200, bits=8, parity=None, stop=1) # init with given parameters
    clock.tick()
    while(True):
        recv = uart.read(9)
        if recv == None:
            pass
        elif len(recv) == 9:
            if recv[0] == 0x59 and recv[1] == 0x59:
                checksum = 0
                for i in range(0, 8):
                    checksum = checksum + recv[i]
                checksum = checksum % 256
                if checksum == recv[8]:
                    distance = recv[2] + recv[3] * 256
                    strength = recv[4] + recv[5] * 256
                    #print(distance, strength)
                draw_pic_lidar(distance)
