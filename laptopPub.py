"""EE 250L Lab 04 Starter Code
MY TEAMMATES: JUST ME
GITHUB REPO: https://github.com/usc-ee250-fall2020/lab05-the-a-team.git
Run vm_publisher.py in a separate terminal on your VM."""

import paho.mqtt.client as mqtt
import time
from pynput import keyboard

def custom_callback_Hit(client, userdata, message):
    s = str(message.payload, "utf-8")
    print(s)
    

def custom_callback_targetAcquired(client, userdata, message):
    s = str(message.payload, "utf-8")
    print(s)

def on_connect(client, userdata, flags, rc): #prints a message if server connection success
    print("Connected to server (i.e., broker) with result code "+str(rc))
    client.message_callback_add("avipi/Hit", custom_callback_Hit) #adds the custom callbacks for
    client.message_callback_add("avipi/targetAcquired", custom_callback_targetAcquired) #both of these topics

    #subscribe to the ultrasonic ranger topic here
    client.subscribe("avipi/Hit") #Then subscribes to both topics to be ready for when the pi publishes
    client.subscribe("avipi/targetAcquired")

def on_message(client, userdata, msg): #this is not used in the context of this lab, publisher should not receive messages
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

if __name__ == '__main__':
    
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
        else:
            print("Invalid command")
        value = ""        

