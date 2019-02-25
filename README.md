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

This code will listen for events originating from a `NOTIFY 'job', <DATA>` query.

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

```python
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
li.run('job', my_dispatcher)
```


A dispatcher function is expected to have the following signature:

```
dispatcher(payload: str) -> Option[Tuple[str, any]]
```

That is, if a dispatcher returns `('new_user', data)`, all
functions listening to `'new_user'` will be triggered with
`data` supplied as the only argument.

## FAQ

### Is it ready for production?
Short answer: Not yet.

Long &nswer: I use this wrapper in some real projects. However,
this wrapper is used in specific environments
that does not allow edge-cases such as an unexpectedly
disconnected database.

### Is it asynchronous?
No.

This library is a wrapper over `psycopg2` which works
in a synchronous manner. Maybe someday I will make a version
using the `asyncpg` library which supports `async`.

### Use cases
This library may not be suited for high-throughput processing such as
data streaming. But, would you use PostgreSQL's `NOTIFY`/`LISTEN` for
this kind of task anyway? :)

