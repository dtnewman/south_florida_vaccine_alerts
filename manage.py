#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from flask_script import Manager, Shell, Server
from flask_migrate import MigrateCommand

from south_florida_vaccine_alerts.app import create_app
import south_florida_vaccine_alerts.models as models
from south_florida_vaccine_alerts.database import db, db_session
try:
    import south_florida_vaccine_alerts.settings_local as settings
except ImportError:
    import south_florida_vaccine_alerts.settings as settings

env = os.environ.get('env', 'Local')

config_object = getattr(settings, env)
app = create_app(config_object=config_object)

manager = Manager(app)


# The following code removes the database session after every request
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


def _make_context():
    """Return context dict for a shell session so you can access
    app, db, and the User model by default.
    """
    return {'app': app, 'db': db, 'models': models}


@manager.command
def test():
    import subprocess
    command = 'nosetests --cover-erase --with-xunit --with-coverage --cover-package=south_florida_vaccine_alerts'.split(' ')
    return subprocess.call(command)

manager.add_command('server', Server())
manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    sys.stdout.flush()
    manager.run()
