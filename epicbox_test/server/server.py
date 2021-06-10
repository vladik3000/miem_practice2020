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

def form_exercise(r):
    all_tests = len(r) 
    passed = 0
    logs = ''
    for test_case in r:
        if test_case['status'] == 'OK':
            passed += 1
        logs += 'test ' + str(passed) + ': ' + test_case['status'] + '\n'
    logs += 'TESTS PASSED: ' + str(passed) + '/' + str(all_tests) + '\n'
    return logs


def humanize_response(response, message):
    header = message['work'] + '\n'
    print(response)
    if 'name' in response[0]:
        for exercise in response:
            name = exercise['name']
            header += name + '\n'
            header += form_exercise(exercise['grade'])
    else:
        header += form_exercise(response)
    return header
    
    

async def post_handler(request):
    try:
        message = await request.json()
        print("MESSAGE RECIEVED", message)
        jsonschema.validate(instance=message, schema=message_schema)
    except Exception as e:
        return web.Response(text=str(e))
    response = proccess_message(message)
    print(response)
    human_response = humanize_response(response['xqueue_body'], message)
    return web.Response(text=str(human_response))


app = web.Application()
app.add_routes([web.get('/', hello)])
app.add_routes([web.post('/', post_handler)])
try:
    web.run_app(app)
except KeyboardInterrupt:
    print("CTRL-C Recieved: stopped")

