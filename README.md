# SPC

## Intro

* The Scientific Platform for the Cloud (SPC) is an integrated cloud platform for rapid interface generation, job scheduling, case management, plotting, and monitoring of scientific applications.

## Quickstart

* To create and initialize the database which SPC uses: 

      `> ./spc init`

* To start running the web server: 

      `> ./spc run`

* Open browser to http://0.0.0.0:8580/

* To run the pre-installed example DNA Analyzer app in SPC:

      - Login with default username/password: guest/guest

      - Click "Apps" and then click "installed"

      - Activate the DNA app, then click "Activated" again

      - Click on "dna" the default installed app

      - Enter a DNA string

      - Click confirm to write the datafile to disk

      - Click execute to run the DNA analysis

      - SPC will submit it to the job scheduleer

      - Click output (if you see an error message, it most likely means the jobs has not started running yet, so you can just click output several times until you see the result)

      - Click plot to see or define a list of plots.  For each plot, you can view it by clicking the plot button.  

* To install another SPC packaged app, e.g. Mendel's Accountant:

      - Mac OS X version:

      `> ./spc install https://github.com/whbrewer/fmendel-spc-osx/archive/master.zip`

      - Linux version:

      `> ./spc install https://github.com/whbrewer/fmendel-spc-linux/archive/master.zip`

* To update SPC: if you got the code using "git clone https://github.com/whbrewer/spc.git" 
  you can just do "git pull" within the spc directory.  Before starting, also make sure
  to run "./spc migrate" to migrate the new changes to the database.

* For more information, see user's manual in the docs/ folder

## Docker

* To start a docker SPC instance:

      - Either use the published image

          `> docker pull willscott/spc`

      - Or build your own

          `> docker build -t spc .`

      - then run an instance of the loaded image.

          `> docker run -d -P willscott/spc`

## Optional Dependencies

* matplotlib >= 1.3.1 (optional-used to support matplotlib plotting)
* docker-py >= 1.1.0 (optional-used to support containers)
* boto >= 2.6.0 (optional-used to support AWS management)
* gevent >= 1.0.1 (optional-used for websocket monitoring)
* gevent-websocket >= 0.9.3 (optional-used for websocket monitoring)
* pika > 0.10.0 and RabbitMQ (optionally-required when using RabbitMQ for scheduling)
* PyYAML >= 3.11 (optional-required for supporting YAML input files)
* requests >= 2.9.1 (optional-required if using remote worker nodes)
* psutil >= 5.0.1 (optional-required for monitoring CPU and Memory useage during runs)

## Questions

* send email to: wes@fluidphysics.com

