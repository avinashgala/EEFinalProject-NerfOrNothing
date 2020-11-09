"""EE 250L Lab 04 Starter Code
MY TEAMMATES: JUST ME
GITHUB REPO: https://github.com/usc-ee250-fall2020/lab05-the-a-team.git
Run vm_publisher.py in a separate terminal on your VM."""

import paho.mqtt.client as mqtt
import time
from pynput import keyboard

def on_connect(client, userdata, flags, rc): #print a message if we connect successfully
    print("Connected to server (i.e., broker) with result code "+str(rc))

    #subscribe to topics of interest here
    #we don't subscribe to topics here since this is a publisher
#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg): #this is not used in the context of this lab, publisher should not receive messages
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))
"""
def on_press(key): #if a key is pressed
    try: 
        k = key.char # single-char keys
    except: 
        k = key.name # other keys
    
    if k == 'w':  #if w a s d are pressed, we print it to the vm and publish it to the topic "avipi/lcd"
        print("w")  #additionally, if a or d are pressed, we publish LED_ON or LED_OFF to topic avipi/led
        client.publish("avipi/lcd", k)
        #send "w" character to rpi
    elif k == 'a':
        print("a")
        # send "a" character to rpi
        #send "LED_ON"
        client.publish("avipi/lcd", k)
        client.publish("avipi/led", "LED_ON")
    elif k == 's':
        print("s")
        client.publish("avipi/lcd", k)
        # send "s" character to rpi
    elif k == 'd':
        print("d")
        # send "d" character to rpi
        # send "LED_OFF"
        client.publish("avipi/lcd", k)
        client.publish("avipi/led", "LED_OFF")
"""

if __name__ == '__main__':
    #setup the keyboard event listener
    lis = keyboard.Listener(on_press=on_press)
    lis.start() # start to listen on a separate thread
    
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()

    while True:
        #print("delete this line")
        time.sleep(1)
        value = input()
        if value == "fire" or value == "warn":
            client.publish("avipi/fire", value)
        value = ""        

