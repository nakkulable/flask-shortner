from . import app


@app.route('/')
@app.route('/index')
def index():
    return "Meenakshi I love you!"
