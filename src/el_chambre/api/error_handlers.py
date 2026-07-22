from flask import jsonify
from werkzeug.exceptions import HTTPException

from el_chambre.application.exceptions.exceptions import (
    ConflictError,
    InsufficientStockError,
    NotFoundError,
    ValidationError,
)


def register_error_handlers(app):
    @app.errorhandler(ValidationError)
    @app.errorhandler(ValueError)
    def handle_validation_error(error):
        return jsonify({"error": str(error)}), 400

    @app.errorhandler(NotFoundError)
    def handle_not_found_error(error):
        return jsonify({"error": str(error)}), 404

    @app.errorhandler(ConflictError)
    @app.errorhandler(InsufficientStockError)
    def handle_conflict_error(error):
        return jsonify({"error": str(error)}), 409

    @app.errorhandler(HTTPException)
    def handle_http_error(error):
        return jsonify({"error": error.description}), error.code

    @app.errorhandler(Exception)
    def handle_unexpected_error(_error):
        return jsonify({"error": "Ocurrió un error interno"}), 500
