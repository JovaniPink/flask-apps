"""Environment-backed application settings."""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

APP_NAME = "Flask Starter App"
APP_SYSTEM_ERROR_SUBJECT_LINE = APP_NAME + " system error"

CSRF_ENABLED = True
SECRET_KEY = os.environ.get("SECRET_KEY")

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = os.environ.get(
    "DATABASE_URL", f"sqlite:///{BASE_DIR / 'app.db'}"
)

SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT")
SECURITY_PASSWORD_HASH = "argon2"
SECURITY_REGISTERABLE = True
SECURITY_CONFIRMABLE = True
SECURITY_RECOVERABLE = True
SECURITY_CHANGEABLE = True
SECURITY_PASSWORD_CONFIRM_REQUIRED = True
SECURITY_WEBAUTHN = False
SECURITY_POST_LOGIN_VIEW = "/home"
SECURITY_POST_LOGOUT_VIEW = "/"
SECURITY_URL_PREFIX = "/user"
SECURITY_LOGIN_URL = "/sign-in"
SECURITY_LOGOUT_URL = "/sign-out"
SECURITY_REGISTER_URL = "/register"
SECURITY_FORGOT_PASSWORD_URL = "/forgot-password"
SECURITY_CHANGE_PASSWORD_URL = "/change-password"
SECURITY_LOGIN_USER_TEMPLATE = "flask_user/login.html"
SECURITY_REGISTER_USER_TEMPLATE = "flask_user/register.html"

MAIL_SERVER = os.environ.get("MAIL_SERVER", "localhost")
MAIL_PORT = int(os.environ.get("MAIL_PORT", "25"))
MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER", "no-reply@localhost")
MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
