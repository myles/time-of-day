#!/usr/bin/python

from flask.ext.script import Manager, Shell, Server
from flask.ext.assets import ManageAssets

from timeofday import app


def create_app(config=None):
    if config is not None:
        app.config.from_pyfile(config)

    return app


manager = Manager(create_app)

manager.add_option('-c', '--config',
                   dest='config',
                   help='config file')

manager.add_command('assets', ManageAssets())
manager.add_command('runserver', Server())
manager.add_command('shell', Shell())

if __name__ == '__main__':
    manager.run()
