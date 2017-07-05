import websockets
import json
import hashlib
import asyncio


async def run():
    deviceid = '0004'
    key = 'uoihwefiuhwef'

    async with websockets.connect('ws://localhost:8765') as sock:
        challenge_js = await sock.recv()
        challenge = json.loads(challenge_js).get('challenge', '')
        print ('Got challenge', challenge)

        algo = 'sha256'
        h = hashlib.new(algo)
        h.update(deviceid.encode('utf8'))
        h.update(key.encode('utf8'))
        h.update(challenge.encode('utf8'))
        response = h.hexdigest()

        reply = {'deviceid': deviceid,
                 'challenge': challenge,
                 'response': response,
                 'algorithm': algo
                 }
        print ('sending reply', reply)
        await sock.send(json.dumps(reply))

        response = await sock.recv()
        print ('Got response:', response)

        print ('sending hello, world!')
        await sock.send('Hello, world!')

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(run())