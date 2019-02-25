import json
import pgnotifpy

def dispatch(payload):
    try:
        data = json.loads(payload)
        action = data['action']
        message = data.get('data')
    except (ValueError, KeyError):
        print('Ill-formed JSON message :(')
        return
    return action, message


li = pgnotifpy.Listener('dbname', 'user')

@li.listen('new_user')
def say_hello(data):
    print('hi', data)

@li.listen('delete_user')
def say_bye(data):
    print('bye', data)

li.run('job', dispatch)

