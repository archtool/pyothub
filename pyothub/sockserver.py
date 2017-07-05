"""


Device Authentication:
========================

When a device connects to the server, it receives a challenge from the server in a JSON message:

    {"challenge": "<random challenge>"}

The device must reply with a response:

    { "challenge": "<the original challenge",
      "deviceid": "<the device ID string",
      "algorithm": "<algorithm name>",   # e.g. sha256
      "response": "<the response string>"
    }

The response should be calculated calculated with (in Python):

    h = hashlib.new("<algorithm>")
    h.update(<deviceid>)
    h.update(<devicekey>)
    h.update(<challenge>)
    response = h.hexdigest()

So the security relies on the deviceid and device key. The deviceid is
exchanged openly, so it is not secret. The key however is NOT exchanged, it
remains secret even over insecure networks.

The device determines which algorithm to use for calculating the hash.
"""

import asyncio
import websockets
import zmq
import json
import uuid
import model
import hashlib
import traceback
from collections import namedtuple


ChallengeResponse = namedtuple('ChallengeResponse', ['deviceid', 'challenge', 'response', 'algorithm'])

class Unauthorized(RuntimeError):
    pass


DEBUG = True



async def hello(websocket, path):
    try:
        # Send the challenge
        challenge = uuid.uuid4().hex
        await websocket.send(json.dumps({'challenge': challenge}))

        # Get the response and check it
        msg_raw = await websocket.recv()
        print("> {}".format(msg_raw))
        msg = json.loads(msg_raw)

        if msg.get('challenge', '') != challenge:
            raise Unauthorized('Please supply the correct challenge in the response')
        if not msg.get('deviceid', ''):
            raise Unauthorized('Please supply the deviceid')
        if not msg.get('response', ''):
            raise Unauthorized('Please supply the response')
        if not msg.get('algorithm', '') in ['sha256', 'sha512']:
            raise Unauthorized('Please supply an acceptable hash algorithm')

        msg = ChallengeResponse(**msg)

        # Calculate what the response should be
        devicekey = model.getDeviceKey(msg.deviceid)
        if not devicekey:
            raise RuntimeError('Unknown deviceid')
        h = hashlib.new(msg.algorithm)
        h.update(msg.deviceid.encode('utf8'))
        h.update(devicekey.encode('utf8'))
        h.update(challenge.encode('utf8'))
        response = h.hexdigest()

        # Now finally check the response. If correct, the device is authenticated!
        if response != msg.response:
            raise Unauthorized('Incorrect response to the challenge')

        await websocket.send('200 OK')

        # Handle any subsequent messages the device may send
        while True:
            msg_raw = await websocket.recv()
            print("> {}".format(msg_raw))
    except Unauthorized as e:
        msg = '401 Unauthorized'
        if DEBUG:
            msg += ': {}'.format(e)
        await websocket.send(msg)
    except websockets.exceptions.ConnectionClosed:
        print('Socket closed!')
        return
    except:
        msg = '500 Internal server error'
        if DEBUG:
            msg += '\n{}'.format(traceback.format_exc())
        await websocket.send(msg)
    print ('Socket closed!')
    websocket.close()


start_server = websockets.serve(hello, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
