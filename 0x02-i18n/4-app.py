#!/usr/bin/env python3
""" 4-app.py """
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
    """ determine the best matching language for the request """
    locale = request.args.get('locale')
    # check if locale argument is given
    if locale in app.config['LANGUAGES']:
        return locale

    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index():
    """ index route to the home """
    return render_template('4-index.html')


if __name__ == "__main__":
    app.run(debug=True)
