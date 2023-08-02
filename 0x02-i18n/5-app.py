#!/usr/bin/env python3
""" 5-app.py """
from flask import Flask, render_template, request, g
from flask_babel import Babel, _
from typing import Dict, Union


app = Flask(__name__)
babel = Babel(app)


class Config:
    """ config class """
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app.config.from_object(Config)


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user() -> Union[Dict, None]:
    """ get users from the users table """
    try:
        return users[int(request.args.get('login_as'))]
    except Exception:
        return None


@app.before_request
def before_request():
    """ a fucntion that checks for login before loading"""
    user = get_user()
    if user:
        g.user = user


@babel.localeselector
def get_locale() -> str:
    """ determine the best macthing for the language """
    locale = request.args.get('locale')
    # checks if local argument is provided
    if locale and locale in app.config['LANGUAGES']:
        return locale

    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index():
    """ index route to the home """
    return render_template('5-index.html')


if __name__ == "__main__":
    app.run(debug=True)
