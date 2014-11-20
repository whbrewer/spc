from bottle import Bottle, template
from bottle_flash import FlashPlugin

app = Bottle()
COOKIE_SECRET = 'super_secret_string'
app.install(FlashPlugin(secret=COOKIE_SECRET))

@app.route('/')
def create_user():
    app.flash('Created !')
    params = { 'app': app }
    return template('flash', params)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8081, debug=True)
