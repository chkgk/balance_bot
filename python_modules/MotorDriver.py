import time
import RPi.GPIO as GPIO

class MotorDriver:
	PWM_FREQUENCY = 100

	def __init__(self, en1, m11, m12):
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BCM)

		self.enable_pin = en1
		self.motor_pin1 = m11
		self.motor_pin2 = m12

		# enable pins
		GPIO.setup(self.enable_pin, GPIO.OUT)
		
		#m1 
		GPIO.setup(self.motor_pin1, GPIO.OUT)
		GPIO.setup(self.motor_pin2, GPIO.OUT)

		GPIO.output(self.motor_pin1, GPIO.LOW)
		GPIO.output(self.motor_pin2, GPIO.LOW)

		self.current_speed = 0

		self.pwm = GPIO.PWM(self.enable_pin, self.PWM_FREQUENCY)
		self.pwm.start(self.current_speed)
	
	def set_direction(self, direction = False):
		if direction == "forward":
			GPIO.output(self.motor_pin1, GPIO.LOW)
			GPIO.output(self.motor_pin2, GPIO.HIGH)
		elif direction == "backward":
			GPIO.output(self.motor_pin1, GPIO.HIGH)
			GPIO.output(self.motor_pin2, GPIO.LOW)
		else:
			GPIO.output(self.motor_pin1, GPIO.LOW)
			GPIO.output(self.motor_pin2, GPIO.LOW)

	def set_speed(self, speed):
		if speed == 0:
			self.set_direction()

		if speed > 0:
			self.set_direction("forward")

		if speed < 0:
			self.set_direction("backward")


		if speed < -100:
			speed = -100

		if speed > 100:
			speed = 100

		self.current_speed = speed
		self.pwm.ChangeDutyCycle(abs(self.current_speed))


if __name__ == "__main__":
	m = MotorDriver(20, 6, 13)
	m.set_speed(50)
	time.sleep(1)
	m.set_speed(-20)
	time.sleep(1)
	m.set_speed(0)
	time.sleep(1)
	GPIO.cleanup()