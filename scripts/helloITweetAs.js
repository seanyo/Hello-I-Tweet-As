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
          var templateColour = '#c11';
          var strokeWidth = 2;
          var cornerRadius = 13;
          var headerHeight = 60;
          var footerHeight = 20;

          context.fillStyle = templateColour;
          context.strokeStyle = templateColour;
          context.linewidth = strokeWidth;

          context.beginPath();
          context.moveTo(0, cornerRadius);
          context.quadraticCurveTo(0, 0, cornerRadius, 0);
          context.lineTo(canvas.width - cornerRadius, 0);
          context.quadraticCurveTo(canvas.width, 0,
                                   canvas.width, cornerRadius);
          context.lineTo(canvas.width, headerHeight);
          context.lineTo(0, headerHeight);
          context.closePath();
          context.fill();
          context.stroke();

          context.moveTo(0, canvas.height - footerHeight);
          context.lineTo(canvas.width, canvas.height - footerHeight);
          context.lineTo(canvas.width, canvas.height - cornerRadius);
          context.quadraticCurveTo(canvas.width, canvas.height,
                                   canvas.width - cornerRadius, canvas.height);
          context.lineTo(cornerRadius, canvas.height);
          context.quadraticCurveTo(0, canvas.height, 0,
                                   canvas.height - cornerRadius);
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
