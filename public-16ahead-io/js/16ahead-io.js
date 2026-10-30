/* 16ahead.io. The universal menu is tt/universal-menu.js; this file only
 * starts the looping video, unless the visitor asked for reduced motion,
 * in which case it shows the player controls instead. */
( function () {
  var video = document.querySelector( 'video[data-autoplay]' );
  if ( !video ) return;
  var reduce = window.matchMedia && window.matchMedia( '(prefers-reduced-motion: reduce)' );
  function apply () {
    if ( reduce && reduce.matches ) {
      video.pause();
      video.controls = true;
      return;
    }
    video.controls = false;
    var played = video.play();
    if ( played && played.catch ) played.catch( function () { video.controls = true; } );
  }
  apply();
  if ( reduce && reduce.addEventListener ) reduce.addEventListener( 'change', apply );
} )();
