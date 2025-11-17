from .user_routes import user_bp
from .role_routes import role_bp


def register_blueprints(app):
    """Function to register all blueprints."""
    app.register_blueprint(user_bp)  # Register user routes
    app.register_blueprint(role_bp)  # Register role routes
