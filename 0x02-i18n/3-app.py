#!/usr/bin/env python3
""" 3-app.py """
from flask import Flask, render_template, request
from flask_babel import Babel, _

app = Flask(__name__)
babel = Babel(app)


class Config:
    """ config class """
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app.config.from_object(Config)


@babel.localeselector
def get_locale():
    """ get_locale function check accepted language """
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index():
    """ index route to the home """
    return render_template('3-index.html')


if __name__ == "__main__":
    app.run(debug=True)
