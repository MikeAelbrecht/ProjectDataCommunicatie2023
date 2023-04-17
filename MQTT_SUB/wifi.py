import network
import time

class Wifi:
    def __init__(self, ssid, password):
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.wlan.connect(ssid, password)
        
        max_wait = 10
        while max_wait > 0:
            if self.wlan.status() < 0 or self.wlan.status() >= 3:
                break
            max_wait -= 1
            print("Waiting for connection...")
            time.sleep(1)
        
        if self.wlan.status() != 3:
            raise RuntimeError("Failed to connect to the network")
        else:
            print(f"Connected to {ssid}")
    
    def get_ip(self):
        self.status = self.wlan.ifconfig()
        print(f"IP: {self.status[0]}")
        return self.status[0]

