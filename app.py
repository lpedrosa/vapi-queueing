import os
from Queue import Queue, Empty as QueueEmpty

from bottle import get, post, request, response, run

from util import RepeatingTimer


# provided by the environment
PORT = os.getenv('PORT', 5000)

call_queue = Queue()


def unqueue_call(queue):
    call = None
    try:
        call = queue.get_nowait()
    except QueueEmpty:
        print('No one in the queue')
    else:
        try:
            transfer_call(call)
        except:
            print("Failed to transfer call: {}".format(call))
        finally:
            queue.task_done()


def transfer_call(call):
    # execute put
    print ("Would PUT to /v1/calls/{}".format(call))

################
# api handlers #
################


def json_response(entity):
    response.content_type = 'application/json'
    import json
    return json.dumps(entity)


@get('/queue')
def queue_call():
    from_addr = request.query['from']
    conversation = request.query['conversation_uuid']
    call = request.query['uuid']

    error_msg = "Received call [conversation_id:{}, call_uuid: {} from: {}]"
    print(error_msg.format(conversation, call, from_addr))

    # store the uuid in queue
    call_queue.put(call)

    # serve ncco
    ncco = [{'action': 'stream',
             'streamUrl': 'someUrl',
             'loop': 0}]

    return json_response(ncco)


@get('/agent')
def agent_ncco():
    ncco = [{'action': 'talk',
             'talk': 'An agent will be with you soon...'}]

    return json_response(ncco)


@post('/queue/events')
def ncco_events():
    event = request.json
    print("Received event: {}".format(event))


try:
    agent_scheduler = RepeatingTimer(5.0, unqueue_call, call_queue)
    print('Starting the agent scheduler')
    agent_scheduler.start()
    run(host='0.0.0.0', port=PORT)
finally:
    print('Stopping the agent scheduler')
    agent_scheduler.stop()
