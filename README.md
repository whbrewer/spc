# SPC

Note: see NOTES.md file for important release notes.

## INTRO

The Scientific Platform for the Cloud (SPC) is a cloud platform for easily migrating and running scientific applications in the cloud.  It is described in more detail in the following paper:

  > W Brewer, W Scott, and J Sanford, “An Integrated Cloud Platform for Rapid Interface Generation, Job Scheduling, Monitoring, Plotting, and Case Management of Scientific Applications”, Proc. of the International Conference on Cloud Computing Research and Innovation, Singapore, IEEE Press, October 2015, pp. 156-165, doi:10.1109/ICCCRI.2015.24 http://ieeexplore.ieee.org/document/7421906/

This platform is ideally suited to run scientific applications that: (1) require an input deck full of integers, floats, strings, and booleans stored in a standardized file format such as INI, XML, JSON, YAML, or Namelist.input, (2) require some amount of processing time (i.e. not instantaneous -- although it can handle such cases too), (3) require some plotting at the end of the simulation, (4) use MPI or MapReduce for parallelization (although handles serial cases well too).  Moreover, it can handle other applications as well, but some amount of pre- or post-processing may be required.  Such topics are described in more detail in the aforementioned paper.  If you need a copy of this paper, please send an e-mail request to the address at the bottom of this file.

Disclaimer: SPC has been tested primarily with Google Chrome browser, Python 2.7.8 to 2.7.12, on Linux and OS X systems. Other environments may work, but are not guaranteed to work.

## QUICKSTART

* Note, SPC assumes you have a few packages installed by default, namely: Python 2.78 or later,
  virtualenv, gcc, and python-dev (required for compiling psutil).  If you don't have these
  installed, use either apt-get or yum to install them.

* To install dependencies, create and initialize the database which SPC uses, type:

    `./spc init`

* To start running the web server, type:

    `./spc run`

* Open browser to http://0.0.0.0:8580/

* To run the pre-installed example DNA Analyzer app in SPC:

    * Click `Apps` and then click `installed`

    * `Activate` the DNA app, then click `Activated` again

    * Click on `dna` the default installed app

    * Enter a DNA string, or use the default

    * Click `confirm` to write the datafile to disk

    * Click `execute` to run the DNA analysis.  SPC will submit it to the job scheduler

    * Click `output` (if you see an error message, it most likely means the jobs has not started running yet, so you can just click output several times until you see the result)

    * Click `plot` to see or define a list of plots.  For each plot, you can view it by clicking the plot button.

## INSTALL PACKAGED APPS

To install another SPC packaged app, e.g. Mendel's Accountant:

* Mac OS X version:

    > ./spc install https://github.com/whbrewer/fmendel-spc-osx/archive/master.zip

* Linux version:

    > ./spc install https://github.com/whbrewer/fmendel-spc-linux/archive/master.zip

## UPDATING SPC

To update SPC: if you got the code using "git clone https://github.com/whbrewer/spc.git"
you can just do "git pull" within the spc directory.  Before starting, also make sure
to run "./spc migrate" to migrate the new changes to the database.

Note that cloning the latest version of the repo may be unstable.  So, it is
better to download one of the releases (click on "Branch: master" and then click "Tags"
and select one of the releases).

For more information, see user's manual in the docs/ folder

## QUESTIONS

For more info, check out the documentation in the docs folder.  Send questions to: wes@fluidphysics.com
