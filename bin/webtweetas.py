#!/usr/bin/env python2

try:
    import web
except ImportError, e:
    import sys
    print >> sys.stderr, "You need to install web.py"
    sys.exit(1)

from itweetas import LabelBuilder, LabelFormat, TwitterUser


urls = (
    '/', 'index',
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
<p>Enter your Twitter ID and we'll make a name tag for you!</p>
<form>
@<input id="twitter_id"/><br/>
<input type="submit" value="Make me a Twitter name tag!"/>
</form>
</body>
<script type="text/javascript" src="http://code.jquery.com/jquery-1.5.2.min.js"></script>
<script type="text/javascript">
function submit_form(event) {
  window.location = '/0/' + $('#twitter_id').val() + '/0/0/';
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
