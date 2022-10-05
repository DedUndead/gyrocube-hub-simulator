# Hub Simulator for Gyrocube project

The script provides simple and easy-to-maintenance interface fpr Gyrocube project.

### Scenarios

Hub Simulator script provides several simple scenarios that simulate communication.<br>
They can be easily configured by passing parameters to respective functions.

#### Activa scenario

In active scenario, cubes dynamically join the network and can be periodically flipped.

#### Flipping scenario

In flipping scenario, cubes are already in the network and are periodically flipped.

### Usage

Using conda:
```
conda env create -f environment.yml
conda activate hubsim
```

Using vanilla python:
```
pip install paho-mqtt
```

After that, configure MQTT server address, port and desired scenario in main.py.<br>
`python main.py` to run the scenario.
