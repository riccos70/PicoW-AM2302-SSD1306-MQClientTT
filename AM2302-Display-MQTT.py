# AM2302 with display and MQTT on PICO W device

import ujson
import dht 
import network
import time
import machine
from ssd1306 import SSD1306_I2C
from machine import Pin, I2C
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

#Fill in OLED details
WIDTH =128 
HEIGHT= 64
i2c=I2C(0,scl=Pin(1),sda=Pin(0),freq=200000)
oled = SSD1306_I2C(WIDTH,HEIGHT,i2c)

def reset():
    print("Resetting...")
    time.sleep(5)
    machine.reset()

def readDHT():
    try:
        dSensor.measure()
        temp = dSensor.temperature()
        hum = dSensor.humidity()
        print(f'Temperature= {temp:.1f}C')
        print(f'Humidity= {hum:.1f}%')
        return temp, hum
    except OSError as e:
        print('Failed to read data from DHT sensor')

def displayDhtData(t,h):
    try:
        oled.fill(0)
        oled.text("Temp:", 0, 10)
        oled.text(str(t), 80, 10)
        oled.text("C", 120, 10)
        oled.text("Humidity:", 0, 30)
        oled.text(str(h), 80, 30)
        oled.text("%", 120, 30)
        oled.show()
    except OSError as e:
        print(f'Failed to display data on OLED. Message: {e}')    
    
def main():
    print(f"Begin connection with MQTT Broker :: {mqtt_host}")
    mqttClient = MQTTClient(client_id=mqtt_client_id, server=mqtt_host, user=mqtt_username, password=mqtt_password, keepalive=60)
    mqttClient.connect()
    while True:
        # Read the data from sensor
#        temp, hum= readDHT()
        dSensor.measure()
        temp = dSensor.temperature()
        hum = dSensor.humidity()
        print(f'Temperature= {temp:.1f}C')
        print(f'Humidity= {hum:.1f}%')
        # Display the data on OLED
        displayDhtData(temp, hum)
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
