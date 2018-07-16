import pymorse

import socket
from PIL import Image
from base64 import decodestring
import ast
import time 
import numpy as np

TCP_BUFF_SIZE=4096

#This class communicates with the Morse simulator using raw tcp.
class Interface:
	def __init__(self , host , interface_port):
		self.host = host
		self.interface_port = interface_port
		ports=self.get_all_stream_ports()
		self.VIDEO_PORT=ports['atrv.POV_robot']
		
	#Open TCP sockect to communicate with Morse sim
	def open_socket(self,port):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((self.host, port))
		return s
		
	#Gets all streams available in the simulator.
	def get_all_stream_ports(self):
		s=self.open_socket(self.interface_port)
		s.send(b'id1 simulation get_all_stream_ports\n')
		buf=""
		done=False
		while not done:
				tmp=s.recv(TCP_BUFF_SIZE).decode("utf-8")
				buf+=tmp
				if '}' in tmp:
					done=True
		obj=ast.literal_eval(buf[len("id1 SUCCESS "):])
		s.close()
		return obj	
	
	#Gets screenshot from Morse sim	
	#Returns a dictionary
	#The image is an RGBA base64 encoded stored in key 'image'
	#It also include width and height 
	def get_image(self):
		s=self.open_socket(self.VIDEO_PORT)
		buf=""
		done=False
		while not done:
				tmp=s.recv(TCP_BUFF_SIZE).decode("utf-8")
				buf+=tmp
				if '}' in tmp:
					done=True
		obj_pic=ast.literal_eval(buf)
		s.close()
		return obj_pic
	
	#Get current position of joystick.	returns a float from -1 to 1.
	def get_joystick_horizontal_axis(self):
		s=self.open_socket(self.interface_port)
		s.send(b'id1 atrv.joy get_local_data\n')
		buf=""
		done=False
		while not done:
				tmp=s.recv(TCP_BUFF_SIZE).decode("utf-8")
				buf+=tmp
				print(tmp)
				if '}' in tmp:
					done=True
		obj=ast.literal_eval(buf[len("id1 SUCCESS "):])
		s.close()
		return obj['horizontal_axis']

#This class converts the different data types used. 
class Convert:		
	def __init__(self):
		print("init convert")
		
	# converts the dictionary response from get_image to a numpy 3d array	
	def image_to_3d_array(self,obj_pic):
		img_data=obj_pic['image']
		image = Image.frombytes('RGBA',(obj_pic['width'],obj_pic['height']),decodestring(img_data.encode("utf-8")))
		return np.array(image)
		
	# converts the dictionary response from get_image to a numpy 4d array	
	def image_to_4d_array(self,obj_pic):
		img_data=obj_pic['image']
		image = Image.frombytes('RGBA',(obj_pic['width'],obj_pic['height']),decodestring(img_data.encode("utf-8")))
		arr_3d=np.array(image)
		arr_4d=np.resize(arr_3d,(1,obj_pic['width'],obj_pic['height'],4))
		return arr_4d
	
	def joystick_to_radians_per_second(self,joystick_pos):
		conversion_factor=-0.4 #This value was found experimentally
		return conversion_factor*joystick_pos 

