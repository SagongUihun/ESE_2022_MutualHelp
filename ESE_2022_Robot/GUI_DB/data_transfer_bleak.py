import asyncio
from bleak import BleakClient

# mac
address = "df:e6:f4:32:69:6d"

# callback event
def on_disconnect(client):
    print("Client with address {} got disconnected!".format(client.address))


def run(address):
    # create client class
    client = BleakClient(address)
    try:
        # device disconnect callback fucntion enrollment
        client.set_disconnected_callback(on_disconnect)
        # device connect start
        client.connect()
        print('connected')    
    except Exception as e:
        # connect fail
        print('error: ', e, end='')        
    finally:
        print('start disconnect')
        # device disconnect
        client.disconnect()

loop = asyncio.get_event_loop()
loop.run_until_complete(run(address))
print('done')