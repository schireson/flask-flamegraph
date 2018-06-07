from werkzeug.wrappers import Response

from flask_flamegraph.sampler import Sampler


class FlaskFlamegraph:
    def __init__(self, app=None, path='/__flame__'):
        self.wsgiapp = None
        self.path = path.rstrip('/')
        self.sampler = None

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        if not self.wsgiapp:
            self.wsgiapp = app.wsgi_app
            app.wsgi_app = self

    def __call__(self, environ, start_response):
        path = environ.get('PATH_INFO', '')
        if path == self.path or path == self.path + '/':
            return self.render(environ, start_response)

        self.sampler = Sampler()
        self.sampler.start()

        result = self.wsgiapp(environ, start_response)

        self.sampler.stop()
        return result

    def render(self, environ, start_response):
        verb = environ.get('REQUEST_METHOD', 'GET').strip().upper()
        if verb != 'GET':
            response = Response(
                '405 Method Not Allowed',
                status=405,
                mimetype='text/plain',
            )
            response.headers['Allow'] = 'GET'

        elif not self.sampler:
            response = Response(
                'Make a request first!',
                status=200,
                mimetype='text/plain',
            )

        else:
            response = Response(
                self.sampler.generate_svg(),
                mimetype='image/svg+xml',
            )

        return response(environ, start_response)
