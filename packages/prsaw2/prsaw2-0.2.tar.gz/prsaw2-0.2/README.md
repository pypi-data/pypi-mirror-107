# prsaw2
Simple python API wrapper for the Random Stuff API.

- Easy to use
- Wraps the entire API
- Supports both async and sync
- Supports both v2 and v3 versions of API

- **[PyPi Package](https://pypi.org/project/prsaw2)**
- **[Documentation](https://flampt.gitbook.io/prsaw2)**

## Installation
Installation can be done easily using the python package manager `pip`
```bash
pip install prsaw2
```

## Quickstart
Firstly make sure to [get the API key from here](https://api.pgamerx.com/register)

Here are few examples to get you started.

### Getting AI response
```py
import prsaw2

client = prsaw2.Client(key='api-key-here')

response = client.get_ai_response("Hi there")
client.close()  # Not necessary
print(response)
```

### Getting random joke
```py
import prsaw2

client = prsaw2.Client(key='api-key-here')

response = client.get_joke(type="any")
client.close()  # Not necessary
print(response.joke)
```

### Getting random image
```py
import prsaw2

client = prsaw2.Client(key='api-key-here')

response = client.get_image(type="any")
client.close()
print(response)
```

## Async Support
The library also supports async usage.
```py
import prsaw2
import asyncio

client = prsaw2.AsyncClient(key="api-key-here")

async def coro():
  response = await client.get_ai_response("Hello world")
  await client.close()  
  print(response)

loop = asyncio.get_event_loop()
loop.run_until_complete(coro())
```