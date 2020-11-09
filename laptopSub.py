"""EE 250L Lab 04 Starter Code
MY TEAMMATES: JUST ME
GITHUB REPO: https://github.com/usc-ee250-fall2020/lab05-the-a-team.git

Run vm_subscriber.py in a separate terminal on your VM."""

import paho.mqtt.client as mqtt
import time

def custom_callback_ultrasonicRanger(client, userdata, message):
    #the third argument is 'message' here unlike 'msg' in on_message 
    s = str(message.payload, "utf-8")
    if (s.isnumeric()): #double triple checks that the ultrasonic sent a number
        print(s)
def custom_callback_button(client, userdata, message):
    #the third argument is 'message' here unlike 'msg' in on_message 
    s = str(message.payload, "utf-8")
    if (s == "Button pressed!"): #checks if the correct text is displayed
        print(s)

def on_connect(client, userdata, flags, rc): #prints a message if server connection success
    print("Connected to server (i.e., broker) with result code "+str(rc))
    client.message_callback_add("avipi/ultrasonicRanger", custom_callback_ultrasonicRanger) #adds the custom callbacks for
    client.message_callback_add("avipi/button", custom_callback_button) #both of these topics

    #subscribe to the ultrasonic ranger topic here
    client.subscribe("avipi/ultrasonicRanger") #Then subscribes to both topics to be ready for when the pi publishes
    client.subscribe("avipi/button")

#Default message callback. Please use custom callbacks. Not used in the context of this lab, we set custom callbacks
def on_message(client, userdata, msg):
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
            

