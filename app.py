#codin:utf-8
from bottle import route, run, request, abort, static_file

from fsm import TocMachine

from transitions.extensions import GraphMachine

from verify import verify_token

import os

#VERIFY_TOKEN = '123456'
VERIFY_TOKEN = verify_token
#PORT = os.environ['PORT']
count = [0]

machine = TocMachine(
    states=[
        'user',
        'asking',
        'label',
        'waiting',
        'check',
        'choose',
        'send_question',
        'ans',
        'convert',
        'produces'
    ],
    transitions=[
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'asking',
            'conditions': 'is_going_to_asking'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'choose',
            'conditions': 'is_going_to_choose'
        },
        {
            'trigger': 'advance',
            'source': 'asking',
            'dest': 'label',
            'conditions': 'is_going_to_label'
        },
        {
            'trigger': 'advance',
            'source': 'asking',
            'dest': 'user',
            'conditions': 'is_going_to_user'
        },
        {
            'trigger': 'advance',
            'source': 'label',
            'dest': 'user',
            'conditions': 'is_going_to_user'
        },
        {
            'trigger': 'advance',
            'source': 'label',
            'dest': 'waiting',
            'conditions': 'is_going_to_waiting'
        },
        {
            'trigger':'advance',
            'source':'waiting',
            'dest':'check',
            'conditions':'is_going_to_check'
        },
        {
            'trigger':'advance',
            'source':'check',
            'dest':'user',
            'conditions':'is_going_to_user'
        },
        {
            'trigger':'advance',
            'source':'choose',
            'dest':'send_question',
            'conditions':'is_going_to_send_question'
        },
        {
            'trigger':'advance',
            'source':'send_question',
            'dest':'ans',
            'conditions':'is_going_to_ans'
        },
        {
            'trigger':'advance',
            'source':'ans',
            'dest':'user',
            'conditions':'is_going_to_user'
        },
        {
            'trigger':'advance',
            'source':'user',
            'dest':'convert',
            'conditions':'is_going_to_convert'
        },
        {
            'trigger':'advance',
            'source':'convert',
            'dest':'produces',
            'conditions':'is_going_to_produces'
        },
        {
            'trigger':'advance',
            'source':'produces',
            'dest':'user',
            'conditions':'is_going_to_user'
        },
        {
            'trigger': 'go_back',
            'source': [
                "produces"
            ],
            'dest': 'user'
        }
    ],
    initial='user',
    auto_transitions=False,
    show_conditions=True,
)


@route("/webhook", method="GET")
def setup_webhook():
    mode = request.GET.get("hub.mode")
    token = request.GET.get("hub.verify_token")
    challenge = request.GET.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("WEBHOOK_VERIFIED")
        return challenge

    else:
        abort(403)


@route("/webhook", method="POST")
def webhook_handler():
    global count
    body = request.json
    print('\nFSM STATE: ' + machine.state)
    print('REQUEST BODY: ')
    print(body)

    if body['object'] == "page":
        event = body['entry'][0]['messaging'][0]
        machine.advance(event,count)
        return 'OK'


@route('/show-fsm', methods=['GET'])
def show_fsm():
    print("!!!")
    machine.get_graph().draw('fsm.png', prog='dot', format='png')
    return static_file('fsm.png', root='./', mimetype='image/png')


if __name__ == "__main__":
    run(host="localhost", port=8000, debug=True, reloader=True)
    #run(host="0.0.0.0", port=PORT, debug=True, reloader=True)
    print(machine.state)
