/* 16ahead.com. The universal menu is tt/universal-menu.js; this file is the
 * hero dial and the /privacy-rights form, the same as taliferro.tech's (public/js/site.js). */

/* The hero dial: the highlight hops between the 16 ticks (one per app) at
 * random, so the logo reads as the apps working together. Still for reduced motion. */
( function () {
  var lit = document.querySelectorAll( '.dial__lit' );
  if ( !lit.length || window.matchMedia( '(prefers-reduced-motion: reduce)' ).matches ) return;
  var on = 1;
  function hop () {
    var next = Math.floor( Math.random() * ( lit.length - 1 ) );
    if ( next >= on ) next++;
    lit[on].classList.remove( 'is-on' );
    lit[next].classList.add( 'is-on' );
    on = next;
    setTimeout( hop, 550 + Math.random() * 450 );
  }
  setTimeout( hop, 900 );
} )();

/* Overnight rows: a poster opens its video in the full-size player (dialog.watch).
 * One video plays at a time; each video's first play is a GA event. */
( function () {
  var dlg = document.querySelector( 'dialog.watch' );
  var player = dlg && dlg.querySelector( 'video' );
  var videos = Array.prototype.slice.call( document.querySelectorAll( '.story' ) );
  if ( player ) videos.push( player );
  videos.forEach( function ( v ) {
    v.addEventListener( 'play', function () {
      videos.forEach( function ( o ) { if ( o !== v ) o.pause(); } );
      var title = v.dataset.title || v.getAttribute( 'aria-label' );
      if ( window.gtag && v.dataset.started !== title ) gtag( 'event', 'video_start', { video_title: title } );
      v.dataset.started = title;
    } );
  } );
  if ( !dlg ) return;
  document.querySelectorAll( '.run__play' ).forEach( function ( btn ) {
    btn.addEventListener( 'click', function () {
      dlg.querySelector( '.watch__bar b' ).textContent = btn.dataset.title;
      player.dataset.title = btn.dataset.title;
      player.poster = btn.dataset.poster;
      player.src = btn.dataset.video;
      dlg.showModal();
      player.play().catch( function () {} );
    } );
  } );
  dlg.querySelector( '.watch__close' ).addEventListener( 'click', function () { dlg.close(); } );
  dlg.addEventListener( 'click', function ( e ) { if ( e.target === dlg ) dlg.close(); } );
  dlg.addEventListener( 'close', function () { player.pause(); player.removeAttribute( 'src' ); player.load(); } );
} )();

( function () {
  var form = document.querySelector( 'form.rights' );
  if ( !form ) return;
  var type = form.elements.type;
  function hints () {
    form.querySelectorAll( '.rights__hint' ).forEach( function ( h ) { h.hidden = h.dataset.for !== type.value; } );
  }
  type.addEventListener( 'change', hints );
  hints();
  form.addEventListener( 'submit', function ( e ) {
    e.preventDefault();
    var email = form.elements.email.value.trim();
    if ( !email ) return;
    var label = type.options[type.selectedIndex].dataset.label;
    var subject = 'CCPA/GDPR ' + label + ' Request — ' + email;
    var body = 'Request type: ' + label + '\nEmail: ' + email + '\n\nDetails:\n' + ( form.elements.details.value.trim() || 'N/A' ) +
      '\n\nSubmitted via 16ahead.com on ' + new Date().toISOString() + '.';
    window.location.href = 'mailto:' + form.dataset.rightsEmail + '?subject=' + encodeURIComponent( subject ) + '&body=' + encodeURIComponent( body );
    form.hidden = true;
    document.querySelector( '.rights__done' ).hidden = false;
  } );
} )();
