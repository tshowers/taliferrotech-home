/* taliferro.tech/investor-room: trade the password for signed video links.
   The links come from the investorRoom function and expire after two hours. */
( function () {
  var form = document.getElementById( 'room-gate' );
  var status = document.getElementById( 'room-status' );
  var shelf = document.getElementById( 'room-videos' );
  if ( !form ) return;

  var MESSAGES = {
    401: 'That password didn’t work. Check your invitation and try again.',
    429: 'Too many tries. Wait fifteen minutes and try again.'
  };

  function render ( videos ) {
    shelf.innerHTML = '';
    videos.forEach( function ( v ) {
      var card = document.createElement( 'div' );
      card.className = 'room__video';
      var h = document.createElement( 'h2' );
      h.className = 'h2 h2--sm';
      h.textContent = v.title;
      var video = document.createElement( 'video' );
      video.controls = true;
      video.preload = 'metadata';
      video.playsInline = true;
      video.setAttribute( 'controlsList', 'nodownload' );
      video.src = v.url;
      card.appendChild( h );
      card.appendChild( video );
      shelf.appendChild( card );
    } );
    shelf.hidden = false;
  }

  form.addEventListener( 'submit', function ( e ) {
    e.preventDefault();
    var button = form.querySelector( 'button' );
    button.disabled = true;
    status.textContent = 'Checking…';
    fetch( '/api/investor-room', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify( { password: form.password.value } )
    } ).then( function ( res ) {
      if ( !res.ok ) throw res.status;
      return res.json();
    } ).then( function ( data ) {
      status.textContent = '';
      form.hidden = true;
      render( data.videos );
      if ( window.gtag ) gtag( 'event', 'investor_room_open' );
    } ).catch( function ( code ) {
      status.textContent = MESSAGES[ code ] || 'Something went wrong. Try again, or email us.';
      button.disabled = false;
    } );
  } );
} )();
