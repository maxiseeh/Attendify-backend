from flask import Flask
from config import Config
from app.extensions import db, migrate, jwt, cors


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)

    from app.routes.auth_routes import auth_bp
    from app.routes.attendance_routes import attendance_bp
    from app.routes.session_routes import session_bp
    from app.routes.report_routes import report_bp
    from app.routes.connection_routes import connection_bp
    from app.routes.device_routes import device_bp
    from app.routes.wifi_routes import wifi_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(attendance_bp)
    app.register_blueprint(session_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(connection_bp)
    app.register_blueprint(device_bp)
    app.register_blueprint(wifi_bp)

    return app
