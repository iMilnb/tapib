What's this?
============

`tapib` is a trivial _RESTful_ interface to _TPB_, it permits to search content
with a simple _REST_ syntax.

Usage
=====

Start the webservice:

    $ python tapib.py

Query the service:

    $ curl localhost:5001/s/all/debian

Possible filters are:

* categories: `localhost:5001/cats`
* top: `localhost:5001/top/applications:unix`
* search: `localhost:5001/s/all/free software`
* search and sort: `localhost:5001/s/video:movies/public domain/size:asc`

Sort filters are composed of `name`, `uploaded`, `size`, `seeders`, `leechers`, `uploader` and `type`. Each filter must be associated with a `des` (decreasing)
or `asc` (increasing) parameter. For example:

    $ curl "localhost:5001/s/audio:music/public domain/leechers:des"

will display results for `"public domain"` in the `audio:music` section by leechers ordering the search from the most to the lesser.  
Default order is `seeders:des`


Requirements
============

* pip install ThePirateBay
* pip install dateutils
* pip install lxml
* pip install Flask-RESTful
