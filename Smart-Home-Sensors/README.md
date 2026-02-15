# Smart-Home-Sensors
This repository contains the sensor layer of a Smart Home IoT system. Its main purpose is to simulate or interface with home sensors, collect environmental and device data, and store it in a database for consumption by other system components.

# How To Run
### Create a Virtual Environment (Optional but Recommended)

#### Windows User

```
python -m venv <virtual_environment_name>

# activate it

<virtual_environment_name>\Scripts\activate
```

#### Linux User

```
python3 -m venv <virtual_environment_name>

# activate it

source <virtual_environment_name>/bin/activate
```

### Install the Dependencies
```
pip install -r requirements.txt
```

### Create .env file
And the and this line (uri of your MongoDb Cluster)
```
MONGODB_URI=mongodb+srv://<user>:<pass>@<host>/
```


```
sudo systemctl enable mosquitto
sudo systemctl start mosquitto
```
