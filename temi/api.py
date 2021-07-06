import json
import uuid
import asyncio
import logging
import colorlog
import websockets


class Temi:
    def __init__(self, uri, logger=None, loglevel='DEBUG'):
        self.uri = uri

        if logger is not None:
            self.logger = logger
        else:
            FORMAT = '%(log_color)s%(levelname)s:%(name)s %(asctime)-15s - %(message)s'
            handler = colorlog.StreamHandler()
            handler.setFormatter(colorlog.ColoredFormatter(FORMAT))

            self.logger = colorlog.getLogger('temi')
            self.logger.addHandler(handler)
            self.logger.setLevel(loglevel)

        self.temisocket = None
        # self.uisocket = None
        self.tasks = []
        self.callbacks = {}

    async def __receive_temi_events(self):
        async for message in self.temisocket:
            message = json.loads(message)
            if message['id'] == 'event':
                self.logger.debug(f"Received {message['event']}: {message['data']}")
                await self.__process_callbacks(message['event'], message['data'])
    
    async def connect(self, tries=3, interval=5):
        for turn in range(tries):
            try:
                # Connect to the WebSocket server on Temi
                self.logger.debug(f'Trying to connect to Temi at {self.uri}...')
                self.temisocket = await websockets.connect(self.uri)
                self.logger.info(f'Connected to Temi at {self.uri}.')
                # Create a task to receive event from Temi WebSocket server
                self.temireceiver = asyncio.create_task(self.__receive_temi_events())
                return
            except Exception as e:
                print(e)
                self.logger.error(f'Cannot connect to Temi at {self.uri}.')
                if turn + 1 < tries:
                    await asyncio.sleep(interval)
        self.logger.critical(f'Could connect to Temi at {self.uri} after {tries} tries.')
        raise Exception('Cannot connect to Temi at', self.uri)

    async def disconnect(self):
        if self.temisocket is not None and self.temisocket.open:
            self.temireceiver.cancel()
            self.temisocket.close()
    
    def register(self, event, callback, oneshot=False):
        if event not in self.callbacks:
            self.callbacks[event] = {
                'oneshot': set(),
                'repeat': set()
            }
        if oneshot:
            self.callbacks[event]['oneshot'].add(callback)
        else:
            self.callbacks[event]['repeat'].add(callback)

    def unregister(self, event, callback):
        if callback in self.callbacks[event]['oneshot']:
            self.callbacks[event]['oneshot'].remove(callback)
        elif callback in self.callbacks[event]['repeat']:
            self.callbacks[event]['repeat'].remove(callback)
    
    async def __process_callbacks(self, event, data):
        self.logger.debug(f'Triggering callbacks for event {event}.')
        for callback in self.callbacks[event]['oneshot']:
            await callback(event, data)
        self.callbacks[event]['oneshot'] = set()
        for callback in self.callbacks[event]['repeat']:
            await callback(event, data)

    async def __send_command(self, command, **kwargs):

        # Create a UUID for this command.
        command_uuid = str(uuid.uuid4())

        # Assemble the JSON message
        kwargs['command'] = command
        kwargs['id'] = command_uuid
        command_string = json.dumps(kwargs, ensure_ascii=False)

        try:
            async with websockets.connect(self.uri) as websocket:
                # Send it.
                await websocket.send(command_string)
                self.logger.debug(f'Sent command to Temi: {command_string}')

                # Receive response from Temi and see if the message is for us. If true, break the loop and return.
                while True:
                    message = await websocket.recv()
                    try: 
                        message = json.loads(message)
                        if message['id'] == command_uuid:
                            self.logger.info(f'Finished "{command}": {message}')
                            return message
                    except:
                        pass
        except Exception as e:
            self.logger.error(f'Error when sending command to Temi.')
            raise e

    async def command(self, command, timeout=None, **kwargs):
        return await asyncio.wait_for(
            self.__send_command(command, **kwargs), timeout=timeout
        )

    async def run(self):
        results = await asyncio.gather( *self.tasks )
        self.tasks = []
        if len(results) == 1:
            return results[0]
        return results

    def __getattr__(self, name):
        def command_template(*args, **kwargs):
            self.tasks += [self.command(name, **kwargs)]
            return self
        return command_template

if __name__ == '__main__':
    class Test:
        def __init__(self, index):
            self.id = index
        def test(self, event, data):
            print(event, data)

    async def connect_temi():
        temi = Temi('ws://192.168.1.105:8175')
        await temi.connect()
        message = await temi.interface(url="https://www.baidu.com/").speak(sentence="百度一下，你就知道。").run()
        print(message)

    asyncio.get_event_loop().run_until_complete(connect_temi())