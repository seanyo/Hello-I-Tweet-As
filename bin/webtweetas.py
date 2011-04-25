#!/usr/bin/env python2

try:
    import web
except ImportError, e:
    import sys
    print >> sys.stderr, "You need to install web.py"
    sys.exit(1)


urls = (
    '/', 'index',
    '/(\d+)/([^/]+)/(-?\d+)/(-?\d+)/?', 'pdf'
    )

class index:
    def GET(self):
        return 'Hello, World!'


class pdf:
    def GET(self, offset, users, fudge_x, fudge_y):
        users = users.split(',')

        return '''Fudge: {0}, {1}
Offset: {3}
Users:
- {2}'''.format(fudge_x, fudge_y, '''
- '''.join(users), offset)


app = web.application(urls, globals())


if __name__ == '__main__':
    app.run()
