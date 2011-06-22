#!/usr/bin/env python2

import ConfigParser, os, urlparse

try:
    import web
except ImportError, e:
    import sys
    print >> sys.stderr, "You need to install web.py"
    sys.exit(1)

import oauth2 as oauth

from itweetas import LabelBuilder, LabelFormat, TwitterUser
from calibration import CalibrationPage


# We don't want web.seeother() to include the script name in the URL
os.environ['REAL_SCRIPT_NAME'] = ''

render = web.template.render('templates/')

urls = (
    '/', 'index',
    '/calibrate', 'calibrate',
    '/login', 'login',
    '/logout', 'logout',
    '/nametags', 'pdf'
    )

class index:
    def GET(self):
        user = ''
        if hasattr(session, 'access_token'):
            user = session.access_token['screen_name']
        return render.index(user=user)


class calibrate:
    def GET(self):
        calibrationPDF = CalibrationPage()

        web.header('Content-Type', 'application/pdf')
        web.header('Content-Disposition', 'attachment; filename="calibration.pdf"')
        return format(calibrationPDF.getPDF())


class login:
    def GET(self):
        i = web.input()

        config = ConfigParser.ConfigParser()
        config.read('itweetas.cfg')

        consumer_key = config.get('oauth', 'consumer_key')
        consumer_secret = config.get('oauth', 'consumer_secret')

        request_token_url = 'https://twitter.com/oauth/request_token'
        access_token_url = 'https://twitter.com/oauth/access_token'
        authorize_url = 'https://twitter.com/oauth/authorize'

        consumer = oauth.Consumer(consumer_key, consumer_secret)
        client = oauth.Client(consumer)

        if hasattr(i, 'oauth_token') and hasattr(i, 'oauth_verifier'):
            # We're back from Twitter with a successful authentication
            token = oauth.Token(i.oauth_token,
                                session.oauth_token_secret)
            token.set_verifier(i.oauth_verifier)
            client = oauth.Client(consumer, token)

            resp, content = client.request(access_token_url, "POST")
            session.access_token = dict(urlparse.parse_qsl(content))

            raise web.seeother('/')

        elif hasattr(i, 'denied'):
            # We're back from Twitter but were not granted access
            # TODO: Report the error somehow
            raise web.seeother('/')

        else:
            # We need to send our authorization request out to Twitter
            resp, content = client.request(request_token_url, "GET")
            if resp['status'] != '200':
                raise Exception("Invalid response %s." % resp['status'])

            request_token = dict(urlparse.parse_qsl(content))

            session.oauth_token = request_token['oauth_token']
            session.oauth_token_secret = request_token['oauth_token_secret']

            raise web.seeother('{0}?oauth_token={1}'.format(authorize_url,
                                                      request_token['oauth_token']))


class logout:
    def GET(self):
        session.kill()
        raise web.seeother('/')


class pdf:
    def POST(self):
        i = web.input()

        users = i.users.split(',')
        users = map(lambda x: x.strip(), users)

        builder = LabelBuilder(LabelFormat())
        # TODO: Try/catch here for invalid fudge values
        builder.setFudge(i.fudge_x, i.fudge_y)

        for user in users:
            builder.addUser(TwitterUser(user))

        builder.generatePDF(offset=int(i.offset))

        web.header('Content-Type', 'application/pdf')
        web.header('Content-Disposition', 'attachment; filename="nametags.pdf"')
        return format(builder.getPDF())


app = web.application(urls, globals())
session = web.session.Session(app, web.session.DiskStore('sessions'),
                              initializer={'user': None})


if __name__ == '__main__':
    app.run()
