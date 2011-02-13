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
var tweeturl = "http://twitter.com/status/user_timeline/" +
  twitterID + ".json?count=1&callback=?";

$(document).ready(function(){
  $.getJSON(tweeturl, function(data){
    $.each(data, function(i, item) {
      var userPicURL =
        item.user.profile_image_url.replace("normal", "bigger");
      var screenName = item.user.screen_name;
      var name = item.user.name;
      var description = item.user.description;
      var location = item.user.location;
      var userPic='<img width=75 height=75 src="'+userPicURL+'" />';
      $('div.left').html(userPic);
      $('p.twitterID').html("@"+screenName);
      $('p.name').html(name+" "+location);
      $('p.description').html(description);
    });
  });
});
