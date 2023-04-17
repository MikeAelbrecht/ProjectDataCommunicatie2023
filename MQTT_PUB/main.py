from machine import Pin, SPI
from time import sleep, sleep_ms
from mcp3008 import MCP3008
import network
from simple import MQTTClient

ssid = "MiniRouter_M"
password = "MikeAelbrecht1"

spi = SPI(0, sck=Pin(2),mosi=Pin(3),miso=Pin(4), baudrate=100000)
cs = Pin(22, Pin.OUT)
cs.value(1) # disable chip at start

chip = MCP3008(spi, cs)

c = None

topic = "/data2023/data"
    
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    print("Connected to the WiFi")
    
def connect_mqtt():
    global c
    c = MQTTClient("pico_master", "broker.hivemq.com")

def read_data():
    value1 = chip.read(0, True)
    value2 = chip.read(1, True)
    value3 = chip.read(4, True)
    value4 = chip.read(7, True)
    
    if value1 == 0:
        print(f"KNOP1   {value1}")
        send_data("ra")
    if value2 == 0:
        print(f"KNOP2   {value2}")
        send_data("ga")
    if value3 == 0:
        print(f"KNOP3   {value3}")
        send_data("ba")
    if value4 == 0:
        print(f"KNOP4   {value4}")
        send_data("au")
    
    sleep(0.1)

def send_data(_data):
    data = b"" + _data
    c.connect()
    c.publish(topic, data)
    c.disconnect()
    
if __name__ == "__main__":
    connect_wifi()
    connect_mqtt()
    
    while True:
        read_data()
