import pymorse

import socket
from PIL import Image
from base64 import decodestring
import ast
import time 
import numpy as np

HOST = "localhost"
VIDEO_PORT = 60000 
VELOCITIES_PORT = 60003
POSE_PORT = 60002
INTERFACE_PORT = 4000
MAX_SAMPLES=100



def open_socket(PORT):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST, PORT))
	return s
#s.send(b'id1 atrv.videocamera capture [1]\n')
def get_image():
	s=open_socket(VIDEO_PORT)
	buf=""
	done=False
	while not done:
			tmp=s.recv(4096).decode("utf-8")
			buf+=tmp
			#print(tmp,end="")
			if '}' in tmp:
				done=True
	obj_pic=ast.literal_eval(buf)
	s.close()
	return obj_pic
def get_velocities():
	s=open_socket(VELOCITIES_PORT)
	buf=""
	done=False
	while not done:
			tmp=s.recv(4096).decode("utf-8")
			buf+=tmp
			if '}' in tmp:
				done=True
	obj_vel=ast.literal_eval(buf)
	
	linear_x=obj_vel['linear_velocity'][0]
	angular_z=obj_vel['angular_velocity'][2]
	#print("X velocity: "+str(linear_x)+" anglular_z: "+str(angular_z))
	s.close()
	return (linear_x,angular_z)
def get_joystick_horizontal_axis():
	s=open_socket(INTERFACE_PORT)
	s.send(b'id1 atrv.joy get_local_data\n')
	buf=""
	done=False
	while not done:
			tmp=s.recv(4096).decode("utf-8")
			buf+=tmp
			print(tmp)
			if '}' in tmp:
				done=True
	obj=ast.literal_eval(buf[len("id1 SUCCESS "):])
	s.close()
	return obj['horizontal_axis']
def image_to_array(obj_pic):
	img_data=obj_pic['image']
	image = Image.frombytes('RGBA',(obj_pic['width'],obj_pic['height']),decodestring(img_data.encode("utf-8")))
	return np.array(image)
def save_image(obj_pic,filename):
	img_data=obj_pic['image']
	image = Image.frombytes('RGBA',(obj_pic['width'],obj_pic['height']),decodestring(img_data.encode("utf-8")))
	image.save(filename)

x_train=[]
y_train=[]


with pymorse.Morse("localhost", 4000) as simu:

	try:
		for i in range(1,400):
			#print("Getting image "+str(i))
			#save_image(get_image(),"pics/pic"+str(i)+".png")
			# Get the 'Pose' sensor datastream
			pose = simu.atrv.pose
			motion = simu.atrv.motion
			
			# Blocks until something is available
			arr=image_to_array(get_image())
			x_train.append(arr)
			
			actual_angle=get_joystick_horizontal_axis()
			y_train.append([-0.4*actual_angle])
			
			print("Step: "+str(i))
			motion.publish({"v": 4, "w": -0.4*actual_angle})
			simu.sleep(0.1)

	except pymorse.MorseServerError as mse:
		print('Oups! An error occured!')
		print(mse)
np_x_train=np.array(x_train)
np.save("x_train_set", np_x_train)
np_y_train=np.array(y_train)
np.save("y_train_set", np_y_train)

