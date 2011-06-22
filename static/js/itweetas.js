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

// From http://diveintohtml5.org/storage.html
function web_storage() {
  try {
    return 'localStorage' in window && window['localStorage'] !== null;
  } catch (e) {
    return false;
  }
}

$(document).ready(function() {
  $('div#calibrate').hide();
  $('div#layout').hide();
  $('#why dd').hide();

  // Add expand/collapse button
  $('div#calibrate').before('<img role="button" class="collapse" id="calibrate_collapse" alt="Expand / collapse calibration section" src="static/images/fam/arrow_down.png"/>');
  $('div#layout').before('<img role="button" class="collapse" id="layout_collapse" alt="Expand / collapse layout section" src="static/images/fam/arrow_down.png"/>');

  $('img#calibrate_collapse').click(function() {
    $('div#calibrate').slideToggle(function() {
      if ($('div#calibrate').is(':visible')) {
        $('img#calibrate_collapse').attr('src', 'static/images/fam/arrow_up.png');
      }
      else {
        $('img#calibrate_collapse').attr('src', 'static/images/fam/arrow_down.png');
      }
    });
  });

  $('img#layout_collapse').click(function() {
    $('div#layout').slideToggle(function() {
      if ($('div#layout').is(':visible')) {
        $('img#layout_collapse').attr('src', 'static/images/fam/arrow_up.png');
      }
      else {
        $('img#layout_collapse').attr('src', 'static/images/fam/arrow_down.png');
      }
    });
  });

  $('#why dt').click(function(){
    $('#why dd').slideToggle();
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
