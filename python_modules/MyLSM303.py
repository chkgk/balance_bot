from Adafruit_LSM303 import LSM303
import math

class MyLSM303(LSM303):
	#Acc Calibration Preset
	ACC_MIN_X = -1042.0  
	ACC_MIN_Y = -989.0  
	ACC_MIN_Z = -1149.0    
	ACC_MAX_X = 998.0    
	ACC_MAX_Y = 1130.0    
	ACC_MAX_Z = 1021.0    

	accXoffset = (ACC_MIN_X + ACC_MAX_X)/2
	accYoffset = (ACC_MIN_Y + ACC_MAX_Y)/2
	accZoffset = (ACC_MIN_Z + ACC_MAX_Z)/2

	# Mag Calibration Preset
	MAG_MIN_X = -628.0    #-629 
	MAG_MIN_Y = -705.0   #-719
	MAG_MIN_Z = -717.0    #-678
	MAG_MAX_X = 496.0    #569
	MAG_MAX_Y = 523.0   #488
	MAG_MAX_Z = 442.0    #429
	DECLINATION = 36.94 / 1000 #Heidelberg declination +2 8' from miliradians to radians
	
	def setCalibration(self, aXmin, aYmin, aZmin, aXmax, aYmax, aZmax, mXmin, mYmin, mZmin, mXmax, mYmax, mZmax):
		# Acc Calibration Preset
		self.ACC_MIN_X = aXmin   
		self.ACC_MIN_Y = aYmin  
		self.ACC_MIN_Z = aZmin    
		self.ACC_MAX_X = aXmax   
		self.ACC_MAX_Y = aYmax   
		self.ACC_MAX_Z = aZmax   

		# Mag Calibration Preset
		self.MAG_MIN_X = mXmin
		self.MAG_MIN_Y = mYmin  
		self.MAG_MIN_Z = mZmin   
		self.MAG_MAX_X = mXmax  
		self.MAG_MAX_Y = mYmax 
		self.MAG_MAX_Z = mZmax   

		#calc offset
		self.accXoffset = (self.ACC_MIN_X + self.ACC_MAX_X)/2
		self.accYoffset = (self.ACC_MIN_Y + self.ACC_MAX_Y)/2
		self.accZoffset = (self.ACC_MIN_Z + self.ACC_MAX_Z)/2
		

	def readMagRaw(self, uncalibrated=False):
		(accX, accY, accZ), (magX, magY, magZ) = self.read()

		if uncalibrated:
			mag = (magX, magY, magZ)
		else: # bullshit below?
			# print (self.MAG_MIN_X)
			
			# hard iron
			magX -= (self.MAG_MIN_X + self.MAG_MAX_X) / 2
			magY -= (self.MAG_MIN_Y + self.MAG_MAX_Y) / 2
			magZ -= (self.MAG_MIN_Z + self.MAG_MAX_Z) / 2
			
			# soft iron scaling!
			#magCX = (magX - self.MAG_MIN_X)/(self.MAG_MAX_X - self.MAG_MIN_X)*2 - 1.0
			#magCY = (magY - self.MAG_MIN_Y)/(self.MAG_MAX_Y - self.MAG_MIN_Y)*2 - 1.0
			#magCZ = (magZ - self.MAG_MIN_Z)/(self.MAG_MAX_Z - self.MAG_MIN_Z)*2 - 1.0
			mag = (magX, magY, magZ)
		return mag


	def readAccRaw(self, uncalibrated=False):
		(accX, accY, accZ), (magX, magY, magZ) = self.read()
		if uncalibrated:
			acc = (accX, accY, accZ)
		else:
			acc = (accX-self.accXoffset, accY-self.accYoffset, accZ-self.accZoffset)
		return acc

	
	def pitch_roll(self, aXYZ_tuple):
		x, y, z = aXYZ_tuple
		pitch = math.degrees(math.atan2(y,z))
		roll = -math.degrees(math.atan2(x,z))
		return (pitch, roll)
		
	def normalize(self, aXYZ_tuple):
		x, y, z = aXYZ_tuple
		accXnorm = x/math.sqrt(x*x + y*y + z*z)
		accYnorm = y/math.sqrt(x*x + y*y + z*z)
		accZnorm = z/math.sqrt(x*x + y*y + z*z)
		return (accXnorm, accYnorm, accZnorm)


	def flatHeading(self, mXYZ_tuple):
		mX, mY, mZ = mXYZ_tuple
		heading = 180 * math.atan2(-mX, -mY) / math.pi
		#if heading < 0:
		#	heading += 360
		return heading

	
