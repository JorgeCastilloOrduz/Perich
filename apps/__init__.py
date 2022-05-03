from flask import Flask

def create_app(config):
    application = Flask(__name__)
    application.config.from_object(config)
    
    from apps import routes

    application.register_blueprint(routes.bp)

    return application