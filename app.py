from bottle import get, post, request, run


@get('/queue')
def queue_call():
    ncco = {'action': 'conversation',
            'name': 'call-queue'}
    return ncco


@post('/queue/events')
def ncco_events():
    event = request.json
    print("Received event: {}".format(event))


run(host='0.0.0.0', port=5000, server='gunicorn', workers='2')
