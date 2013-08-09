from apps import app_f90

myapp = app_f90('mendel')

#print myapp.params

#myapp.write_html_template()

params, _, _ = myapp.read_params()

myapp.write_params(params)
