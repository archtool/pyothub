Security
=============



User Login
------------

Login is handled by the login micro-service. All successfull logins are broadcast on the Login channel of the
communication bus. The message contains the following information:

* The session UUID
* The IP address from which this session was opened
* The time at which the session was opened
* The ID of the user
* The Group(s) the user is part of
* The OU(s) the user is part of

All other services listen to this channel, and will maintain their own list of authorized
sessions. Each request is matched against this list to verify its authenticity and authority.

Device Login
--------------

It is absolutely required that all communications are encrypted to prevent eavesdropping.
It is also required that all devices have their own key used for authentication, which can be revoked by the Hub.
For now, the key will be used as follows:

* During a challenge-response handshake the key is checked
* A simple session key is exchanged that is used for further encryption
* The session key is used to encrypt all messages
* The session is used for as long as the socket stays open

Common IoT Attacks
-----------------------

IoT devices interact with the real world, and thus the consequences of attacks can be far greater that
your average website. Also, the devices are often physically accessible for hackers.
Common attacks to be prevented are:

* Spoofing of data to confuse / abuse the backend
* Replay attacks, especially when part of the message is changed
* Man-in-the middle attacks, to either attack the backend or the device
* Analysis of a stolen device to reverse-engineer the protocol
* Running a device in a hacked sandbox, where e.g. the update server is spoofed.
* Publishing data to the hub that is routed to a device -- i.e. spoofing backend messages
  using the MQTT broker...

Key Functionality
-------------------

* Sending meterology data to the backend
* Sending alarms and other state changes to the backend
* Sending logs to the backend
* Receiving a new key
* Receiving commands from the backend
* Receiving software updates


Ideas
----------

Some ideas that may be worth implementing:

All requests must contain the time at which the request was issued, which must be no later than 1
minute old. This to prevent replay attacks. However, this also means that the (approximate) time
must be synchronised between server and device.

Software updates are served using the standard DEB utilities in Debian. The identity of the update server
must be checked by the device, otherwise it can easily be spoofed by a hacker.

The system depends on a separate MQTT broker, e.g. Mosquitto.

Questions
------------

How to safely send messages back to the devices? MQTT is too open to do this safely...
Anyone who can connect to the broker can send any message to the other clients.

It seems that websockets are easier to secure and contain than MQTT. At least outsiders
can not inject messages with websockets!