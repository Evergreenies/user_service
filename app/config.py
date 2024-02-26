try:
    from .twelve_factor_app_framework.bootstrap import app
except ImportError:
    from twelve_factor_app_framework.bootstrap import app

app = app
user_app = app()
config = app.config
logger = app.logger

# Email validation regular expression (limited scope)
EMAIL_REGEX = r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?\.(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?)*$"
