/* taliferro.tech/investor-room
   R0: the locked entry is in the HTML. R1: the room is drawn here from
   GET /api/investor-room/room, which only answers with a valid session, so
   no terms, numbers or document links ever ship in this file or the page. */
( function () {
  'use strict';
  var root = document.getElementById( 'iroom' );
  if ( !root ) return;
  var gate = document.getElementById( 'room-gate' );
  var status = document.getElementById( 'room-status' );
  var app = document.getElementById( 'room-app' );
  var data = null;

  /* ------------------------------------------------------------ helpers */
  var P = {
    check: '<path d="M20 6 9 17l-5-5"/>',
    calendar: '<rect width="18" height="18" x="3" y="4" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
    download: '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="m7 10 5 5 5-5M12 15V3"/>',
    play: '<path d="m7 4 13 8-13 8V4z" fill="currentColor"/>',
    eye: '<path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/><circle cx="12" cy="12" r="3"/>',
    film: '<rect width="18" height="18" x="3" y="3" rx="2"/><path d="M7 3v18M17 3v18M3 7.5h4M3 12h18M3 16.5h4M17 7.5h4M17 16.5h4"/>',
    file: '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/>',
    shield: '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/>',
    pie: '<path d="M21.21 15.89A10 10 0 1 1 8 2.83"/><path d="M22 12A10 10 0 0 0 12 2v10z"/>',
    sheet: '<rect width="18" height="18" x="3" y="3" rx="2"/><path d="M3 9h18M3 15h18M9 3v18"/>',
    user: '<circle cx="12" cy="8" r="5"/><path d="M20 21a8 8 0 0 0-16 0"/>',
    message: '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>',
    left: '<path d="m15 18-6-6 6-6"/>',
    right: '<path d="m9 18 6-6-6-6"/>',
    expand: '<path d="M15 3h6v6M9 21H3v-6M21 3l-7 7M3 21l7-7"/>',
    logout: '<path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4M16 17l5-5-5-5M21 12H9"/>'
  };
  function ico( name, size ) {
    size = size || 18;
    return '<svg class="i" width="' + size + '" height="' + size + '" viewBox="0 0 24 24" fill="none" stroke="currentColor" ' +
      'stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + ( P[ name ] || P.file ) + '</svg>';
  }
  function esc( s ) {
    return String( s == null ? '' : s ).replace( /[&<>"']/g, function ( c ) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[ c ];
    } );
  }
  function money( n ) { return '$' + Number( n ).toLocaleString( 'en-US' ); }
  function longDate( iso ) {
    var p = String( iso ).split( '-' );
    return new Date( Date.UTC( +p[ 0 ], +p[ 1 ] - 1, +p[ 2 ] ) ).toLocaleDateString( 'en-US', { month: 'long', day: 'numeric', year: 'numeric', timeZone: 'UTC' } );
  }
  function api( path, body ) {
    return fetch( '/api/investor-room/' + path, {
      method: body ? 'POST' : 'GET',
      credentials: 'same-origin',
      headers: body ? { 'Content-Type': 'application/json' } : {},
      body: body ? JSON.stringify( body ) : undefined
    } );
  }
  function track( type, ref, value ) {
    api( 'event', { type: type, ref: ref, value: value } ).catch( function () {} );
  }
  function setState( s ) { root.setAttribute( 'data-state', s ); }

  /* ------------------------------------------------------------ R0: gate */
  var codeInput = gate.elements.code;
  var agree = gate.elements.agree;
  var enter = gate.querySelector( '.iroom__enter' );
  function ready() {
    enter.disabled = codeInput.value.replace( /[^a-z0-9]/gi, '' ).length < 12 || !agree.checked;
  }
  codeInput.addEventListener( 'input', function () { status.textContent = ''; ready(); } );
  agree.addEventListener( 'change', ready );

  gate.addEventListener( 'submit', function ( e ) {
    e.preventDefault();
    if ( enter.disabled ) return;
    enter.disabled = true;
    enter.textContent = 'Checking…';
    api( 'signin', { code: codeInput.value, agree: agree.checked } ).then( function ( res ) {
      if ( res.ok ) return openRoom();
      return res.json().catch( function () { return {}; } ).then( function ( j ) {
        status.textContent =
          res.status === 401 ? 'That code didn’t work. Check your invitation email.' :
          res.status === 429 ? 'Too many tries. Try again in 15 minutes.' :
          res.status === 410 ? 'This code has expired. We’ve let ' + ( j.contact || 'your contact' ) + ' know.' :
          'Something went wrong. Try again, or email us.';
      } );
    } ).catch( function () {
      status.textContent = 'Something went wrong. Try again, or email us.';
    } ).then( function () {
      enter.textContent = 'Enter the room';
      ready();
    } );
  } );

  /* ------------------------------------------------------------ R1: room */
  function openRoom() {
    return api( 'room' ).then( function ( res ) {
      if ( !res.ok ) { setState( 'locked' ); return; }
      return res.json().then( function ( d ) {
        data = d;
        app.innerHTML = render( d );
        app.hidden = false;
        setState( 'open' );
        codeInput.value = '';
        wire();
        window.scrollTo( 0, 0 );
        if ( window.gtag ) gtag( 'event', 'investor_room_open' );
      } );
    } ).catch( function () { setState( 'locked' ); } );
  }

  function render( d ) {
    return [ welcome( d ), terms( d.terms ), video( d ), deck( d ), numbers( d.numbers ), portfolio( d.portfolio ),
      acquisition( d.acquisition ), risks( d.risks ), diligence( d ), footer( d ) ].join( '' );
  }

  function welcome( d ) {
    var c = d.contact;
    var book = c.bookingUrl || ( 'mailto:' + c.email + '?subject=' + encodeURIComponent( 'Investor call: ' + d.investor.name ) );
    return '<section class="iroom__welcome" data-section="welcome">' +
      '<div class="iroom__hello">' +
        '<div class="iroom__meta"><span class="tag t-blue">Investor room · Confidential</span>' +
        '<span>Updated ' + esc( longDate( d.updatedAt ) ) + '</span>' +
        '<button class="iroom__signout" type="button" data-signout>' + ico( 'logout', 14 ) + 'Sign out</button></div>' +
        '<h1 class="display display--md">Welcome, ' + esc( d.investor.firstName ) + '.</h1>' +
        '<p class="lede">You’ve seen the story. This room has what the public page doesn’t: the terms, the numbers, the portfolio and the risks.</p>' +
      '</div>' +
      '<aside class="iroom__contact"><span class="iroom__kicker">Your contact</span>' +
        '<div class="iroom__person"><span class="iroom__avatar">' + esc( c.initials ) + '</span>' +
        '<span><b>' + esc( c.name ) + '</b><small>' + esc( c.title ) + '</small></span></div>' +
        '<a class="iroom__btn iroom__btn--accent" href="' + esc( book ) + '"' + ( c.bookingUrl ? ' target="_blank" rel="noopener"' : '' ) + '>' +
        ico( 'calendar', 16 ) + 'Book a call</a>' +
      '</aside></section>';
  }

  function terms( t ) {
    var rows = [ [ 'Raising', t.raising ], [ 'Instrument', t.instrument ], [ 'Valuation cap', t.valuationCap ],
      [ 'Minimum check', t.minimumCheck ], [ 'Target close', t.targetClose ] ].filter( function ( r ) { return r[ 1 ]; } );
    if ( !rows.length ) return '';
    return '<section class="iroom__terms" data-section="terms" aria-label="Key terms">' + rows.map( function ( r ) {
      return '<div class="iroom__term"><span class="iroom__kicker">' + esc( r[ 0 ] ) + '</span><b>' + esc( r[ 1 ] ) + '</b></div>';
    } ).join( '' ) + '</section>';
  }

  function video( d ) {
    if ( !d.videos || !d.videos.length ) return '';
    var v = d.videos[ 0 ];
    return '<section class="iroom__sec" data-section="video" id="room-video">' +
      '<span class="iroom__kicker">Watch first</span><h2 class="h2 h2--sm">From the founders, in two minutes</h2>' +
      '<div class="iroom__videogrid">' +
        '<div class="iroom__player" data-video="' + esc( v.id ) + '">' +
          '<video preload="none" playsinline controlslist="nodownload" poster="' + esc( d.videoPoster || '' ) + '" src="' + esc( v.url ) + '"></video>' +
          '<div class="iroom__overlay"><span class="iroom__presenter">' + esc( v.presenter + ' · ' + v.length ) + '</span>' +
          '<button class="iroom__play" type="button" aria-label="Play ' + esc( v.title ) + '">' + ico( 'play', 26 ) + '</button></div>' +
        '</div>' +
        '<div class="iroom__list"><span class="iroom__kicker">Videos</span>' +
          d.videos.map( function ( x, i ) {
            return '<button class="iroom__chapter' + ( i === 0 ? ' is-on' : '' ) + '" type="button" data-pick="' + esc( x.id ) + '">' +
              '<span>' + esc( x.length ) + '</span>' + esc( x.title ) + '</button>';
          } ).join( '' ) +
          '<p class="iroom__note">Not the pitch again. You already have that.</p>' +
        '</div>' +
      '</div></section>';
  }

  function deck( d ) {
    var k = d.deck;
    if ( !k || !k.slides || !k.slides.length ) return '';
    return '<section class="iroom__sec" data-section="deck" id="room-deck">' +
      '<div class="iroom__sechead"><div><span class="iroom__kicker">The deck</span><h2 class="h2 h2--sm">' + k.slides.length + ' slides</h2></div>' +
      '<div class="iroom__secactions"><a class="iroom__pill iroom__pill--surface" href="/api/investor-room/doc?id=' + encodeURIComponent( k.pdf ) + '">' + ico( 'download', 15 ) + 'Download PDF</a>' +
      '<button class="iroom__pill iroom__pill--surface" type="button" data-fullscreen>' + ico( 'expand', 15 ) + 'Full screen</button></div></div>' +
      '<div class="iroom__decktray">' +
        '<div class="iroom__stage" tabindex="0" aria-roledescription="slide viewer" aria-label="Investor deck, use the arrow keys">' +
          '<button class="iroom__nav iroom__nav--prev" type="button" aria-label="Previous slide" data-step="-1">' + ico( 'left', 20 ) + '</button>' +
          '<img class="iroom__slide" alt="" src="' + esc( k.slides[ 0 ].url ) + '">' +
          '<button class="iroom__nav iroom__nav--next" type="button" aria-label="Next slide" data-step="1">' + ico( 'right', 20 ) + '</button>' +
        '</div>' +
        '<div class="iroom__thumbs">' + k.slides.map( function ( sl, i ) {
          return '<button class="iroom__thumb' + ( i === 0 ? ' is-on' : '' ) + '" type="button" data-slide="' + i + '">' +
            '<img src="' + esc( sl.url ) + '" alt="" loading="lazy"><span>' + ( i < 9 ? '0' : '' ) + ( i + 1 ) + ' ' + esc( sl.title ) + '</span></button>';
        } ).join( '' ) + '</div>' +
        '<p class="iroom__dots" aria-live="polite"></p>' +
      '</div></section>';
  }

  function numbers( n ) {
    if ( !n ) return '';
    var bars = n.revenueByYear || [];
    var max = Math.max.apply( null, bars.map( function ( b ) { return b.value || 0; } ).concat( [ 1 ] ) );
    var chart = bars.length ? '<div class="iroom__panel"><div class="iroom__panelhead"><h3>Revenue by year</h3></div>' +
      '<div class="iroom__bars">' + bars.map( function ( b ) {
        var h = b.value ? Math.max( 4, Math.round( b.value / max * 100 ) ) : 0;
        return '<div class="iroom__bar"><span class="iroom__barval">' + money( b.value ) + '</span>' +
          '<span class="iroom__barfill' + ( b.value ? '' : ' is-zero' ) + '" style="height:' + h + '%"></span>' +
          '<span class="iroom__barlab">' + esc( b.label ) + '</span>' +
          ( b.note ? '<small>' + esc( b.note ) + '</small>' : '' ) + '</div>';
      } ).join( '' ) + '</div>' +
      ( n.revenueNote ? '<p class="iroom__note">' + esc( n.revenueNote ) + '</p>' : '' ) + '</div>' : '';
    var stats = ( n.stats || [] ).filter( function ( s ) { return s.value; } );
    var side = stats.length ? '<div class="iroom__panel iroom__stats">' + stats.map( function ( s ) {
      return '<div class="iroom__stat"><span class="iroom__kicker">' + esc( s.label ) + '</span><b>' + esc( s.value ) + '</b></div>';
    } ).join( '' ) + '</div>' : '';
    if ( !chart && !side ) return '';
    return '<section class="iroom__sec" data-section="numbers"><span class="iroom__kicker">The numbers</span>' +
      '<h2 class="h2 h2--sm">Where the business is today</h2><div class="iroom__numgrid">' + chart + side + '</div></section>';
  }

  function portfolio( p ) {
    if ( !p ) return '';
    return '<section class="iroom__sec" data-section="portfolio"><span class="iroom__kicker">Why invest</span>' +
      '<h2 class="h2 h2--sm">A portfolio of bets</h2>' + ( p.lede ? '<p class="iroom__lede">' + esc( p.lede ) + '</p>' : '' ) +
      ( p.pricing && p.pricing.length ? '<div class="iroom__prices">' + p.pricing.map( function ( x ) {
        return '<div class="iroom__price"><span class="iroom__kicker">' + esc( x.label ) + '</span><b>' + esc( x.value ) + '</b><small>' + esc( x.unit ) + '</small></div>';
      } ).join( '' ) + '</div>' : '' ) +
      '<div class="iroom__apps">' + ( p.apps || [] ).map( function ( a ) {
        return '<div class="iroom__app"><span class="chip t-' + esc( a.tint || 'blue' ) + '" style="--sz:44px" aria-hidden="true">' +
          '<span class="glyph" style="--g:url(/img/products/' + esc( a.glyph ) + ')"></span></span>' +
          '<span><b>' + esc( a.name ) + '</b><small>' + esc( a.platforms ) + ( a.price ? ' · ' + esc( a.price ) : '' ) + '</small></span></div>';
      } ).join( '' ) + '</div></section>';
  }

  function acquisition( a ) {
    if ( !a || !a.items || !a.items.length ) return '';
    return '<section class="iroom__sec" data-section="acquisition"><span class="iroom__kicker">Why invest</span>' +
      '<h2 class="h2 h2--sm">Acquisition ready</h2>' + ( a.lede ? '<p class="iroom__lede">' + esc( a.lede ) + '</p>' : '' ) +
      '<div class="iroom__facts">' + a.items.map( function ( x ) {
        return '<div class="iroom__fact"><b>' + esc( x.value ) + '</b><h3>' + esc( x.title ) + '</h3><p>' + esc( x.detail ) + '</p></div>';
      } ).join( '' ) + '</div></section>';
  }

  function risks( r ) {
    if ( !r || !r.length ) return '';
    return '<section class="iroom__sec" data-section="risks"><span class="iroom__kicker">Risks</span>' +
      '<h2 class="h2 h2--sm">What could slow us down</h2><div class="iroom__risks">' + r.map( function ( x ) {
        return '<div class="iroom__risk"><h3>' + esc( x.title ) + '</h3><p>' + esc( x.detail ) + '</p></div>';
      } ).join( '' ) + '</div></section>';
  }

  function diligence( d ) {
    var docs = ( d.documents || [] ).map( function ( x ) {
      var action =
        x.action === 'download' ? '<a class="iroom__pill" href="/api/investor-room/doc?id=' + encodeURIComponent( x.id ) + '" data-doc="' + esc( x.id ) + '">' + ico( 'download', 15 ) + 'Download</a>' :
        x.action === 'watch' ? '<button class="iroom__pill" type="button" data-watch="' + esc( x.video ) + '">' + ico( 'eye', 15 ) + 'Watch</button>' :
        '<button class="iroom__pill" type="button" data-request="' + esc( x.title ) + '">' + ico( 'message', 15 ) + 'Request</button>';
      return '<div class="iroom__doc"><span class="iroom__docicon">' + ico( x.icon ) + '</span>' +
        '<span class="iroom__doctext"><b>' + esc( x.title ) + '</b><small>' + esc( x.detail ) + '</small></span>' + action + '</div>';
    } ).join( '' );
    return '<section class="iroom__sec" data-section="documents"><div class="iroom__docgrid">' +
      '<div><span class="iroom__kicker">Documents</span><h2 class="h2 h2--sm">For your diligence</h2>' +
        '<div class="iroom__docs">' + docs + '</div></div>' +
      '<aside class="iroom__side">' + ask( d ) + interest( d ) + '</aside>' +
      '</div></section>';
  }

  function ask( d ) {
    return '<form class="iroom__ask" id="room-ask"><h3>Ask a question</h3>' +
      '<textarea name="body" rows="4" maxlength="4000" placeholder="What would you like to know?" aria-label="Your question" required></textarea>' +
      '<button class="iroom__btn iroom__btn--dark" type="submit">Send</button>' +
      '<p class="iroom__small" id="room-ask-status" role="status">Answers are posted here within one business day.</p>' +
      history( d.questions ) + '</form>';
  }

  function history( q ) {
    if ( !q || !q.length ) return '<div id="room-history"></div>';
    return '<div id="room-history"><button class="iroom__link" type="button" data-history aria-expanded="false">Earlier questions: ' + q.length + '</button>' +
      '<ol class="iroom__qs" hidden>' + q.map( function ( x ) {
        return '<li><p><b>You:</b> ' + esc( x.body ) + '</p>' + ( x.answer ? '<p><b>Answer:</b> ' + esc( x.answer ) + '</p>' : '<p class="iroom__small">Awaiting an answer</p>' ) + '</li>';
      } ).join( '' ) + '</ol></div>';
  }

  function interest( d ) {
    var has = d.interest != null;
    return '<form class="iroom__interest" id="room-interest"><h3>Interested?</h3>' +
      '<p>Tell us the amount you’re considering. It’s not a commitment; it helps us plan the round.</p>' +
      '<label class="iroom__amount"><span>$</span><input name="amount" inputmode="numeric" placeholder="50,000" aria-label="Amount you’re considering" value="' +
      ( has ? esc( Number( d.interest ).toLocaleString( 'en-US' ) ) : '' ) + '" required></label>' +
      '<button class="iroom__btn iroom__btn--accent" type="submit">' + ( has ? 'Update interest' : 'Indicate interest' ) + '</button>' +
      '<p class="iroom__small" id="room-interest-status" role="status">' + ( has ? 'You’ve indicated ' + money( d.interest ) + '. You can change it any time.' : '' ) + '</p></form>';
  }

  function footer( d ) {
    return '<footer class="iroom__foot"><span>Confidential. Shared with ' + esc( d.investor.name ) +
      ' under the investor room terms. Not an offer to sell securities.</span><span>Taliferro Tech, LLC · Seattle, WA</span></footer>';
  }

  /* ------------------------------------------------------------ behaviour */
  function wire() {
    app.querySelector( '[data-signout]' ).addEventListener( 'click', function () {
      api( 'signout', {} ).then( function () { location.reload(); } );
    } );

    // Video: poster + play button first, native controls once playing.
    var player = app.querySelector( '.iroom__player' );
    if ( player ) {
      var vid = player.querySelector( 'video' );
      var marks = {};
      var start = function () { vid.controls = true; player.classList.add( 'is-playing' ); vid.play(); };
      player.querySelector( '.iroom__play' ).addEventListener( 'click', start );
      vid.addEventListener( 'play', function () { track( 'video_play', player.getAttribute( 'data-video' ) ); } );
      vid.addEventListener( 'timeupdate', function () {
        if ( !vid.duration ) return;
        var id = player.getAttribute( 'data-video' );
        var pct = vid.currentTime / vid.duration * 100;
        [ 25, 50, 75, 100 ].forEach( function ( m ) {
          if ( pct >= ( m === 100 ? 99 : m ) && !marks[ id + m ] ) { marks[ id + m ] = 1; track( 'video_progress', id, m ); }
        } );
      } );
      var pick = function ( id, autoplay ) {
        var v = data.videos.filter( function ( x ) { return x.id === id; } )[ 0 ];
        if ( !v ) return;
        player.setAttribute( 'data-video', v.id );
        vid.src = v.url;
        player.querySelector( '.iroom__presenter' ).textContent = v.presenter + ' · ' + v.length;
        app.querySelectorAll( '[data-pick]' ).forEach( function ( b ) { b.classList.toggle( 'is-on', b.getAttribute( 'data-pick' ) === id ); } );
        if ( autoplay ) start();
      };
      app.querySelectorAll( '[data-pick]' ).forEach( function ( b ) {
        b.addEventListener( 'click', function () { pick( b.getAttribute( 'data-pick' ), true ); } );
      } );
      app.querySelectorAll( '[data-watch]' ).forEach( function ( b ) {
        b.addEventListener( 'click', function () {
          pick( b.getAttribute( 'data-watch' ), true );
          document.getElementById( 'room-video' ).scrollIntoView( { behavior: 'smooth' } );
        } );
      } );
    }

    // Deck: arrows, thumbnails, keys, full screen, swipe; each slide logged once.
    var stage = app.querySelector( '.iroom__stage' );
    if ( stage ) {
      var slides = data.deck.slides, cur = 0, seenSlides = {};
      var img = stage.querySelector( '.iroom__slide' );
      var dots = app.querySelector( '.iroom__dots' );
      var go = function ( i ) {
        cur = ( i + slides.length ) % slides.length;
        img.src = slides[ cur ].url;
        img.alt = 'Slide ' + ( cur + 1 ) + ': ' + slides[ cur ].title;
        dots.textContent = ( cur + 1 ) + ' / ' + slides.length + ' · ' + slides[ cur ].title;
        app.querySelectorAll( '.iroom__thumb' ).forEach( function ( t, j ) {
          t.classList.toggle( 'is-on', j === cur );
          if ( j === cur && t.scrollIntoView && document.activeElement && document.activeElement.closest && document.activeElement.closest( '.iroom__thumbs' ) ) t.scrollIntoView( { block: 'nearest', inline: 'nearest' } );
        } );
        if ( !seenSlides[ cur ] ) { seenSlides[ cur ] = 1; track( 'slide', String( cur + 1 ), cur + 1 ); }
      };
      app.querySelectorAll( '[data-step]' ).forEach( function ( b ) {
        b.addEventListener( 'click', function () { go( cur + Number( b.getAttribute( 'data-step' ) ) ); } );
      } );
      app.querySelectorAll( '[data-slide]' ).forEach( function ( b ) {
        b.addEventListener( 'click', function () { go( Number( b.getAttribute( 'data-slide' ) ) ); } );
      } );
      stage.addEventListener( 'keydown', function ( e ) {
        if ( e.key === 'ArrowRight' ) { e.preventDefault(); go( cur + 1 ); }
        if ( e.key === 'ArrowLeft' ) { e.preventDefault(); go( cur - 1 ); }
      } );
      document.addEventListener( 'keydown', function ( e ) {
        if ( document.fullscreenElement !== stage ) return;
        if ( e.key === 'ArrowRight' ) go( cur + 1 );
        if ( e.key === 'ArrowLeft' ) go( cur - 1 );
      } );
      var x0 = null;
      stage.addEventListener( 'touchstart', function ( e ) { x0 = e.touches[ 0 ].clientX; }, { passive: true } );
      stage.addEventListener( 'touchend', function ( e ) {
        if ( x0 == null ) return;
        var dx = e.changedTouches[ 0 ].clientX - x0;
        if ( Math.abs( dx ) > 40 ) go( cur + ( dx < 0 ? 1 : -1 ) );
        x0 = null;
      } );
      var fs = app.querySelector( '[data-fullscreen]' );
      if ( !stage.requestFullscreen ) fs.hidden = true;
      fs.addEventListener( 'click', function () { stage.requestFullscreen(); stage.focus(); } );
      dots.textContent = '1 / ' + slides.length + ' · ' + slides[ 0 ].title;
      img.alt = 'Slide 1: ' + slides[ 0 ].title;
    }

    // Request a document: prefill the question box.
    var askForm = document.getElementById( 'room-ask' );
    app.querySelectorAll( '[data-request]' ).forEach( function ( b ) {
      b.addEventListener( 'click', function () {
        askForm.elements.body.value = 'Could you share the ' + b.getAttribute( 'data-request' ).toLowerCase() + '?';
        askForm.elements.body.focus();
      } );
    } );

    var wireHistory = function () {
      var t = app.querySelector( '[data-history]' );
      if ( !t ) return;
      t.addEventListener( 'click', function () {
        var list = t.nextElementSibling;
        list.hidden = !list.hidden;
        t.setAttribute( 'aria-expanded', String( !list.hidden ) );
      } );
    };
    wireHistory();

    askForm.addEventListener( 'submit', function ( e ) {
      e.preventDefault();
      var body = askForm.elements.body.value.trim();
      var note = document.getElementById( 'room-ask-status' );
      if ( !body ) return;
      var btn = askForm.querySelector( 'button[type=submit]' );
      btn.disabled = true;
      api( 'question', { body: body } ).then( function ( res ) {
        if ( !res.ok ) throw res.status;
        return res.json();
      } ).then( function ( j ) {
        askForm.elements.body.value = '';
        note.textContent = 'Sent. ' + data.contact.name + ' will answer here within one business day.';
        document.getElementById( 'room-history' ).outerHTML = history( j.questions );
        wireHistory();
      } ).catch( function () {
        note.textContent = 'That didn’t send. Try again, or email ' + data.contact.email + '.';
      } ).then( function () { btn.disabled = false; } );
    } );

    var intForm = document.getElementById( 'room-interest' );
    intForm.addEventListener( 'submit', function ( e ) {
      e.preventDefault();
      var amount = Number( intForm.elements.amount.value.replace( /[^0-9.]/g, '' ) );
      var note = document.getElementById( 'room-interest-status' );
      if ( !amount ) { note.textContent = 'Enter an amount in dollars.'; return; }
      var btn = intForm.querySelector( 'button[type=submit]' );
      btn.disabled = true;
      api( 'interest', { amount: amount } ).then( function ( res ) {
        if ( !res.ok ) throw res.status;
        return res.json();
      } ).then( function ( j ) {
        intForm.elements.amount.value = j.amount.toLocaleString( 'en-US' );
        note.textContent = 'Thanks. ' + j.contact + ' will be in touch.';
        btn.textContent = 'Update interest';
      } ).catch( function () {
        note.textContent = 'That didn’t save. Try again.';
      } ).then( function () { btn.disabled = false; } );
    } );

    // View log: each section once per visit.
    if ( 'IntersectionObserver' in window ) {
      var seen = {};
      var io = new IntersectionObserver( function ( entries ) {
        entries.forEach( function ( en ) {
          var s = en.target.getAttribute( 'data-section' );
          if ( en.isIntersecting && !seen[ s ] ) { seen[ s ] = 1; track( 'section', s ); io.unobserve( en.target ); }
        } );
      }, { threshold: 0.35 } );
      app.querySelectorAll( '[data-section]' ).forEach( function ( el ) { io.observe( el ); } );
    }
  }

  /* ------------------------------------------------------------ start */
  openRoom();
} )();
