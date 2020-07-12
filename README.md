# Self-driving car in sim.
This project shows how to train a model to create a track following car.

# Data Collection
Start the Morse simulation server:
```
cd src; morse run simulation.py
```
Start the data colecting client:
```
cd scripts; python data_collector.py
``` 

# Training
Once you have collected some data create and train the model with:
```
cd scripts; python train.py
```

# Run in self-driving mode.
Start the Morse simulation server:
```
cd src; morse run simulation.py
```
Start the self-driving client:
```
cd scripts; python neural_network.py
``` 


