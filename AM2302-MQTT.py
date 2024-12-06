# DS18B20 with MQTT on PICO W device

import ujson
import dht 
import network
import time
import random
import machine
import boot

from machine import Pin
from umqtt.simple import MQTTClient

with open('config.json', 'r') as f:
    config = ujson.load(f)

# Fill in your MQTT Broker details
mqtt_host = config['MQTT']['HOST']
mqtt_username = config['MQTT']['USERNAME']  
mqtt_password = config['MQTT']['PASSWORD']
ttype = config['TOPIC']['TYPE']
tarea = config['TOPIC']['AREA']
tzone = config['TOPIC']['ZONE']
mqtt_publish_topic = ttype+"/"+tarea+"/"+tzone
mqtt_client_id = f'publish-{random.randint(0, 1000)}'

# Fill in sensor details
dSensor = dht.DHT22(Pin(2))
mis01 = config['DATA']['MEAS01']
mis02 = config['DATA']['MEAS02']



def main():
    print(f"Starting connection with MQTT Broker :: {mqtt_host}")
    mqttClient = MQTTClient(client_id=mqtt_client_id, server=mqtt_host, user=mqtt_username, password=mqtt_password, keepalive=60)
    mqttClient.connect()
    print(f"Connected with MQTT Broker :: {mqtt_host}")
    while True:
        # Read the data from sensor
        boot.do_connect()
        dSensor.measure()
        temp = dSensor.temperature()
        hum = dSensor.humidity()
        msg = "{\"area\": \""+tarea+"\", \"zone\": \""+tzone+"\", \""+mis01+"\": " + str(temp) + ", \""+mis02+"\": " + str(hum) + "}"
        print(msg)
        # Publish the data to the topics
        mqttClient.publish(mqtt_publish_topic, msg)
        # Wait for interval time
        time.sleep(30)


if __name__ == "__main__":
    main()


