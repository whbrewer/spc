# SPC

## Intro

* The Scientific Platform for the Cloud (SPC) is an integrated cloud platform for rapid interface generation, job scheduling, case management, plotting, and monitoring of scientific applications.

## Quickstart

* To create and initialize the database which SPC uses: 

      `> spc init`

* To start running the web server: 

      `> spc go`

* Open browser to http://0.0.0.0:8580/

* To run the pre-installed example DNA Analyzer app in SPC:

      - Login with default username/password: guest/guest

      - Click "Show Apps" to show a list of installed apps 

      - Click on "dna" the default installed app

      - Enter a DNA string

      - Click confirm to write the datafile to disk

      - Click execute to run the DNA analysis

      - SPC will submit it to the job scheduleer

      - Click output (if you see an error message, it most likely means the jobs has not started running yet, so you can just click output several times until you see the result)

      - Click plot to see or define a list of plots.  For each plot, you can view it by clicking the plot button.  

* For more information, see user's manual in the docs/ folder

## Docker

* To start a docker SPC instance:

      - Either use the published image

      `> docker pull willscott/spc`

      - Or build your own

      `> docker build -t spc .`

      - then run an instance of the loaded image.

      `> docker run -d -P willscott/spc`

## Dependencies

* docker-py (optional-used to support containers)
* matplotlib (optional-used to support matplotlib plotting)
* boto (optional-used to support AWS features)

## Questions

* send email to: wes@fluidphysics.com

