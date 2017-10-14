import RPi.GPIO as GPIO
import time

class Kickstand:
	PWM_FREQUENCY = 50 # hz	
	SERVO_MIN_DC = 2.5
	SERVO_MAX_DC = 12.5
	SERVO_NEUTRAL_DC = (SERVO_MIN_DC + SERVO_MAX_DC) / 2

	# SERVO_MOUNT_ANGLE = 15 # degrees
	# SERVO_VERTICAL = 90 + SERVO_MOUNT_ANGLE

	def __init__(self, pin, mount_offset = 1, start_extended = True):
		self.pin = pin
		self.mount_offset = mount_offset
		self.dc_extended = 7.5 + self.mount_offset
		self.dc_stored = 2.5
		self.extended = start_extended

		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.pin, GPIO.OUT)

		self.pwm = GPIO.PWM(self.pin, self.PWM_FREQUENCY)

		position = self.dc_extended if self.extended else self.dc_stored
		print(position)
		self.pwm.start(position) 

	def toggle(self):
		if self.extended:
			self.store()
		else:
			self.extend()

	def extend(self):
		self.extended = True
		self.pwm.ChangeDutyCycle(self.dc_extended)

	def store(self):
		self.extended = False
		self.pwm.ChangeDutyCycle(self.dc_stored)

	def extend_slowly(self):
		if self.extended:
			return False

		for i in self.frange(self.dc_stored, self.dc_extended, 0.25):
			self.pwm.ChangeDutyCycle(i)
			time.sleep(0.1)

		self.pwm.ChangeDutyCycle(self.dc_extended)
		return True


	def dismantle(self):
		self.pwm.stop()

	def frange(self, x, y, jump):
		while x < y:
			yield x
			x += jump

if __name__ == "__main__":
	kicker = Kickstand(18)
	time.sleep(0.5)
	kicker.store()
	time.sleep(1)
	kicker.extend_slowly()
	# kicker.extend()
	time.sleep(1)
	kicker.dismantle()
	GPIO.cleanup()
