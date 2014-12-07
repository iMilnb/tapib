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

# main subject and default value
constants = {
            'cat': [CATEGORIES, CATEGORIES.ALL],
            'order': [ORDERS, ORDERS.SEEDERS.DES]
        }

def abort_on_mistake(var, filtr):
    try:
        if not ':' in filtr:
            # return default value
            return constants[var][1]
        k, v = filtr.split(':')
        return getattr(getattr(constants[var][0], k.upper()), v.upper())
    except AttributeError:
        abort(404, message='unkown value')

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
    categories = ['all']
    def get(self):
        if len(self.categories) > 1:
            return self.categories
        # main categories
        cats = [a for a in dir(CATEGORIES) if not a.startswith('__')]
        # sub categories except ALL
        for c in [s for s in cats if not s == 'ALL']:
            subcat = getattr(CATEGORIES, c)
            for sub in [s for s in dir(subcat) if not s.startswith('__')]:
                self.categories.append('{0}:{1}'.format(c.lower(), sub.lower()))
        return self.categories

class Top(Resource):
    def get(self, category):
        top = []
        cat = abort_on_mistake('cat', category)
        for r in t.top().category(cat):
            top.append(append_torrent(r))
        return top

class Search(Resource):
    def get(self, category='all', sstr=None, sort=ORDERS.SEEDERS.DES):
        search = []

        cat = abort_on_mistake('cat', category)

        for r in t.search(sstr).category(cat).order(sort):
            search.append(append_torrent(r))
        return search

class SortSearch(Resource):
    def get(self, category='all', sstr=None, sort='seeders:des'):
        s = abort_on_mistake('order', sort)
        print(s)
        return Search.get(self, category=category, sstr=sstr, sort=s)


api.add_resource(Categories, '/cats')
api.add_resource(Top, '/top/<string:category>')
api.add_resource(Search, '/s/<string:category>/<string:sstr>')
api.add_resource(SortSearch, '/s/<string:category>/<string:sstr>/<string:sort>')

if __name__ == '__main__':
        app.run(debug=True, host='0.0.0.0', port=5001)
