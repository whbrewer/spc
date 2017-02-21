function user_defaults() {
    set_style()
}

var style_cookie_name = "theme" ;
var style_cookie_duration = 360;
var style_domain = window.location.hostname;

function switch_style ( css_title )
{
// You may use this script on your site free of charge provided
// you do not remove this notice or the URL below. Script from
// https://www.thesitewizard.com/javascripts/change-style-sheets.shtml
  var i, link_tag ;
  for (i = 0, link_tag = document.getElementsByTagName("link") ;
    i < link_tag.length ; i++ ) {
    if ((link_tag[i].rel.indexOf( "stylesheet" ) != -1) &&
      link_tag[i].title) {
      link_tag[i].disabled = true ;
      if (link_tag[i].title == css_title) {
        link_tag[i].disabled = false ;
      }
    }
    $.post('/theme', { 'theme': css_title });
  }
}

function set_style()
{
  $.get( "/theme", function( data ) {
      if (data.length) { switch_style( data ) }
  });
}
