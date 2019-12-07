# Roller Shutter

TODO

## Production mode

### gunicorn conf file
Gunicorn configuration file isn't under version control.
You need to create a `gunicorn_config.py` like this:

```python
worker_class = "gevent"
workers = 1
bind = "0.0.0.0:5000"
```

If you need to run the server with ssl cert, add these rows:

```python
certfile = "/path/to/ssl/certfile.pem"
keyfile = "path/to/ssl/privkey.pem"
```
