
import sys
sys.path.append('../../Software/Python/')   #This is so we can use the grovepi libraries
sys.path.append('../../Software/Python/grove_rgb_lcd')
import paho.mqtt.client as mqtt
import time

import RPi.GPIO as GPIO

servoPIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)
GPIO.setwarnings(False)
p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
p.start(2.5) # Initialization

import grovepi
from grove_rgb_lcd import *

import multiprocessing      
import threading           
lock = threading.Lock()   
i2c_lock = multiprocessing.RLock()
state = 0

grovepi.pinMode(buzzer,"OUTPUT")
grovepi.pinMode(led,"OUTPUT")
buzzer = 8
led = 3


def custom_callback_fire(client, userdata, message):  
    s = str(message.payload, "utf-8")
    if state == 1:
        if s == "fire":
            p.ChangeDutyCycle(4.0)
            time.sleep(0.5)
            p.ChangeDutyCycle(2.5)
            client.publish("avipi/Hit", "Hostile Destroyed")
        elif s == "warn":
            grovepi.digitalWrite(buzzer, 1)
            count = 5
            while count != 0:
                grovepi.digitalWrite(led, 1)
                time.sleep(1)
                grovepi.digitalWrite(led, 0)
                count = count - 1
            grovepi.digitalWrite(buzzer, 0)
    elif state == 0:
        client.publish("avipi/Hit", "No Target in Range")
   

def on_connect(client, userdata, flags, rc): 
    print("Connected to server (i.e., broker) with result code "+str(rc))
    client.message_callback_add("avipi/fire", custom_callback_fire)

    client.subscribe("avipi/fire")
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))


if __name__ == '__main__':
    print("test")
    ultrasonic_ranger = 4 
    client = mqtt.Client()  
    client.on_message = on_message 
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60) 
    client.loop_start() 
    while True:
        
        with i2c_lock: 
            try:
                ultrasonic_value = grovepi.ultrasonicRead(ultrasonic_ranger) 
                print(str(ultrasonic_value))
                if ultrasonic_value < 200:
                    state = 1
                    sensorstring = str(ultrasonic_value)
                    client.publish("avipi/targetAcquired", "target acquired at " +
                    sensorstring)
                    while True:
                        ultrasonic_value = grovepi.ultrasonicRead(ultrasonic_ranger) 
                        if ultrasonic_value > 350:
                            state = 0
                            client.publish("avipi/targetAcquired", "target lost")
                            break
            except KeyboardInterrupt: 
                break
            except IOError:
                print("IOERROR") 
        time.sleep(1) 

            

