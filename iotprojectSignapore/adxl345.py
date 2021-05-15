import time
from machine import I2C


ADXL345_ADDR = 0x53

i2c = I2C(0, I2C.MASTER, baudrate=100000)

BW_RATE_100HZ = 0x0B
POWER_CTL = 0x2D 
MEASURE = 0x08
DATA_FORMAT = 0x31
AXES_DATA = 0x32
BW_RATE = 0x2C
RANGE_2G = 0x00
SCALE_MULTIPLIER = 0.004
EARTH_GRAVITY_MS2 = 9.80665

class ADXL345(object):
	

	def __init__(self, i2c=None):
		self.i2c = i2c
		self.addr = ADXL345_ADDR
		print('One')
		self.setBandwidthRate(BW_RATE_100HZ)
		self.setRange(RANGE_2G)
		self.enableMeasurement()

	def enableMeasurement(self):
		i2c.writeto(self.addr, bytes([POWER_CTL]))
		i2c.writeto(self.addr, bytes([MEASURE])) 

	def setBandwidthRate(self, rate_flag):
		print('Two')
		i2c.writeto_mem(self.addr, BW_RATE, bytes([rate_flag]))
        # i2c.writeto_mem(self.addr, BW_RATE, rate_flag)


	def setRange(self, range_flag):
		value = i2c.readfrom_mem(self.addr, DATA_FORMAT, range_flag)
		print('here')
		value &= ~0x0F;
		value |= range_flag;
		value |= 0x08;

		i2c.writeto(self.addr, DATA_FORMAT, value)

	def getAxes(self, gforce = False):
		bytes = i2c.readfrom(self.addr, AXES_DATA, 6)

		x = bytes[0] | (bytes[1] << 8)
		if(x & (1 << 16 - 1)):
			x = x - (1<<16)

		y = bytes[2] | (bytes[3] << 8)
		if(y & (1 << 16 - 1)):
			y = y - (1<<16)

		z = bytes[4] | (bytes[5] << 8 )
		if(z & (1 << 16 - 1)):
			z = z - (1<<16)

		x = x * SCALE_MULTIPLIER
		y = y * SCALE_MULTIPLIER
		z = z * SCALE_MULTIPLIER

		if gforce == False: 
			x = x * EARTH_GRAVITY_MS2
			y = y * EARTH_GRAVITY_MS2
			z = z * EARTH_GRAVITY_MS2

		x = round(x,4)
		y = round(y,4)
		z = round(z,4)

		return {"x": x, "y": y, "z": z}
print('Start')

for i in range(0,10):
	adxl345 = ADXL345()
	axes = adxl345.getAxes(True)
	print(axes['x'])
	sleep_ms(25)