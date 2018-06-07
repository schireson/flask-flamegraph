import flask

from flask_flamegraph import FlaskFlamegraph


def test_wsgi():
    app = flask.Flask(__name__)
    flask_flamegraph = FlaskFlamegraph()
    flask_flamegraph.init_app(app)
