import re

#sim_conf_template = 'static/mendel.in'
sim_conf_template = './static/mendel.in'
sim_conf_file = './mendel.in'
sim_exe_path = 'engine/mendel'
sim_out_path = './output/'

# for user authentication
user='wes'
password='john3.16'

# define user input parameters here and set them with default values
#params = dict(case_id='xyz123',mutn_rate=10,frac_fav_mutn=0.00001,
#              reproductive_rate=2,pop_size=100,num_generations=50)

# define parameters for executing simulation
exe = dict(path='engine/mendel')

# user must write their own function for how to write the output file
def write_params(form_params):
   f = open(sim_conf_file, 'w')
   f.write('&basic\n')
   #keys = params.keys()
   keys = read_namelist().keys() # change this in the future
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

def read_namelist():
    '''read the namelist file and return as a dictionary'''
    params = dict()
    #get_block = dict()
    block = 'dummy'
    for line in open(sim_conf_template, 'rU'):
        for word in line.split():
            m = re.search(r'&(\w+)',line) # block title
            n = re.search(r'(\w+) = (.*$)',line) # parameter
            if m:
                block = m.group(1)  
            elif n:
                #print block, n.group(1), n.group(2)
                params[n.group(1)] = n.group(2)
                #get_block[n.group(1)] = block
    #print get_block
    print params
    return params

#def write_params():
#    def wrapper:  
