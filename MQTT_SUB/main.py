import time
from machine import Pin, I2C

from wifi import Wifi
from simple import MQTTClient

ssid = "MiniRouter_M"
password = "MikeAelbrecht1"

mqtt_client = "pico_slave"
mqtt_server = "broker.hivemq.com"

i2c_addres = 19

Wifi(ssid, password)
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)

def sub_cb(topic, msg):
    msg = msg.decode()
    print(msg)
    if msg == "ra":
        i2c.writeto(i2c_addres, b"ra")
    elif msg == "ga":
        i2c.writeto(i2c_addres, b"ga")
    elif msg == "ba":
        i2c.writeto(i2c_addres, b"ba")
    elif msg == "au":
        i2c.writeto(i2c_addres, b"au")
    else:
        print(f"An invalid message")

if __name__ == "__main__":
    mqtt = MQTTClient(mqtt_client, mqtt_server)
    mqtt.set_callback(sub_cb)
    mqtt.connect()
    mqtt.subscribe(b"/data2023/data")
    
    while True:
        mqtt.check_msg()
        time.sleep(1)
        
    mqtt.disconnect()
    
    

