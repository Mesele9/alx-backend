#!/usr/bin/env python3
""" 4-app.py """
from flask import Flask, render_template, request, g
from flask_babel import Babel, _

app = Flask(__name__)
babel = Babel(app)

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user(user_id: int) -> dict:
    """ get users from the users table """
    return users.get(user_id)


@app.before_request
def before_request():
    """ a fucntion that checks for login before loading"""
    login_as = request.args.get('login_as')
    if login_as is not None:
        user_id = int(login_as)
        g.user = get_user(user_id)
    else:
        g.user = None


class Config:
    """ config class """
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app.config.from_object(Config)


@babel.localeselector
def get_locale():
    """ determine the best macthing for the language """
    locale = request.args.get('locale')
    # checks if local argument is provided
    if locale in app.config['LANGUAGES']:
        return locale

    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index():
    """ index route to the home """
    return render_template('5-index.html')


if __name__ == "__main__":
    app.run(debug=True)
