#from .views import api, inside_api
from .inViews import inside_api
from .outViews import api

def init_app(app):
    app.register_blueprint(api)
    app.register_blueprint(inside_api)