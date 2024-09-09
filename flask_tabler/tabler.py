from flask import Blueprint

default_tabler_version = 'v1.0.0-beta20'

class Tabler(object):
    def __init__(self, app=None, tabler_version=default_tabler_version):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.jinja_env.globals.update(tabler=self.tabler)
        app.jinja_env.globals.update(tabler_version=self.tabler_version)

        blueprint = Blueprint(
            'tabler',
            __name__,
            template_folder='templates',
            static_folder='static',
            static_url_path=app.static_url_path + '/tabler'
        )

        app.register_blueprint(blueprint)

        # setup support for flask-nav
        renderers = app.extensions.setdefault('nav_renderers', {})
        renderer_name = (__name__ + '.nav', 'TablerRenderer')
        renderers['tabler'] = renderer_name

        renderers[None] = renderer_name