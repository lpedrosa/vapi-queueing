from bottle import get, post, request, response, run
from Queue import Queue, Empty as QueueEmpty
from threading import Timer

import os
import sys

# provided by the environment
PORT = os.getenv('PORT', 5000)

call_queue = Queue()


class RepeatingTimer(object):
    """Based on RepeatedTimer in http://stackoverflow.com/a/38317060"""

    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False

    def _run(self):
        self.is_running = False
        try:
            self.function(*self.args, **self.kwargs)
        except:
            # Prevents the repeated timer from stopping
            print("RepeatedTimer failed:{}".format(sys.exec_info()[0]))
        finally:
            self.start()

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False


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
