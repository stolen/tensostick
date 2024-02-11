import time
import board
import busio
import pwmio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

maxval = 512
pwmcenter = 32768
pwmstep = pwmcenter // maxval
def setpwm(val, pin):
    duty = pwmcenter + val*pwmstep
    duty = max(0, min(65535, duty))
    pin.duty_cycle = duty



x1 = pwmio.PWMOut(board.A0, frequency=1000000, duty_cycle=2**15)
y1 = pwmio.PWMOut(board.A1, frequency=1000000, duty_cycle=2**15)
i2c1 = busio.I2C(board.GP1, board.GP0, frequency=1000000)
ads1 = ADS.ADS1115(i2c1, address=0x49, gain=16, data_rate=860, mode=ADS.Mode.SINGLE)

x2 = pwmio.PWMOut(board.A2, frequency=1000000, duty_cycle=2**15)
y2 = pwmio.PWMOut(board.A3, frequency=1000000, duty_cycle=2**15)
i2c2 = busio.I2C(board.GP7, board.GP6, frequency=1000000)
ads2 = ADS.ADS1115(i2c2, gain=16, data_rate=860, mode=ADS.Mode.SINGLE)

# rates: [8, 16, 32, 64, 128, 250, 475, 860]

chan1a = AnalogIn(ads1, ADS.P0, ADS.P3)
chan1b = AnalogIn(ads1, ADS.P1, ADS.P3)

chan2a = AnalogIn(ads2, ADS.P0, ADS.P3)
chan2b = AnalogIn(ads2, ADS.P1, ADS.P3)

cal1a = sorted([chan1a.value for i in range(0,31)])[15]
cal1b = sorted([chan1b.value for i in range(0,31)])[15]
cal2a = sorted([chan2a.value for i in range(0,31)])[15]
cal2b = sorted([chan2b.value for i in range(0,31)])[15]

n = 0
time1 = time.monotonic()
while True:
    n += 1
    a1 = chan1a.value - cal1a
    setpwm(a1, y1)
    a2 = chan2a.value - cal2a
    setpwm(a2, x2)
    b1 = chan1b.value - cal1b
    setpwm(-b1, x1)
    b2 = chan2b.value - cal2b
    setpwm(b2, y2)
    time2 = time.monotonic()
    if (time2 - time1 > 1.0) or n > 300:
        print("n={:>5} dt={:>5.2f} ({:>5},{:>5}) ({:>5},{:>5})".format(n, time2 - time1, a1, b1, a2, b2))
        time1 = time2
        n = 0
