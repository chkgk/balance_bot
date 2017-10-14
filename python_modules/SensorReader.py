import time
import math

from threading import Thread

import L3GD20
import MyLSM303

class SensorReader(Thread):
	def __init__(self):
		Thread.__init__(self)
		
		self.main_loop_frequency = 250 # hz
		self.sampling_frequency = 50 # hz
		
		self.last_sampling_time = None
		self.dt = None
		
		self.gX = 0.0
		self.gY = 0.0
		self.gZ = 0.0
		
		self.pitch = 0.0
		self.roll = 0.0
		self.yaw = 0.0
		
		self.mX = 0.0
		self.mY = 0.0
		self.mZ = 0.0

		self.lastPitch = self.pitch
		self.lastRoll = self.roll
		self.lastYaw = self.yaw
		
		self.alpha = 0.98
		self.filterPitch = 0.0
		self.filterRoll = 0.0
		self.filterYaw = 0.0

		self.lastFilterPitch = self.filterPitch
		self.lastFilterRoll = self.filterRoll
		self.lastFitlerYaw = self.filterYaw
		
		self.yawOffset = 0.0
		
		self.killThread = False
		
		self.Gyro = L3GD20.L3GD20(busId = 1, slaveAddr = 0x6b, ifLog = False, ifWriteBlock=False)
		self.AccMag = MyLSM303.MyLSM303()
		
		self._setup_gyro()
		
	def _setup_gyro(self):
		self.Gyro.Set_PowerMode("Normal")
		self.Gyro.Set_FullScale_Value("250dps")
		self.Gyro.Set_AxisX_Enabled(True)
		self.Gyro.Set_AxisY_Enabled(True)
		self.Gyro.Set_AxisZ_Enabled(True)
		self.Gyro.Set_HighPassFilter_Enabled(True)
		self.Gyro.Init()
		self.Gyro.Calibrate()
	

	def run(self):
		main_loop_speed = 1.0 / self.main_loop_frequency
		sampling_interval = 1.0 / self.sampling_frequency
		
		self.last_sampling_time = time.time()
		self.yawOffset = self.AccMag.flatHeading(self.AccMag.readMagRaw())
		
		while not self.killThread:
			time.sleep(main_loop_speed)
			now = time.time()
			if now >= (self.last_sampling_time + sampling_interval):
				self.dt = now - self.last_sampling_time
				self.last_sampling_time = now
				
				# read values
				self.gX, self.gY, self.gZ = self.Gyro.Get_CalOut_Value()
				aXYZ = self.AccMag.readAccRaw(True)
				
				self.mX, self.mY, self.mZ = self.AccMag.readMagRaw(False)
				
				pitch, roll = self.AccMag.pitch_roll(aXYZ)
				yaw = self.AccMag.flatHeading((self.mX, self.mY, self.mZ)) #- self.yawOffset
				
				

				self.pitch = round(pitch)
				self.roll = round(roll)
				self.yaw = round(yaw)
				
				# converted to deg/s
				#dAngleX, dAngleZ = ((self.angleX - self.lastAngleX)/self.dt, (self.angleZ - self.lastAngleZ)/self.dt)

				# filter
				#self.filterX = self.alpha * (self.lastFilterX + self.gX * self.dt) + (1 - self.alpha) * self.angleX
				#self.filterZ = self.alpha * (self.lastFilterZ + self.gZ * self.dt) + (1 - self.alpha) * self.angleZ

				self.filterPitch = self.alpha * (self.lastPitch + self.gX * self.dt) + (1 - self.alpha) * self.pitch
				self.filterRoll = self.alpha * (self.lastRoll + self.gY * self.dt) + (1 - self.alpha) * self.roll
				self.filterYaw = self.alpha * (self.lastYaw + self.gZ * self.dt) + (1 - self.alpha) * self.yaw

				# prep next round
				self.lastPitch, self.lastRoll, self.lastYaw = (self.pitch, self.roll, self.yaw)
				self.lastFilterPitch, self.lastFilterRoll, self.lastFilterYaw = (self.filterPitch, self.filterRoll, self.filterYaw)
				
				
if __name__ == "__main__":
	s = SensorReader()
	s.start()

	myXs = []
	myYs = []
	try:
		while 1:
			time.sleep(0.25)
			#print(s.gX, s.gY, s.gZ, s.angleX, s.angleZ, s.filterX, s.filterZ)

			x = s.filterPitch
			y = s.filterRoll
			z = s.filterYaw

			print(x, y, z)
			
	
	except KeyboardInterrupt:
		pass
	finally:	
		s.killThread = True
	
		time.sleep(1)
