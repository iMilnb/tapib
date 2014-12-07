# Very simple RESTful interface to TPB
# Uses:
#   * https://github.com/karan/TPB
#   * http://flask-restful.readthedocs.org/en/latest

from flask import Flask
from flask.ext.restful import abort, Api, Resource
from tpb import TPB
from tpb import CATEGORIES, ORDERS

tpburl = 'https://thepiratebay.se'

app = Flask(__name__)
api = Api(app)

t = TPB(tpburl)

def abort_if_no_category(category):
    try:
        cat, sub = category.split(':')
        return getattr(getattr(CATEGORIES, cat.upper()), sub.upper())
    except AttributeError:
        abort(404, message="category {} doesn't exist".format(category))

def append_torrent(r):
    return {
            'created': r.created.strftime('%m/%d/%Y'),
            'title': r.title,
            'magnet': r.magnet_link,
            'seeders': r.seeders,
            'leechers': r.leechers,
            'size': r.size,
           }

class Categories(Resource):
    def get(self):
        categories = ['all']
        # main categories
        cats = [a for a in dir(CATEGORIES) if not a.startswith('__')]
        # sub categories except ALL
        for c in [s for s in cats if not s == 'ALL']:
            subcat = getattr(CATEGORIES, c)
            for sub in [s for s in dir(subcat) if not s.startswith('__')]:
                categories.append('{0}:{1}'.format(c.lower(), sub.lower()))
        return categories

class Top(Resource):
    def get(self, category):
        top = []
        cat = abort_if_no_category(category)
        for r in t.top().category(cat):
            top.append(append_torrent(r))
        return top

class Search(Resource):
    def get(self, category, sstr):
        search = []
        if category == 'all':
            cat = CATEGORIES.ALL
        else:
            cat = abort_if_no_category(category)
        for r in t.search(sstr).category(cat).order(ORDERS.SEEDERS.DES):
            search.append(append_torrent(r))
        return search

api.add_resource(Categories, '/cats')
api.add_resource(Top, '/top/<string:category>')
api.add_resource(Search, '/s/<string:category>/<string:sstr>')

if __name__ == '__main__':
        app.run(debug=True, host='0.0.0.0', port=5001)
