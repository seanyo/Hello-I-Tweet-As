#!/usr/bin/env python2

try:
    import web
except ImportError, e:
    import sys
    print >> sys.stderr, "You need to install web.py"
    sys.exit(1)

from itweetas import LabelBuilder, LabelFormat, TwitterUser
from calibration import CalibrationPage


urls = (
    '/', 'index',
    '/calibrate', 'calibrate',
    '/(\d+)/([^/]+)/(-?\d+)/(-?\d+)/?', 'pdf'
    )

class index:
    def GET(self):
        return '''<html>
<head>
<title>Hello, I tweet as...</title>
</head>

<body>
<h1>Hello, I Tweet As</h1>
<form>
<h2>Step 1: Calibrate the software</h2>
<p>We strongly recommend that you calibrate the software using <a href="/calibrate">this PDF</a> before generating name tags. This step minimizes misprinted label sheets.</p>
<p>Your fudge values</p>
1.<input id="fudge_x" value="0"/> 2.<input id="fudge_y" value="0"/>
<h2>Step 2: Generate your nametags</h3>
<p>Enter your Twitter ID and we'll make a name tag for you!</p>
@<input id="twitter_id"/>
<h2>Tweak the layout</h2>
<p>How many labels would you like to skip?</p>
<input id="skip_n_labels" value="0"/><br/>
<input type="submit" value="Make me a Twitter name tag!"/>
</form>
</body>
<script type="text/javascript" src="http://code.jquery.com/jquery-1.5.2.min.js"></script>
<script type="text/javascript">
function submit_form(event) {
  window.location = '/' + $('#skip_n_labels').val() + '/' + $('#twitter_id').val() +
    '/' + $('#fudge_x').val() + '/' + $('#fudge_y').val() + '/';
  return false;
}

/*
$('#twitter_id').keypress(function(event) {
  var code = (event.keyCode ? event.keyCode : event.which);

  // Enter
  if (code == 13) {
    if ($('#twitter_id').val() !== '') {
      submit_form();
    }
    return false;
  }
});
*/
$('form').submit(submit_form);
</script>
</html>
'''


class calibrate:
    def GET(self):
        calibrationPDF = CalibrationPage()

        web.header('Content-Type', 'application/pdf')
        web.header('Content-Disposition', 'attachment; filename="calibration.pdf"')
        return format(calibrationPDF.getPDF())


class pdf:
    def GET(self, offset, users, fudge_x, fudge_y):
        users = users.split(',')

        builder = LabelBuilder(LabelFormat())
        builder.setFudge(int(fudge_x), int(fudge_y))

        for user in users:
            builder.addUser(TwitterUser(user))

        builder.generatePDF(offset=int(offset))

        web.header('Content-Type', 'application/pdf')
        web.header('Content-Disposition', 'attachment; filename="nametags.pdf"')
        return format(builder.getPDF())


app = web.application(urls, globals())


if __name__ == '__main__':
    app.run()
