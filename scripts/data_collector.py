import pymorse
import numpy as np
import Interface

HOST = "localhost"
INTERFACE_PORT = 4000
TOTAL_STEPS=1000
x_train=[]
y_train=[]

#Save training data to disk	
def save_trainning_data():
	np_x_train=np.array(x_train)
	np.save("x_train_set", np_x_train)
	np_y_train=np.array(y_train)
	np.save("y_train_set", np_y_train)

i=Interface.Interface(HOST,INTERFACE_PORT)
c=Interface.Convert()
with pymorse.Morse(HOST,INTERFACE_PORT) as simu:
	try:
		motion = simu.atrv.motion
		
		for step in range(TOTAL_STEPS):	
			
			#Get a screenshot from the simulator and store it for the CNN	
			image=i.get_image()
			arr=c.image_to_3d_array(image)
			x_train.append(arr)
			
			#Get the current joystick position and convert to radians per second
			joystick_pos=i.get_joystick_horizontal_axis()
			desired_angular_velocity=c.joystick_to_radians_per_second(joystick_pos)
			
			#Store desired angular position as the desired output for the CNN
			y_train.append([desired_angular_velocity])
			
			print("Step: "+str(step))
			
			motion.publish({"v": 4, "w": desired_angular_velocity})
			simu.sleep(0.1)

	except pymorse.MorseServerError as mse:
		print('Oups! An error occured!')
		print(mse)
	
save_trainning_data()
