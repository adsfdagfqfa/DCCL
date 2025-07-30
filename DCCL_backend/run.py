import eventlet
eventlet.monkey_patch()
from flask import Flask
from application.app import create_app
app=create_app()
if __name__ == '__main__':

    app.run()