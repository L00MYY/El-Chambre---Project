from flask import Flask

from el_chambre.api.endpoints.routes import register_routes
from el_chambre.api.error_handlers import register_error_handlers


def create_app(test_config=None):
    app = Flask(__name__)

    if test_config:
        app.config.update(test_config)

    register_error_handlers(app)
    register_routes(app)
    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
