from . import app
from flask import json, request, redirect, render_template, make_response
from shortner import UrlShortener
import urlparse

shrt = UrlShortener()


@app.route('/')
@app.route('/index/')
def index():
    return render_template('index.html')


@app.route('/404')
def missing():
    return render_template('missing.html')


@app.route('/400')
def invalid():
    return render_template('invalid.html')


# short url lookup
@app.route('/<code>')
def lookup(code):
    url = shrt.lookup(code)
    if not url:
        return redirect('/404')
    else:
        return redirect(url)


# short url generation
#
# If JSON is fed, we shorten and reply in JSON as well
# If a Form is posted we reply in HTML
# Otherwise we redirect to a failure page
@app.route('/', methods=['POST'])
def shorten_url():
    if request.json and 'url' in request.json:
        u = urlparse.urlparse(request.json['url'])
        if u.netloc == '':
            url = 'http://' + request.json['url']
        else:
            url = request.json['url']
        res = shrt.shorten(url)
        response = make_response(json.dumps(res))
        response.headers['Content-Type'] = 'application/json'
        return response
    elif request.form and 'url' in request.form:
        u = urlparse.urlparse(request.form['url'])
        if u.netloc == '':
            url = 'http://' + request.form['url']
        else:
            url = request.form['url']
        res = shrt.shorten(url)
        return render_template('result.html', result=res)
    else:
        # Invalid URL
        return redirect('/400')
