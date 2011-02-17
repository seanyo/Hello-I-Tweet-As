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

// Break a single long string into an array of shorter strings that will fit
// int he given maxLength number of pixels when rendered in the given
// context.
function wrapTextIntoLines(context, text, maxLength) {
  var words = text.split(" ");
  var currentWordIndex = 0;
  var lines = [];

  while (currentWordIndex < words.length) {
    var currentLine = words[currentWordIndex++];
    while (context.measureText(currentLine + " "
                               + words[currentWordIndex + 1]).width
           < maxLength && currentWordIndex < words.length) {
      currentLine += " " + words[currentWordIndex++];
    }
    lines.push(currentLine);
  }

  return lines;
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
          var leftMargin = 1;
          var rightMargin = 1;
          var cornerRadius = 9;
          var headerHeight = 60;
          var footerHeight = 20;

          context.fillStyle = templateColour;
          context.strokeStyle = templateColour;
          context.lineWidth = strokeWidth;

          // Large solid rectangle with rounded corners
          context.beginPath();
          context.moveTo(0, cornerRadius);
          context.quadraticCurveTo(0, 0, cornerRadius, 0);
          context.lineTo(canvas.width - cornerRadius, 0);
          context.quadraticCurveTo(canvas.width, 0,
                                   canvas.width, cornerRadius);
          context.lineTo(canvas.width, canvas.height - cornerRadius);
          context.quadraticCurveTo(canvas.width, canvas.height,
                                   canvas.width - cornerRadius, canvas.height);
          context.lineTo(cornerRadius, canvas.height);
          context.quadraticCurveTo(0, canvas.height, 0,
                                   canvas.height - cornerRadius);
          context.closePath();
          context.fill();

          // Inner whitespace for content
          context.fillStyle = '#fff';
          context.fillRect(leftMargin, headerHeight,
                           canvas.width - rightMargin - leftMargin,
                           canvas.height - headerHeight - footerHeight);

          // Header text
          context.fillStyle = '#fff';
          context.font = 'bold 30px Arial, sans-serif';
          context.textAlign = 'center';
          context.textBaseline = 'top';
          context.fillText('HELLO', canvas.width / 2, 5);

          context.font = 'bold 20px Arial, sans-serif';
          context.fillText('I TWEET AS', canvas.width / 2, 35);

          // Twitter Avatar
          var avatar = new Image();
          avatar.src = data.profile_image_url.replace("normal", "bigger");

          // Wait a fifth of a second for the image to load before drawing it
          setTimeout(function() {
            context.drawImage(avatar, 10,
                              (canvas.height -
                               headerHeight -
                               footerHeight -
                               avatar.height) / 2 + headerHeight,
                              73, 73);
          }, 200);

          // Twitter account info
          context.fillStyle = '#000';
          context.font = 'bold 20px Arial, sans-serif';
          var fontSize = 20;
          var twitterName = '@' + data.screen_name;
          var maxWidth = canvas.width - 73 - 30;
          var centerPoint = (canvas.width - 83) / 2 + 83;
          while (context.measureText(twitterName) > maxWidth) {
            context.font =
              'bold {fontSize}px Arial, sans-serif'
              .supplant({fontSize: --fontSize});
          }
          context.fillText(twitterName, centerPoint, headerHeight + 10);

          context.font = '15px Arial, sans-serif';
          context.fillText(data.name, centerPoint, headerHeight + 35);
          context.font = '11px Arial, sans-serif';
          context.fillText(data.location, centerPoint, headerHeight + 55);

          if (data.description != "") {
            // The Description can be long, so we'll put up to two lines
            // worth and then end it
            context.font = 'italic 14px Arial, sans-serif';
            var lines = wrapTextIntoLines(context, data.description, maxWidth);

            // If the description will be cut off, append ellipses to the
            // second line.
            if (lines.length > 2) {
              lines[1] += '…';
            }
            if (lines.length > 0) {
              context.fillText(lines[0], centerPoint, headerHeight + 80);
            }
            if (lines.length > 1) {
              context.fillText(lines[1], centerPoint, headerHeight + 94);
            }
          }
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
