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


var twitterID = getParam("tid");
var tweeturl = "http://api.twitter.com/1/users/show/" + twitterID + ".json";

$(document).ready(function() {
  // Need to suppress regular HTTP response codes since jQuery's JSONP
  // support doesn't handle error callbacks for cross-domain requests. True
  // as of jQuery 1.5.
  $.getJSON(tweeturl + "?suppress_response_codes&callback=?", function(data) {
    if (data.error === undefined) {
      var userPicURL = data.profile_image_url.replace("normal", "bigger");
      var screenName = data.screen_name;
      var name = data.name;
      var description = data.description;
      var location = data.location;
      var userPic='<img width=75 height=75 src="'+userPicURL+'" />';
      $('div.left').html(userPic);
      $('p.twitterID').html("@"+screenName);
      $('p.name').html(name+" "+location);
      $('p.description').html(description);
    }
    else {
      // Because we had to suppress HTTP error codes (see above) we don't get
      // numeric errors. Have to test against strings to figure out what
      // broke.
      switch (data.error) {
        case "Not found":
          $("p.twitterID").html("Error: Could not retrieve your profile.");
          break;
        case "Internal server error":
          $("p.twitterID").html("Error: Twitter appears to be down.");
          break;
        case "Service unavailable":
          $("p.twitterID").html("Error: Twitter is experiencing heavy load.");
          break;
        default:
          $("p.twitterID").html("Error: Something went wrong.");
          break;
      }
    }
  });
});
