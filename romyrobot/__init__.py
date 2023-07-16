import logging
from zeroconf import ServiceBrowser, Zeroconf, ServiceListener
import requests
import time


class RomyRobotServiceListener(ServiceListener):
    def __init__(self):
        self.ip_address = None
        self.port = None

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        if info:
            # Get the IP address and port of the robot
            self.ip_address = ".".join(map(str, info.addresses[0]))
            self.port = info.port


class RomyRobot:

    def __init__(self):
        self.ip_address = None
        self.port = 10009

    def find(self):
        zeroconf = Zeroconf()
        listener = RomyRobotServiceListener()
        browser = ServiceBrowser(zeroconf, "_aicu-http._tcp.local.", listener)

        try:
            # Wait until the robot is found
            while not listener.ip_address:
                time.sleep(0.1)
        finally:
            zeroconf.close()
        self.ip_address = listener.ip_address
        self.port = listener.port

    def get_info(self):
        # Use the get request get/robot_id to identify the robot instance
        response = requests.get(f"http://{self.ip_address}:{self.port}/get/robot_id")
        return response.json()


if __name__ == "__main__":
    robot = RomyRobot()
    robot.find()
    print(robot.get_info())

