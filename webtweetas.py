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
<style type="text/css">
div.step {
  background-color: #eee;
  border: 1px solid #ccc;
  border-radius: 7px;
  margin: 1em 0em;
  padding: 0.2em 1em;
}
</style>
</head>

<body>
<h1>Hello, I Tweet As</h1>
<form>
<div class="step">
<h2 id="calibrate_header">Calibrate the software (optional)</h2>
<div id="calibrate" class="collapse">
<p>We strongly recommend that you calibrate the software using <a href="/calibrate">this PDF</a> before generating name tags. This step minimizes misprinted label sheets.</p>
<p>Your fudge values</p>
1.<input id="fudge_x" value="0"/> 2.<input id="fudge_y" value="0"/>
</div>
</div>
<div class="step">
<h2>Generate your nametags</h3>
<div id="handles" class="collapse">
<p>Enter your Twitter ID and we'll make a name tag for you!</p>
@<input id="twitter_id"/>
</div>
</div>
<div class="step">
<h2 id="layout_header">Tweak the layout (optional)</h2>
<div id="layout" class="collapse">
<p>How many labels would you like to skip?</p>
<input id="skip_n_labels" value="0"/><br/>
</div>
</div>
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

$('input#fudge_x').blur(function() {
  if (web_storage()) {
    window.localStorage.setItem('fudge_x', $('input#fudge_x').val());
  }
});

$('input#fudge_y').blur(function() {
  if (web_storage()) {
    window.localStorage.setItem('fudge_y', $('input#fudge_y').val());
  }
});

$('form').submit(submit_form);

// From http://diveintohtml5.org/storage.html
function web_storage() {
  try {
    return 'localStorage' in window && window['localStorage'] !== null;
  } catch (e) {
    return false;
  }
}
</script>

<script type="text/javascript">
  $(document).ready(function() {
    $('div#calibrate').hide();
    $('div#layout').hide();

    $('h2#calibrate_header').click(function() {
      $('div#calibrate').slideToggle();
    });

    $('h2#layout_header').click(function() {
      $('div#layout').slideToggle();
    });

    // Load fudge values from web storage
    if (web_storage()) {
      var x, y;

      if (x = window.localStorage.getItem('fudge_x')) {
        $('input#fudge_x').val(x);
      }
      if (y = window.localStorage.getItem('fudge_y')) {
        $('input#fudge_y').val(y);
      }
    }
  });

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
