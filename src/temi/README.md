# Temi Python API
The Python API requires a [Temi-side Android application](https://github.com/tongji-cdi/temi-woz-android) in order to function. 
The android application creates a WebSocket server at ws://TEMI_IP:8175, then waits for connections from the Python API. 

## API format
Every call to the Temi API is in JSON format. The standard parameters are:
```json
{
  "command": "API command",
  "id": "An automatically generated UUID."
}
```
Other parameters can be added as needed. Upon finishing the request, the Android side should reply with another JSON message. 
The parameters in the return message varies based on the API used, but the `"id"` must remain THE SAME as the request message.

## Dialogue
### Say a sentence
**Request**
```json
{
  "id": "...",
  "command": "speak",
  "sentence": "The sentence to be spoken"
}
```
**Reply**
```json
{
  "id": "..."
}
```

### Ask a question, then recognize the user's answer
**Request**
```json
{
  "id": "...",
  "command": "ask",
  "sentence": "The sentence to be spoken"
}
```
**Reply**
```json
{
  "id": "...",
  "answer": "The TTS result of the user's answer"
}
```

## Movement

### Go to a saved location
**Request**
```json
{
  "id": "...",
  "command": "goto",
  "location": "The name of the location"
}
```
**Reply**
If Temi successfully reached the destination, `"success"` should be `true`. Otherwise, it should be `false`.
```json
{
  "id": "...",
  "success": true
}
```

### Raise head to a certain angle
**Request**
```json
{
  "id": "...",
  "command": "raise_head",
  "angle": 0
}
```
**Reply**
```json
{
  "id": "..."
}
```

### Rotate by a certain angle
**Request**
```json
{
  "id": "...",
  "command": "turn",
  "angle": 0
}
```
**Reply**
```json
{
  "id": "..."
}
```

## User interface
...TBD
