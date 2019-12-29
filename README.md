# Roller Shutter Manager

This is a Flask app that allows to manage a set of Shelly 2.5 switches mounted to control roller shutters.àà#

## Prerequisites

- mqtt broker running (i use mosquitto)

## App configuration

We use [Instance folders](https://flask.palletsprojects.com/en/1.1.x/config/#instance-folders) configuration,
so you need to create a configuration file in `instance/config.py` with informations like these::

    MQTT_BROKER_URL = "127.0.0.1"
    MQTT_BROKER_PORT = 1883
    FLASK_APP = "blinds_manager"

    BLINDS = [
        {"id": "blind1", "name": "Kitchen"},
    ]

Where `MQTT_*` are config informations for MQTT broker connection.

BLINDS is a list of dictionaries where `id` is the blind id set into MQTT settings into Shelly device.

## Installation

This app runs with a buildout configuration, to handle dependencies and helper scripts.

First of all you need to create a virtualenv and install zc.buildout.

If you are using `pipenv`, just run::

    > pipenv

It will create a new virtual environment with Python 3.7 and zc.buildout.

After that, you have to run the buildout to install all the needed dependencies.
There are two main config files (development.cfg and production.cfg). Symlink buildout.cfg with one of these
depending on the environment where you are working on.::

    > ln -s development.cfg buildout.cfg

And finally, run buildout::

    pipenv run buildout -N

Or with Makefile::

    > make buildout

This will install all Flask dependencies and supervisor.

## Production mode

TODO

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
