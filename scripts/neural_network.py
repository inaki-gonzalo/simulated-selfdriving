import pymorse
import Interface
import numpy as np
from keras.models import load_model

MODEL_FILENAME='model.h5'
HOST = "localhost"
INTERFACE_PORT = 4000
LINEAR_SPEED=3 #m/s

i=Interface.Interface(HOST,INTERFACE_PORT)
c=Interface.Convert()
model = load_model(MODEL_FILENAME)

with pymorse.Morse(HOST, INTERFACE_PORT) as simu:

	try:
		while True:
			
			motion = simu.atrv.motion
			#Get current screenshot and transform it into a numpy array.
			arr=c.image_to_4d_array(i.get_image())
			
			#Get an angle prediction from Neural network using current screenshot as input.
			desired_angle=model.predict(arr, batch_size=None,steps=1)
			print("Neural network Output: "+str(desired_angle))
			
			#Send command to simulated robot
			motion.publish({"v": LINEAR_SPEED, "w": float(desired_angle[0][0])})

			simu.sleep(0.1)

	except pymorse.MorseServerError as mse:
		print('Oups! An error occured!')
		print(mse)


