# Temi Python API
(Unofficial) Python library for remote-controlling the Temi robot, via WebSocket.

A corresponding server needs to be installed on Temi. You can find it [here](https://github.com/tongji-cdi/temi-woz-android).

## Installation
```
pip install temi
```

## Usage

### Basics
This library uses asyncio to perform the operations. The minimum structure is as follows:
```python
import asyncio
from temi import Temi

async def connect_temi():
    temi = Temi('ws://YOUR_TEMI_IP:8175')
    await temi.connect()
    await temi.speak(sentence='Hello!').run()

asyncio.get_event_loop().run_until_complete(connect_temi())
```
Note that each call needs to be `await`-ed, and must end with a `run()`.

### Sending multiple commands at once
Sometimes, you need temi to do multiple things at once, while other times you may want Temi to do things sequentially. It is easy to mix both in you code. Just do it like such:
```python
# Temi will go to the door, uttering "I hear someone at the door" along the way.
# When Temi arrives, it will ask the question "Hello! What's your name?"
await temi.speak(sentence='I hear someone at the door.').goto(location='Front Door').run()
await temi.ask(sentence="Hello! What's your name?").run()
```

### Timeout
All commands support a `timeout` parameter. If it is specified, the `await` will terminate after the timeout, regardless of execution state.
```python
# The call will return after three seconds, regardless of Temi's location.
# Temi may continue walking to the door, but you can command it to stop in the following code.
await temi.goto(location='Front Door', timeout=3).run()
```

## API
Currently, the following APIs are implemented:
```Python
# Speak a sentence.
await temi.speak(sentence="Sentence to say", timeout=None).run()

# Ask a question, then return the reply.
reply = await temi.ask(sentence="Question to ask", timeout=None).run()

# Go to a location
await temi.goto(location="Location name", timeout=None).run()

# Turn by an angle
await temi.turn(angle=angle, timeout=None).run()

# Tilt screen to an angle (-25 ~ 55)
await temi.turn(angle=angle, timeout=None).run()
```
