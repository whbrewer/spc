sim_conf_file = 'mendel.in'
sim_exe_path = 'engine/mendel'
sim_out_path = './output/'

user='wes'
password='john3.16'

# define user input parameters here and set them with default values
params = dict(case_id='xyz123',mutn_rate=10,frac_fav_mutn=0.00001,
              reproductive_rate=2,pop_size=100,num_generations=50)

# define parameters for executing simulation
exe = dict(path='engine/mendel')

# user must write their own function for how to write the output file
def write_params(form_params):
   f = open(sim_conf_file, 'w')
   f.write('&basic\n')
   keys = params.keys()
   for key in keys:
      #print key, form_params[key]
      f.write(key + ' = ' + form_params[key] + "\n")
   f.write('/\n')
   f.write('&mutations\n')
   f.write('/\n')
   f.write('&selection\n')
   f.write('/\n')
   f.write('&population\n')
   f.write('/\n')
   f.write('&substructure\n')
   f.write('/\n')
   f.write('&computation\n')
   f.write('data_file_path = \'' + sim_out_path + '\'\n')
   f.write('/\n')
   f.close
   return 1

#def read_params()

