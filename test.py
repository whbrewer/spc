#from apps import app_f90
#myapp = app_f90('mendel')
#params, _, _ = myapp.read_params()
#myapp.write_params(params)

import bottle
import bottle.ext.sqlite

app = bottle.Bottle()
#plugin = bottle.ext.sqlite.Plugin(dbfile='/tmp/test.db')
plugin = bottle.ext.sqlite.Plugin(dbfile='test.db')
app.install(plugin)

@app.route('/show/:item')
def show(item, db):
    row = db.execute('SELECT * from items where name=?', item).fetchone()
    if row:
        return template('showitem', page=row)
    return HTTPError(404, "Page not found")

app.run(host='localhost', port=8080)
