// Retrieve the value of a given URL parameter. Return undefined if the
// parameter does not exist.
//
// TODO: Prevent this from re-parsing the URL each time.
function getParam(key) {
  var searchString = window.location.search;

  // Remove the leading '?'
  if (searchString.match(/^\?/)) {
    searchString = searchString.slice(1);
  }

  var params = {};

  // There's got to be a better way... but this works for now.
  searchString.split("&").forEach(
    function(paramString) {
      if (paramString != undefined) {
        var parts = paramString.split("=");
        params[parts[0]] = parts[1];
      }
    });

  return params[key];
}

function nameTagHTML(screenName, name, description, location, userPicUrl) {
  var html = '<div class="top">\
<h1>HELLO</h1>\
<p class="subtitle">I Tweet As</p>\
</div>\
<div class="middle">\
<div class="left">\
<img src="{userPicUrl}"/>\
</div>\
<div class="right">\
<p class="twitterID">@{screenName}</p>\
<p class="name">{name}<br/>{location}</p>\
<p class="description">{description}</p>\
</div>\
</div>\
<div class="bottom"/>'.supplant({description: description,
                                 location: location,
                                 name: name,
                                 screenName: screenName,
                                 userPicUrl: userPicUrl});

  return html;
}


var twitterID = getParam("tid");
if (twitterID != undefined) {
    var tweeturl = "http://api.twitter.com/1/users/show/" +
        twitterID + ".json";
}

$(document).ready(function() {
  // Need to suppress regular HTTP response codes since jQuery's JSONP
  // support doesn't handle error callbacks for cross-domain requests. True
  // as of jQuery 1.5.
  $.getJSON(tweeturl + "?suppress_response_codes&callback=?", function(data) {
    if (data.error === undefined) {
      // Create a new canvas element
      $("div#nametags")
        .append('<canvas id="nametag" width="300" height="200">\
Your browser doesn\'t support canvas!\
</canvas>');

      var canvas = document.getElementById("nametag");

      if (canvas && canvas.getContext) {
        var context = canvas.getContext('2d');

        if (context) {
          context.fillStyle = '#c11';
          context.strokeStyle = '#c11';
          context.linewidth = 2;
          // context.fillRect(0, 0, 300, 60);
          // context.fillRect(0, 180, 300, 200);

          context.beginPath();
          context.moveTo(0, 10);
          context.quadraticCurveTo(0, 0, 10, 0);
          context.lineTo(290, 0);
          context.quadraticCurveTo(300, 0, 300, 10);
          context.lineTo(300, 60);
          context.lineTo(0, 60);
          context.closePath();
          context.fill();
          context.stroke();

          context.moveTo(0, 180);
          context.lineTo(300, 180);
          context.lineTo(300, 190);
          context.quadraticCurveTo(300, 200, 290, 200);
          context.lineTo(10, 200);
          context.quadraticCurveTo(0, 200, 0, 190);
          context.closePath();
          context.fill();
          context.stroke();

          context.moveTo(0, 60);
          context.lineTo(0, 180);
          context.moveTo(300, 180);
          context.lineTo(300, 60);
          context.stroke();
        }
      }
    }
    else {
      // Because we had to suppress HTTP error codes (see above) we don't get
      // numeric errors. Have to test against strings to figure out what
      // broke.
      switch (data.error) {
        case "Not found":
          $("div#nametags").append("Error: Could not retrieve Twitter profile for '" + twitterID + "'.");
          break;
        case "Internal server error":
          $("div#nametags").append("Error: Twitter appears to be down.");
          break;
        case "Service unavailable":
          $("div#nametags").append("Error: Twitter is experiencing heavy load.");
          break;
        default:
          $("div#nametags").append("Error: Something went wrong.");
          break;
      }
    }
  });
});
