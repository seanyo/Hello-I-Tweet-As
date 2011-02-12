var tweeturl = "http://twitter.com/status/user_timeline/"+$.url.param("tid")+".json?count=1&callback=?";
$(document).ready(function(){
  $.getJSON(tweeturl, function(data){
    $.each(data, function(i, item) {
      var userPicURL = item.user.profile_image_url.replace("normal", "bigger");
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
