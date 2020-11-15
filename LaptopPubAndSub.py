
import paho.mqtt.client as mqtt
import time

def custom_callback_Hit(client, userdata, message):
    s = str(message.payload, "utf-8")
    print(s)
    

def custom_callback_targetAcquired(client, userdata, message):
    s = str(message.payload, "utf-8")
    print(s)

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    client.message_callback_add("avipi/Hit", custom_callback_Hit) 
    client.message_callback_add("avipi/targetAcquired", custom_callback_targetAcquired) 

    client.subscribe("avipi/Hit") 
    client.subscribe("avipi/targetAcquired")

def on_message(client, userdata, msg): 
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

if __name__ == '__main__':
    
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()

    while True:
        time.sleep(1)
        value = input()
        if value == "fire" or value == "warn":
            client.publish("avipi/fire", value)
        else:
            print("Invalid command")
        value = ""        

