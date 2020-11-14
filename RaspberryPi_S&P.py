"""EE 250L Lab 04 Starter Code
MY TEAMMATES: JUST ME
GITHUB REPO: https://github.com/usc-ee250-fall2020/lab05-the-a-team.git
Run rpi_pub_and_sub.py on your Raspberry Pi."""
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

import multiprocessing      #I created both a normal lock and an i2c reentrant lock to debug some
import threading            #very strange issues (including a race condition)
lock = threading.Lock()     #although I dont use both in the code, I see no reason to delete them
i2c_lock = multiprocessing.RLock()
state = 0


def custom_callback_fire(client, userdata, message):  
    #If the word fire is typed from the laptop publisher, we fire one bullet
    # by activating the arduino
    if state == 1:
        p.ChangeDutyCycle(4.0)
        time.sleep(0.5)
        p.ChangeDutyCycle(2.5)
        client.publish("avipi/Hit", "Hostile Destroyed")
    elif state == 0:
        client.publish("avipi/Hit", "No Target in Range")
   

def on_connect(client, userdata, flags, rc): #When the rpi connects to the server, it should print the success message
                                            #Then add the custom callback for when the word fire comes from the laptop
                                            #then subscribe to the corresponding topic
    print("Connected to server (i.e., broker) with result code "+str(rc))
    client.message_callback_add("avipi/fire", custom_callback_fire)

    #subscribe to topics of interest here
    client.subscribe("avipi/fire")
#Default message callback. Please use custom callbacks. I believe this callback is never used in the context of this lab
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))


if __name__ == '__main__':
    print("test")
    ultrasonic_ranger = 4 #sets the pin for the ultrasonic, button, and led, and the initial state of the rgb and button
    client = mqtt.Client()  #starts client as the client
    client.on_message = on_message #primes the client for responding to a connection or message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60) #connects client to broker
    client.loop_start() #begins accepting messages from broker
    while True:
        
        with i2c_lock: #locks the grovepi functions to prevent race condition
            try:
                ultrasonic_value = grovepi.ultrasonicRead(ultrasonic_ranger) #reads a value from ultrasonic
                print(str(ultrasonic_value))
                if ultrasonic_value < 200:
                    state = 1
                    sensorstring = str(ultrasonic_value) #converts it to a string for consistency
                    client.publish("avipi/targetAcquired", "target acquired at " +
                    sensorstring) #publishes it to the ultrasonicRanger topic
                    while True:
                        ultrasonic_value = grovepi.ultrasonicRead(ultrasonic_ranger) #reads a value from ultrasonic
                        if ultrasonic_value > 350:
                            state = 0
                            client.publish("avipi/targetAcquired", "target lost")
                            break
            except KeyboardInterrupt: #These are some exceptions that were used in testing. They do not do anything.
                break
            except IOError:
                print("IOERROR") 
        time.sleep(1) #Sleep for one second

            

