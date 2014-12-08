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

# convert a twolevel constants to flatten dict
#  { 'other:other' => CATEGORIES.OTHER.OTHER }
def make_twolevel_constants(obj, result={}):
    # main level
    main = [e for e in dir(obj) if not e.startswith('_')]

    # sub level, except 'ALL'
    for main_entry in [e for e in main if not e == 'ALL']:
        sub_obj = getattr(obj, main_entry)
        for sub_entry in [e for e in dir(sub_obj) if not e.startswith('_')]:
            key   = '{0}:{1}'.format(main_entry.lower(), sub_entry.lower())
            result[key] = getattr(sub_obj, sub_entry)

    return result

categories = make_twolevel_constants(CATEGORIES, {'all': CATEGORIES.ALL})
orders = make_twolevel_constants(ORDERS)

def abort_on_mistake(a_dict, a_value):
    try:
        return a_dict[a_value.lower()]
    except KeyError:
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
    def get(self):
        return categories.keys()

class Top(Resource):
    def get(self, category):
        top = []
        cat = abort_on_mistake(categories, category)
        for r in t.top().category(cat):
            top.append(append_torrent(r))
        return top

class Search(Resource):
    def get(self, category='all', sstr=None, sort=ORDERS.SEEDERS.DES):
        search = []

        cat = abort_on_mistake(categories, category)

        for r in t.search(sstr).category(cat).order(sort):
            search.append(append_torrent(r))
        return search

class SortSearch(Resource):
    def get(self, category='all', sstr=None, sort='seeders:des'):
        s = abort_on_mistake(orders, sort)
        print(s)
        return Search.get(self, category=category, sstr=sstr, sort=s)


api.add_resource(Categories, '/cats')
api.add_resource(Top, '/top/<string:category>')
api.add_resource(Search, '/s/<string:category>/<string:sstr>')
api.add_resource(SortSearch, '/s/<string:category>/<string:sstr>/<string:sort>')

if __name__ == '__main__':
        app.run(debug=True, host='0.0.0.0', port=5001)
