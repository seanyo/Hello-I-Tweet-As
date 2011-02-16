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
      $("div#nametags").
        append(nameTagHTML(data.screen_name,
                           data.name,
                           data.description,
                           data.location,
                           data.profile_image_url.replace("normal",
                                                          "bigger")));
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
