from time import sleep
import MyLSM303
import math
import os
clear = lambda: os.system('clear')

lsm = MyLSM303.MyLSM303()

MmaxX = -2000
MmaxY = -2000
MmaxZ = -2000

MminX = 2000
MminY = 2000
MminZ = 2000

AmaxX = -2000
AmaxY = -2000
AmaxZ = -2000

AminX = 2000
AminY = 2000
AminZ = 2000

while True:
    x,y,z = lsm.readMagRaw(True)
    ax, ay, az = lsm.readAccRaw(True)

    print "mag: ", (MminX, MminY, MminZ), (MmaxX, MmaxY, MmaxZ)
    print "acc: ", (AminX, AminY, AminZ), (AmaxX, AmaxY, AmaxZ)

    if x > MmaxX:
        MmaxX = x
    if y > MmaxY:
        MmaxY = y
    if z > MmaxZ:
        MmaxZ = z

    if x < MminX:
        MminX = x
    if y < MminY:
        MminY = y
    if z < MminZ:
        MminZ = z

    if ax > AmaxX:
        AmaxX = ax
    if ay > AmaxY:
        AmaxY = ay
    if az > AmaxZ:
        AmaxZ = az

    if ax < AminX:
        AminX = ax
    if ay < AminY:
        AminY = ay
    if az < AminZ:
        AminZ = az

    sleep(0.1)
    clear()