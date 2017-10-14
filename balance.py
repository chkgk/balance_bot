import time
import math

from python_modules.MotorDriver import MotorDriver
from python_modules.SensorReader import SensorReader
from python_modules.Kickstand import Kickstand

kicker = Kickstand(18)
kicker.store()

motor1 = MotorDriver(20, 6, 13,)
motor2 = MotorDriver(21, 19, 26)
sensors = SensorReader()

main_loop_frequency = 250 # hz
action_frequency = 50 # hz

main_loop_speed = 1.0 / main_loop_frequency
action_interval = 1.0 / action_frequency

last_action_time = time.time()
dt = 0.0

# now we prepare for the PID controller
# we are interested in not falling over. 
# we fall over, if Z-angle != 0
# => Z-angle == 0 is our goal!
goal = 90

# let's assume for now, that we are perfectly upright
previous_error = 0
current_error = 0

# we will need to tune three gain factors:
P = 20.0 # proportional
I = 0.0 # integral
D = 0.0 # derivative

# and we initialize the factors themselves:
proportional = 0.0
integral = 0.0
derivative = 0.0

# offset 
offsetX = 0.0

goal += offsetX

try:
	sensors.start()
	
	print ("all threads are running")

	#kicker.store()

	# main control loop
	while 1:
		time.sleep(main_loop_speed)
		now = time.time()
		
		if now >= (last_action_time + action_interval):
			dt = now - last_action_time
			last_action_time = now
			
			# we need to know how far away from our goal we are:
			# current error = goal - current z-Angle
			current_error = goal - sensors.filterPitch
			
			# calculate the values for the three factors
			proportional = current_error
			integral += dt * current_error
			derivative = (current_error - previous_error) / dt
			
			# output is sum of the three, each multiplied with its gain
			output = P * proportional + I * integral + D * derivative
			
			# for positive errors, we are leaning backwards
			# to correct this we need to drive backwards, i.e. 
			# motor speed setting needs to be negative output
			motor_speed = output
			
			# also, we need to limit motor speed to -100 to +100
			if motor_speed > 100:
				motor_speed = 100
			
			if motor_speed < -100:
				motor_speed = -100
			
			# for debugging we will output current errors and output:
			print(current_error, motor_speed)
			
			# now we send it to motors
			motor1.set_speed(motor_speed)
			motor2.set_speed(motor_speed)

	
except KeyboardInterrupt:
	pass
finally:
	sensors.killThread = True
