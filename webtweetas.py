#!/usr/bin/env python2

try:
    import web
except ImportError, e:
    import sys
    print >> sys.stderr, "You need to install web.py"
    sys.exit(1)

from itweetas import LabelBuilder, LabelFormat, TwitterUser
from calibration import CalibrationPage


render = web.template.render('templates/')

urls = (
    '/', 'index',
    '/calibrate', 'calibrate',
    '/nametags', 'pdf'
    )

class index:
    def GET(self):
        return render.index()


class calibrate:
    def GET(self):
        calibrationPDF = CalibrationPage()

        web.header('Content-Type', 'application/pdf')
        web.header('Content-Disposition', 'attachment; filename="calibration.pdf"')
        return format(calibrationPDF.getPDF())


class pdf:
    def POST(self):
        i = web.input()

        users = i.users.split(',')

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


if __name__ == '__main__':
    app.run()
