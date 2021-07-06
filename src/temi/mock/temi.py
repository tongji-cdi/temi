import json
import asyncio
import websockets

async def echo(websocket, path):
    speed = 0

    await asyncio.sleep(speed * 10)  # Wait for actual robot event here
    await websocket.send(json.dumps({
        'id': 'event',
        'event': 'human_detected',
        'data': {}
    }))   # Send actual reply here

    async for message in websocket:
        message = json.loads(message)
        if message['command'] == 'speak':
            await asyncio.sleep(speed * len(message['sentence']))
            await websocket.send(json.dumps(message))
        elif message['command'] == 'ask':
            if message['sentence'] == "我好像不记得见过你，请问你是？":
                await asyncio.sleep(speed * len(message['sentence']))
                message['answer'] = "我叫李明，是新来的实习生"
                await websocket.send(json.dumps(message))
            if message['sentence'] == "":
                pass


        await asyncio.sleep(2)  # Do actual robot things here
        await websocket.send(message)   # Send actual reply

async def emit(websocket, path):
    pass
    

async def server(websocket, path):
    while True:
        await asyncio.gather(
            echo(websocket, path),
            emit(websocket, path)
        )

start_server = websockets.serve(server, "localhost", 8175)

print('Starting a mock Temi server at ws://localhost:8175...')

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()