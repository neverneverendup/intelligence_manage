from .views import api, inside_api

def init_app(app):
    app.register_blueprint(api)
    app.register_blueprint(inside_api)