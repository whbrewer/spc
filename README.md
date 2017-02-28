# SPC

## Intro

The Scientific Platform for the Cloud (SPC) is a cloud platform for easily migrating and running scientific applications in the cloud.  It is described in more detail in the following paper:

  > W Brewer, W Scott, and J Sanford, “An Integrated Cloud Platform for Rapid Interface Generation, Job Scheduling, Monitoring, Plotting, and Case Management of Scientific Applications”, Proc. of the International Conference on Cloud Computing Research and Innovation, Singapore, IEEE Press, October 2015, pp. 156-165, doi:10.1109/ICCCRI.2015.24 http://ieeexplore.ieee.org/document/7421906/

If you need a copy of this paper, please send an e-mail request to the address at the bottom of this file.

## Quickstart

* To create and initialize the database which SPC uses:

    `./spc init`

* To start running the web server:

    `./spc run`

* Open browser to http://0.0.0.0:8580/

* To run the pre-installed example DNA Analyzer app in SPC:

      - Login with default username/password: guest/guest

      - Click "Apps" and then click "installed"

      - Activate the DNA app, then click "Activated" again

      - Click on "dna" the default installed app

      - Enter a DNA string, or use the default

      - Click confirm to write the datafile to disk

      - Click execute to run the DNA analysis.  SPC will submit it to the job scheduler

      - Click output (if you see an error message, it most likely means the jobs has not started running yet, so you can just click output several times until you see the result)

      - Click plot to see or define a list of plots.  For each plot, you can view it by clicking the plot button.  

## Install packaged apps

To install another SPC packaged app, e.g. Mendel's Accountant:

* Mac OS X version:

    > ./spc install https://github.com/whbrewer/fmendel-spc-osx/archive/master.zip

* Linux version:

    > ./spc install https://github.com/whbrewer/fmendel-spc-linux/archive/master.zip

## Updating SPC

To update SPC: if you got the code using "git clone https://github.com/whbrewer/spc.git"
you can just do "git pull" within the spc directory.  Before starting, also make sure
to run "./spc migrate" to migrate the new changes to the database.  

Note that cloning the latest version of the repo may be unstable.  So, it is
better to download one of the releases (click on "Branch: master" and then click "Tags"
and select one of the releases).

For more information, see user's manual in the docs/ folder

## Optional Dependencies

SPC can run without any dependencies except Python 2.7 standard libs.  It
is extensible in various ways by including other libs listed here:

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

For more info, check out the documentation in the docs folder.  Send questions to: wes@fluidphysics.com
