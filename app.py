from bottle import get, post, request, response, run
from Queue import Queue

import os

# provided by the environment (e.g. Heroku)
PORT = os.getenv('PORT', 5000)

call_queue = Queue()


def json_response(container):
    response.content_type = 'application/json'
    import json
    return json.dumps(container)


@get('/queue')
def queue_call():
    from_addr = request.query['from']
    conversation = request.query['conversation_uuid']
    call = request.query['uuid']

    print("Received call [conversation_id:{}, call_uuid: {} from: {}]"
            .format(conversation, call, from_addr))

    # store the uuid in queue
    call_queue.put(call)

    # serve ncco
    ncco = [{'action': 'stream',
             'streamUrl': 'someUrl',
             'loop': 0}]

    return json_response(ncco)


@post('/queue/events')
def ncco_events():
    event = request.json
    print("Received event: {}".format(event))


run(host='0.0.0.0', port=PORT, server='gunicorn', workers='1')
