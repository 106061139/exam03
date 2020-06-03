import serial
import time
import paho.mqtt.client as paho

# https://os.mbed.com/teams/mqtt/wiki/Using-MQTT#python-client


# MQTT broker hosted on local machine

mqttc = paho.Client()


# Settings for connection

# TODO: revise host to your ip

host = "192.168.1.113"

topic = "velocity"
# Callbacks

def on_connect(self, mosq, obj, rc):

      print("Connected rc: " + str(rc))


def on_message(mosq, obj, msg):

      print("[Received] Topic: " + msg.topic + ", Message: " + str(msg.payload) + "\n");


def on_subscribe(mosq, obj, mid, granted_qos):

      print("Subscribed OK")


def on_unsubscribe(mosq, obj, mid, granted_qos):

      print("Unsubscribed OK")


# Set callbacks

mqttc.on_message = on_message

mqttc.on_connect = on_connect

mqttc.on_subscribe = on_subscribe

mqttc.on_unsubscribe = on_unsubscribe
# Connect and subscribe


mqttc.subscribe(topic, 0)

# XBee setting
serdev = '/dev/ttyUSB0'
s = serial.Serial(serdev, 9600)
s.write("+++".encode())
char = s.read(2)
print("Enter AT mode.")
print(char.decode())
s.write("ATMY 0x233\r\n".encode())
char = s.read(3)
print("Set MY <BASE_MY>.")
print(char.decode())
s.write("ATDL 0x232\r\n".encode())
char = s.read(3)
print("Set DL <BASE_DL>.")
print(char.decode())
s.write("ATID 0x0\r\n".encode())
char = s.read(3)
print("Set PAN ID <PAN_ID>.")
print(char.decode())
s.write("ATWR\r\n".encode())
char = s.read(3)
print("Write config.")
print(char.decode())
s.write("ATMY\r\n".encode())
char = s.read(4)
print("MY :")
print(char.decode())
s.write("ATDL\r\n".encode())
char = s.read(4)
print("DL : ")
print(char.decode())
s.write("ATCN\r\n".encode())
char = s.read(3)
print("Exit AT mode.")
print(char.decode())
print("start sending RPC")
while True:
    # send RPC to remote
    s.write("/acce_value/run\r".encode())
    line=s.readline()
    print(line.decode())
    # Publish messages from Python
    ret = mqttc.publish(topic, "Message from Python!\n", qos=0)
    if (ret[0] != 0):

        print("Publish failed")

    mqttc.loop()
    time.sleep(1)
mqttc.loop_forever()
s.close()
