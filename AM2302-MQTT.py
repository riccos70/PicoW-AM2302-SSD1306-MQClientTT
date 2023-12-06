# AM2302 with display and MQTT on PICO W device

import ujson
import dht 
import network
import time
import machine
from machine import Pin
from umqtt.simple import MQTTClient

with open('config.json', 'r') as f:
    config = ujson.load(f)

# Fill in your MQTT Broker details
mqtt_host = config['MQTT']['HOST']
mqtt_username = config['MQTT']['USERNAME']  
mqtt_password = config['MQTT']['PASSWORD']
mqtt_publish_temp_topic = config['MQTT']['TOPIC_TEMP01']
mqtt_publish_hum_topic = config['MQTT']['TOPIC_HUM01']
mqtt_client_id = config['MQTT']['CLIENT_ID']

# Fill in sensor details
dSensor = dht.DHT22(Pin(2))

def reset():
    print("Resetting...")
    time.sleep(5)
    machine.reset()

def main():
    print(f"Begin connection with MQTT Broker :: {mqtt_host}")
    mqttClient = MQTTClient(client_id=mqtt_client_id, server=mqtt_host, user=mqtt_username, password=mqtt_password, keepalive=60)
    mqttClient.connect()
    while True:

        # Read the data from sensor
        dSensor.measure()
        temp = dSensor.temperature()
        hum = dSensor.humidity()
        print(f'Temperature= {temp:.1f}C')
        print(f'Humidity= {hum:.1f}%')
        # Publish the data to the topics
        mqttClient.publish(mqtt_publish_temp_topic, str(temp))
        mqttClient.publish(mqtt_publish_hum_topic, str(hum))
        # Wait for interval time
        time.sleep(20)

if __name__ == "__main__":
    while True:
        try:
            main()
        except OSError as e:
            print("Error: " + str(e))
            reset()
