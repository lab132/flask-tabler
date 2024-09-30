from flask import Blueprint, render_template
from .forms import render_form, render_table, render_form_scripts

default_tabler_version = "v1.0.0-beta20"


class Tabler(object):
    def __init__(self, app=None, tabler_version=default_tabler_version):
        if app is not None:
            self.init_app(app)
        self.version = tabler_version

    def init_app(self, app):
        app.jinja_env.globals.update(tabler_version=self.version)
        app.jinja_env.globals.update(tabler_render_form=render_form)
        app.jinja_env.globals.update(tabler_render_form_scripts=render_form_scripts)
        app.jinja_env.globals.update(tabler_render_table=render_table)

        blueprint = Blueprint(
            "tabler", __name__, template_folder="templates", static_folder="static", static_url_path=app.static_url_path + "/tabler"
        )

        app.register_blueprint(blueprint)

        # setup support for flask-nav
        renderers = app.extensions.setdefault("nav_renderers", {})
        renderer_name = ("flask_tabler.nav", "TablerRenderer")
        renderers["tabler"] = renderer_name

        renderers[None] = renderer_name

    def render_overview(self, items, fields, title=None, description=None):
        return render_template("tabler/overview.html.j2", items=items, fields=fields, title=title, description=description)
