# pgnotifpy
A Simple wrapper around psycopg2 to handle PostgreSQL NOTIFY à la Flask


`pgnotifpy` is a simple wrapper around psycopg2 to work with PostgreSQL
notification with a Flask-like API:

```python
import pgnotifpy

li = pgnotifpy.Listener('dbname', 'user')

@li.listen('new_user')
def say_hello(data):
    print('hi', data)

@li.listen('delete_user')
def say_bye(data):
    print('bye', data)

li.run('job', dispatch)
```

`pgnotifpy` allows you to use your own dispatcher, so you are not
obliged to follow a specific convention for your messages.

For example, suppose you work with JSON-encoded messages that looks like this:

```json
{
    "action": "new_user",
    "data": {
        "id": 42,
        "name": "John Doe"
    }
}
```

All you have to do is to write a simple dispatcher function so `pgnotifpy` can
do the correct routing for you.

```pyhton
def my_dispatch(payload):
    try:
        data = json.loads(payload)
        action = data['action']
        message = data.get('data')
    except (ValueError, KeyError):
        print('Ill-formed JSON message :(')
        return
    return action, message
```

Then, just pass it to the `run` method:

```python
li.run('job', my_dispatcher
```


A dispatcher function is expected to have the following signature:

```
dispatcher(payload: str) -> Option[Tuple[str, any]]
```

That is, if a dispatcher returns `('new_user', data)`, all
functions listening to `'new_user'` will be triggered with
`data` supplied as the only argument.


