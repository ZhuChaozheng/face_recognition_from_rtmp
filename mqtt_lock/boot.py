# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import micropython
import uos, machine
import gc
import time
from machine import Timer
from robust import MQTTClient
from machine import Pin,PWM
import network
import socket
import os
#import webrepl
#webrepl.start()
global TOPIC 
global TOPIC1 
global stasus
global tim
tim = Timer(-1)
status = Pin(16,Pin.OUT)
lock = Pin(14,Pin.OUT)
button = Pin(13,Pin.IN)


lock_on_flag = 0
lock_five_off = 0
def sub_cb(topic, msg):
    global lock_on_flag
    if msg == b"on":
        lock_on_flag = 1
        try:
            c.publish(topic=b"lock_confirm",msg="on")
        except OSError as e:
            machine.reset()
    print((topic, msg))


TOPIC = b"hello"
TOPIC1 = b"lock"
global A_Name,Apass

def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect("secret", "1.1.1.ping+..")
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())

ap = network.WLAN(network.AP_IF)
ap.config(essid="EasyMqtt", authmode=network.AUTH_WPA_WPA2_PSK, password="UsemqttN")
ap.active(True)

STAconfig = Pin(12,Pin.IN)

lock(1)
status(0)
do_connect()
clientidentity = str(machine.unique_id())+str(os.urandom(5))
clientidentity.replace("b","")
clientidentity.replace("'","")
c = MQTTClient(clientidentity,'10.196.83.16',port=1883,keepalive= 40)
c.DEBUG = True
c.set_callback(sub_cb)
try:
    c.connect(clean_session=False)
except OSError as e:
    machine.reset()
print('connected to mqtt')
try:
    c.subscribe(b"lock")
except OSError as e:
    machine.reset()
print('lock subscribed')
status(1)

while 1:
    try:
        c.sock.setblocking(False)
        c.wait_msg()
    except OSError as e:
        print("main restart")
        machine.reset()

    if button.value() == 0: #button pressed
       lock_on_flag = 1
    
    if lock_on_flag == 1:
       lock_on_flag = 0
       lock_five_off = 250
       print("lock on sub")
       lock(0)

    if lock_five_off>0 :
        lock_five_off = lock_five_off - 1
    if lock_five_off == 0:
        lock(1)
    print("i am checking everything")
    time.sleep(0.02)
    gc.collect()
    
gc.collect()
