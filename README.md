SciPaaS is both a platform and framework for rapidly deploying scientific applications to the cloud.

-----------
QUICKSTART
-----------

* To create and initialize the database which SciPaaS uses: 
  
      scipaas-admin.py init

* To start running the web server: 

      python scipaas.py

* To run the dna case in scipaas:

  Login with default username/password: guest/guest
  Click "Show Apps" to show a list of isntalled apps 
  Click on "dna" the default installed app
  Enter a DNA string
  Click confirm to write the datafile to disk
  Click execute to run the DNA analysis
     scipaas will submit it to the job scheduleer
  Click output (if you see an error message, it most likely means the jobs has not started running yet, 
                so you can just click output several times until you see the result)
  Click plot to see or define a list of plots.  For each plot, you can view it by clicking the plot button.  

* To start a docker SciPaaS instance:

      # Either use the published image
      docker pull willscott/scipaas
      # Or build your own
      docker build -t scipaas .
      # then run an instance of the loaded image.
      docker run -d -P willscott/scipaas

----------
QUESTIONS
----------

  send email to: wbrewer@alum.mit.edu

