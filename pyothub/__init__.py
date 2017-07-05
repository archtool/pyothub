""" PyOTHub: a hub for IOT devices that provides bi-directional communication and security

The project consists several parts: an MQTT server that handles updates from and to the devices,
and a REST API for managing the devices.

The main goal for this project is to be easy to deploy and flexible. It is currently not geared towards
large numbers of devices.

"""




class PyotHub:
    """ Implementation of the REST API for managing devices """
    def index(self):
        """ Retrieve the list of devices """
        pass
    def addDevice(self, device_id=None):
        """ Add a new device """
    def deleteDevice(self, device_id):
        """ Delete a device """
    def activateNewKey(self, device_id, key):
        """ Change the key that the device must use to authenticate itself """
    def sendMessage(self, device_id, msg):
        """ Send a specific message to the device """