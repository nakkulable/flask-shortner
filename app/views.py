from . import app
from flask import json, request, redirect, render_template, make_response
from shortner import UrlShortener
import urlparse

shrt = UrlShortener()


@app.route('/')
@app.route('/index/')
def index():
    return render_template('index.html')
