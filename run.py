from app import app
# from werkzeug.contrib.fixers import ProxyFix

# app.wsgi_app = ProxyFix(app.wsgi_app)
port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)
# app.run(debug=True)
