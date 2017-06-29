v0.20 released on 6/29/17
-------------------------
* add support for dependencies using virtualenv (see note in README.md)
* add support for using <rel_apps_path> tag when specifying app command
* remove official support for matplotlib (although the code is still there)

v0.13 released on 6/29/17
-------------------------
* add TOML parser
* allow for displaying unicode and html code in descriptions
* add script in etc/ folder for starting and stopping spc using initctl
* change plot line ranges to use - instead of :, e.g. 1-100 lines
* better support for shutting down server using Control-C
* better support for admin user to monitor all jobs /jobs/all
* prevent stop button from disappearing
* add merge feature
* add line numbers feature
* rename Home label to Apps
* fix bug in tailing output for short output streams
* add .svg extension to list of possible images
* show number of listed files in /files view
* add support for YAML
* improvements on Docker support
* add support for bootstrap notifications (user must include in app JS file)
* add auto-scrolling feature when "more"ing data, such as output
* fix many bugs and refactor code


v0.12 released on 2/28/17
-------------------------
* add support for themes
* add 'spc update' option for updating plot defs when spc.json file changes
* add support for animating flot plots
* more support for /stats page
* add diff feature in /jobs to compare two cases 
* rename flot-line to flot-scatter
* add labels to datasources
* remove experimental schedulers, all except the multi-processor scheduler
* improved support for admin to delete users
* add support for setting tab title in config.py, use setting: title = "myname"
* add user groups
