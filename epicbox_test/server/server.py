from aiohttp import web
import json
import jsonschema
from handler import proccess_message
#message schema that student should sent via HTTP (CHANGE TO NORMAL ONE)
message_schema = {
        'type': 'object',
        'properties': {
            'name': { 'type': 'string' },
            'work': { 'type': 'string' },
            'git': { 'type': 'string' }
            },
        'required': ['name', 'work', 'git'] 
    }


async def hello(request):
    return web.Response(text="Hello, world")

async def post_handler(request):
    try:
        message = await request.json()
        print("MESSAGE RECIEVED", message)
        jsonschema.validate(instance=message, schema=message_schema)
    except Exception as e:
        return web.Response(text=str(e))
    response = proccess_message(message)
    return web.Response(text=response)


app = web.Application()
app.add_routes([web.get('/', hello)])
app.add_routes([web.post('/', post_handler)])
try:
    web.run_app(app)
except KeyboardInterrupt:
    print("CTRL-C Recieved: stopped")

