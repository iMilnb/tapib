What's this?
============

`tapib` is a trivial _RESTful_ interface to _TPB_, it permits to search content
with a simple _REST_ syntax.

Usage
=====

Start the webservice:

    $ python tapib.py

Query the service:

    $ curl coruscant:5001/s/all/debian

Possible filters are:

* categories: `service:5001/cats`
* top: `service:5001/top/applications:unix`
* search: `service:5001/s/all/free software`

Requirements
============

* pip install ThePirateBay
* pip install dateutils
* pip install lxml
* pip install Flask-RESTful
