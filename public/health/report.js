/* Weekly product health report: unlocks /health/data.enc with the password,
   then renders it. Every number and the summary paragraph come from the data
   that src/health_pull.py writes. Layout follows the Claude Design handoff
   (corporate/design_handoff_product_health).

   URL options: ?sort=engaged|change|name, ?low=0 hides low-traffic products
   (the investor version). */
( function () {
  'use strict';

  var DATA_URL = '/health/data.enc';
  var ITER = 210000; // must match PBKDF2_ITER in src/health_pull.py
  var root = document.documentElement;
  var qs = new URLSearchParams( location.search );
  var sortBy = qs.get( 'sort' ) || 'engaged';
  var showLow = qs.get( 'low' ) !== '0';
  var data = null;
  var openRow = null;

  // ------------------------------------------------------------ unlock

  /* data.enc is `openssl enc -aes-256-cbc -pbkdf2 -md sha256 -salt` output:
     "Salted__" + 8-byte salt + ciphertext. PBKDF2 gives 48 bytes: key then IV. */
  async function unlock ( password ) {
    var res = await fetch( DATA_URL, { cache: 'no-store' } );
    if ( !res.ok ) throw new Error( 'No report has been published yet.' );
    var buf = new Uint8Array( await res.arrayBuffer() );
    if ( new TextDecoder().decode( buf.slice( 0, 8 ) ) !== 'Salted__' ) throw new Error( 'The report file is damaged.' );
    var base = await crypto.subtle.importKey( 'raw', new TextEncoder().encode( password ), 'PBKDF2', false, [ 'deriveBits' ] );
    var bits = new Uint8Array( await crypto.subtle.deriveBits(
      { name: 'PBKDF2', hash: 'SHA-256', salt: buf.slice( 8, 16 ), iterations: ITER }, base, 384 ) );
    var key = await crypto.subtle.importKey( 'raw', bits.slice( 0, 32 ), 'AES-CBC', false, [ 'decrypt' ] );
    try {
      var plain = await crypto.subtle.decrypt( { name: 'AES-CBC', iv: bits.slice( 32, 48 ) }, key, buf.slice( 16 ) );
      return JSON.parse( new TextDecoder().decode( plain ) );
    } catch ( e ) {
      throw new Error( 'That password didn’t work.' );
    }
  }

  // ------------------------------------------------------------ theme

  var ICON = {
    moon: '<path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/>',
    sun: '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/>',
    chev: '<path d="m6 9 6 6 6-6"/>'
  };
  function icon ( k, cls ) {
    var svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="black" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">' + ICON[ k ] + '</svg>';
    return '<span class="ic ' + ( cls || '' ) + '" style="--i:url(&quot;data:image/svg+xml,' + encodeURIComponent( svg ) + '&quot;)" aria-hidden="true"></span>';
  }
  var darkQuery = window.matchMedia ? window.matchMedia( '(prefers-color-scheme: dark)' ) : null;
  function isDark () {
    var t = root.dataset.theme;
    return t === 'dark' || ( t !== 'light' && !!( darkQuery && darkQuery.matches ) );
  }
  function paintTheme () {
    var btn = document.getElementById( 'theme' );
    var dark = isDark();
    btn.innerHTML = icon( dark ? 'sun' : 'moon' ) + ( dark ? 'Light' : 'Dark' );
    btn.setAttribute( 'aria-label', 'Switch to ' + ( dark ? 'light' : 'dark' ) + ' mode' );
  }
  document.getElementById( 'theme' ).addEventListener( 'click', function () {
    var next = isDark() ? 'light' : 'dark';
    root.dataset.theme = next;
    try { localStorage.setItem( 'theme', next ); } catch ( e ) { /* optional */ }
    paintTheme();
  } );
  if ( darkQuery && darkQuery.addEventListener ) darkQuery.addEventListener( 'change', paintTheme );
  paintTheme();

  // ------------------------------------------------------------ formatting

  var STATUS = { green: [ 'Growing', 'green' ], yellow: [ 'Slipping', 'yellow' ], red: [ 'Down', 'pink' ],
    low: [ 'Low traffic', 'grey' ], new: [ 'New', 'blue' ], none: [ 'No data', 'grey' ] };
  var ICONS = { 'ask-todd': 'png', docs: 'png', 'email-creator': 'svg', 'email-signature': 'png', find: 'svg',
    'image-creator': 'svg', 'lead-vault': 'png', maya: 'png', moves: 'png', music: 'png', network: 'png',
    outreach: 'png', pulse: 'png', sayit: 'png', social: 'png' };

  function esc ( s ) {
    return String( s == null ? '' : s ).replace( /[&<>"']/g, function ( c ) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[ c ];
    } );
  }
  function n ( v ) { return v == null ? '—' : Number( v ).toLocaleString( 'en-US' ); }
  function pct ( c ) {
    if ( c == null ) return '—';
    return ( c > 0 ? '+' : c < 0 ? '−' : '' ) + Math.abs( Math.round( c * 1000 ) / 10 ).toLocaleString( 'en-US' ) + '%';
  }
  function bare ( c ) { return pct( Math.abs( c || 0 ) ).replace( '+', '' ); }
  function dir ( c ) { return c == null || c === 0 ? 'flat' : c > 0 ? 'up' : 'down'; }
  function fmtD ( s, o ) { return new Date( s + 'T00:00:00Z' ).toLocaleDateString( 'en-US', Object.assign( { timeZone: 'UTC' }, o ) ); }
  function range ( w ) {
    var sameMonth = w.start.slice( 0, 7 ) === w.end.slice( 0, 7 );
    return fmtD( w.start, { month: 'short', day: 'numeric' } ) + ' – ' +
      fmtD( w.end, sameMonth ? { day: 'numeric' } : { month: 'short', day: 'numeric' } ) + ', ' + w.end.slice( 0, 4 );
  }
  function slug ( name ) { return name.toLowerCase().replace( /\s+/g, '-' ); }
  function imgFor ( name ) {
    var s = slug( name );
    if ( ICONS[ s ] ) return '/img/products/' + s + '.' + ICONS[ s ];
    return name === 'Taliferro Tech' ? '/img/general/apple-touch-icon.png' : null;
  }
  // Black line-art icons always sit on a white tile so they read in dark mode.
  function productIcon ( name, size ) {
    var src = imgFor( name );
    var r = Math.round( size * 0.28 ), pad = size >= 48 ? 6 : 5;
    if ( src ) return '<img class="icon" src="' + src + '" alt="" width="' + size + '" height="' + size + '" style="border-radius:' + r + 'px;padding:' + pad + 'px">';
    return '<span class="letter" style="width:' + size + 'px;height:' + size + 'px;border-radius:' + Math.round( size * 0.3 ) +
      'px;font-size:' + Math.round( size * 0.42 ) + 'px" aria-hidden="true">' + esc( name[ 0 ] ) + '</span>';
  }
  function pill ( st ) { var s = STATUS[ st ] || [ st, 'grey' ]; return '<span class="pill t-' + s[ 1 ] + '">' + esc( s[ 0 ] ) + '</span>'; }

  // ------------------------------------------------------------ render

  function summaryText ( D ) {
    var props = D.properties, es = D.totals.engaged_sessions;
    var s = 'Engaged sessions ' + ( ( es.change || 0 ) >= 0 ? 'rose' : 'fell' ) + ' ' + bare( es.change ) + ' to ' + n( es.this ) +
      ', from ' + n( es.prev ) + ' the week before.';
    var gainers = props.map( function ( p ) { return { p: p, d: p.engaged_sessions.this - p.engaged_sessions.prev }; } )
      .filter( function ( x ) { return x.d > 0; } ).sort( function ( a, b ) { return b.d - a.d; } ).slice( 0, 2 );
    if ( gainers.length ) {
      s += ' ' + gainers.map( function ( g ) { return g.p.name; } ).join( ' and ' ) + ' added the most (' +
        gainers.map( function ( g ) { return '+' + g.d; } ).join( ', ' ) + ').';
    }
    var hurt = props.filter( function ( p ) { return p.status === 'red' || p.status === 'yellow'; } );
    if ( hurt.length ) {
      s += ' ' + hurt.map( function ( p ) {
        return p.name + ' ' + ( p.engaged_sessions.change < 0 ? 'fell' : 'moved' ) + ' ' + bare( p.engaged_sessions.change );
      } ).join( '; ' ) + '.';
    }
    var fresh = props.filter( function ( p ) { return p.status === 'new'; } );
    if ( fresh.length ) {
      s += ' Tracking began on ' + fresh.length + ' more product' + ( fresh.length === 1 ? '' : 's' ) + ' on ' +
        fmtD( fresh[ 0 ].tracking_since || D.week.end, { month: 'short', day: 'numeric' } ) + '.';
    }
    return s;
  }

  function rowHtml ( p ) {
    var open = openRow === p.name, w = p.web || {}, ch = p.engaged_sessions.change, st = p.status;
    var change = st === 'new' ? 'New' : ch == null ? ( p.engaged_sessions.this > 0 ? 'First week' : '—' ) : pct( ch );
    var html = '<div class="row' + ( open ? ' open' : '' ) + '">' +
      '<button type="button" class="cols" data-row="' + esc( p.name ) + '" aria-expanded="' + open + '">' +
      '<span class="prod">' + productIcon( p.name, 40 ) + '<span class="nm"><b>' + esc( p.name ) + '</b><span>' + esc( p.host ) + '</span></span></span>' +
      '<span>' + pill( st ) + '</span>' +
      '<span class="eng"><b>' + n( p.engaged_sessions.this ) + '</b><span>from ' + n( p.engaged_sessions.prev ) + '</span></span>' +
      '<span class="change ' + dir( st === 'new' ? null : ch ) + '">' + change + '</span>' +
      '<span class="val">' + ( w.engagement_rate == null ? '—' : Math.round( w.engagement_rate * 100 ) + '%' ) + '</span>' +
      '<span class="val">' + ( w.engaged_sec_per_session ? w.engaged_sec_per_session + 's' : '—' ) + '</span>' +
      icon( 'chev', 'chev' ) + '</button>';
    if ( open ) {
      var metric = function ( k, m ) {
        m = m || {};
        return '<div class="metric"><span class="k">' + k + '</span><span class="v"><b>' + n( m.this ) + '</b>' +
          ( m.change != null ? '<span class="' + dir( m.change ) + '">' + pct( m.change ) + '</span>' : '' ) +
          '</span><span class="p">from ' + n( m.prev ) + '</span></div>';
      };
      var events = Object.keys( p.events || {} ).map( function ( k ) {
        var v = p.events[ k ];
        return '<span><b>' + esc( k.replace( /_/g, ' ' ) ) + '</b><em>' + n( v.this ) + ' this week · ' + n( v.prev ) + ' before</em></span>';
      } ).join( '' );
      html += '<div class="detail"><div class="metrics">' + metric( 'Sessions', w.sessions ) + metric( 'Views', w.views ) +
        metric( 'Users (incl. bots)', w.users_incl_bots ) + '</div>' +
        ( events ? '<div class="chips">' + events + '</div>' : '' ) +
        ( p.notes || [] ).map( function ( t ) { return '<span class="note">' + esc( t ) + '</span>'; } ).join( '' ) +
        '<a class="open-link" href="' + esc( p.url ) + '" target="_blank" rel="noopener">Open ' + esc( p.host ) + '</a></div>';
    }
    return html + '</div>';
  }

  function render () {
    var D = data, props = D.properties || [], T = D.totals || {}, es = T.engaged_sessions || {}, bs = T.by_status || {}, th = D.thresholds || {};

    var statusTiles = [ 'green', 'yellow', 'red', 'low', 'new' ].filter( function ( k ) { return bs[ k ] || k === 'red'; } ).map( function ( k ) {
      return '<div class="tile t-' + STATUS[ k ][ 1 ] + '"><b>' + ( bs[ k ] || 0 ) + '</b><span>' + STATUS[ k ][ 0 ] + '</span></div>';
    } ).join( '' );

    var ranked = props.filter( function ( p ) { return p.engaged_sessions.this > 0; } )
      .sort( function ( a, b ) { return b.engaged_sessions.this - a.engaged_sessions.this; } );
    var parts = ranked.slice( 0, 3 ).map( function ( p ) { return [ p.name, p.engaged_sessions.this ]; } );
    var rest = ranked.slice( 3 );
    if ( rest.length ) parts.push( [ rest.length + ' others', rest.reduce( function ( s, p ) { return s + p.engaged_sessions.this; }, 0 ) ] );
    var colours = [ 'var(--blue)', 'var(--t-cyan-fg)', 'var(--t-violet-fg)', 'var(--muted)' ];
    var total = es.this || 1;
    var bar = parts.map( function ( x, i ) { return '<span style="flex:' + x[ 1 ] + ' 0 0;background:' + colours[ i ] + '"></span>'; } ).join( '' );
    var legend = parts.map( function ( x, i ) {
      return '<span><i style="background:' + colours[ i ] + '"></i><b>' + esc( x[ 0 ] ) + '</b><span>' +
        Math.round( x[ 1 ] / total * 100 ) + '% · ' + n( x[ 1 ] ) + '</span></span>';
    } ).join( '' );

    var hurt = props.filter( function ( p ) { return p.status === 'red' || p.status === 'yellow'; } );
    var attention = hurt.map( function ( p ) {
      return '<div class="t-pink">' + productIcon( p.name, 48 ) + '<span class="txt"><b>' + esc( p.name ) + '</b><span>' +
        n( p.engaged_sessions.this ) + ' engaged sessions, down from ' + n( p.engaged_sessions.prev ) + '</span></span>' +
        '<span class="pct">' + pct( p.engaged_sessions.change ) + '</span></div>';
    } ).join( '' );

    var order = [];
    props.forEach( function ( p ) { if ( order.indexOf( p.group ) < 0 ) order.push( p.group ); } );
    var sorter = {
      engaged: function ( a, b ) { return b.engaged_sessions.this - a.engaged_sessions.this; },
      change: function ( a, b ) { return ( b.engaged_sessions.change == null ? -9 : b.engaged_sessions.change ) - ( a.engaged_sessions.change == null ? -9 : a.engaged_sessions.change ); },
      name: function ( a, b ) { return a.name.localeCompare( b.name ); }
    }[ sortBy ] || function () { return 0; };
    var groups = order.map( function ( g ) {
      var rows = props.filter( function ( p ) { return p.group === g && ( showLow || p.status !== 'low' ); } ).sort( sorter );
      if ( !rows.length ) return '';
      return '<div class="group"><span class="kicker">' + esc( g ) + '</span><div class="scroll"><div class="table">' +
        '<div class="cols th"><span>Product</span><span>Status</span><span class="r">Engaged</span><span class="r">Change</span>' +
        '<span class="r">Engagement rate</span><span class="r">Engaged time</span><span></span></div>' +
        rows.map( rowHtml ).join( '' ) + '</div></div></div>';
    } ).join( '' );

    var apps = props.filter( function ( p ) { return p.app_store; } ).map( function ( p ) {
      var a = p.app_store, dl = a.downloads || {}, t = dl.this || {}, pr = dl.prev || {};
      var tiles = [ [ 'Downloads', 'downloads' ], [ 'Redownloads', 'redownloads' ], [ 'Updates', 'updates' ] ].map( function ( x ) {
        return '<div class="dl"><span class="k">' + x[ 0 ] + '</span><b>' + n( t[ x[ 1 ] ] ) + '</b><span>' + n( pr[ x[ 1 ] ] ) + ' the week before</span></div>';
      } ).join( '' );
      return '<div class="app"><span class="top">' + productIcon( p.name, 52 ) + '<span class="nm"><b>' + esc( a.name || p.name ) + '</b><span>Version ' +
        esc( a.version ) + ' · ' + ( a.rating_count ? esc( a.rating ) + ' ★ (' + n( a.rating_count ) + ')' : 'No ratings yet' ) + '</span></span>' +
        ( a.url ? '<a href="' + esc( a.url ) + '" target="_blank" rel="noopener">App Store</a>' : '' ) + '</span>' +
        '<div class="dls">' + tiles + '</div></div>';
    } ).join( '' );
    var appsOk = D.app_store_status === 'ok';

    document.title = 'Product health · ' + range( D.week ) + ' · Taliferro Tech';
    document.getElementById( 'report' ).innerHTML =
      '<div class="title"><span class="kicker">Weekly product health</span><div class="week">' + range( D.week ) + '</div>' +
      '<div class="summary">' + esc( summaryText( D ) ) + '</div>' +
      '<div class="meta">Compared with ' + range( D.prev_week ) + ' · Generated ' +
      new Date( D.generated_at ).toLocaleString( 'en-US', { month: 'short', day: 'numeric', hour: 'numeric', minute: '2-digit' } ) + '</div></div>' +

      '<div class="kpis"><div class="total"><span class="kicker">Engaged sessions, all products</span><span class="big"><span class="num">' + n( es.this ) +
      '</span><span class="chg t-' + ( ( es.change || 0 ) >= 0 ? 'green' : 'pink' ) + '">' + pct( es.change ) + '</span></span>' +
      '<span class="prev">' + n( es.prev ) + ' the week before</span></div>' +
      '<div class="status"><span class="kicker">' + props.length + ' products by status</span><div class="tiles">' + statusTiles + '</div></div></div>' +

      '<div class="sec"><span class="h2">Where engagement came from</span><div class="bar" role="img" aria-label="Share of engaged sessions by product">' + bar +
      '</div><div class="legend">' + legend + '</div></div>' +

      ( attention ? '<div class="sec"><span class="h2">Needs attention</span><div class="attn">' + attention + '</div></div>' : '' ) +

      '<div class="prods"><div class="prods-head"><span class="h2">Every product</span><span class="meta">Select a row for sessions, views and users.</span></div>' +
      groups + '</div>' +

      ( apps ? '<div class="sec"><span class="apps-head"><span class="h2">App Store</span><span class="pill t-' + ( appsOk ? 'green' : 'pink' ) + '">' +
        ( appsOk ? 'Data current' : 'Data unavailable' ) + '</span></span><div class="apps">' + apps + '</div></div>' : '' ) +

      '<div class="how"><b>How status is set</b><span>An engaged session is a visit that lasts longer than a bounce. A product shows Low traffic below ' +
      n( th.min_engaged_sessions == null ? 10 : th.min_engaged_sessions ) + ' engaged sessions a week, since percentage changes on very small numbers swing widely. ' +
      'Above that, a drop of more than ' + Math.round( Math.abs( th.yellow_below == null ? 0.05 : th.yellow_below ) * 100 ) + '% shows Slipping and a drop of more than ' +
      Math.round( Math.abs( th.red_below == null ? 0.2 : th.red_below ) * 100 ) + '% shows Down. New means tracking started during the week, so there is no full week to compare. ' +
      'User counts include bots.</span></div>';
  }

  document.getElementById( 'report' ).addEventListener( 'click', function ( e ) {
    var btn = e.target.closest( '[data-row]' );
    if ( !btn ) return;
    var name = btn.getAttribute( 'data-row' );
    openRow = openRow === name ? null : name;
    render();
    var again = document.querySelector( '[data-row="' + CSS.escape( name ) + '"]' );
    if ( again ) again.focus();
  } );

  // ------------------------------------------------------------ gate

  var gate = document.getElementById( 'gate' );
  var msg = document.getElementById( 'msg' );

  async function open ( password, quiet ) {
    msg.classList.remove( 'err' );
    msg.textContent = quiet ? '' : 'Opening…';
    try {
      data = await unlock( password );
      try { sessionStorage.setItem( 'health-pw', password ); } catch ( e ) { /* optional */ }
      msg.textContent = '';
      gate.hidden = true;
      render();
      document.getElementById( 'report' ).hidden = false;
    } catch ( e ) {
      try { sessionStorage.removeItem( 'health-pw' ); } catch ( x ) { /* optional */ }
      if ( !quiet ) { msg.classList.add( 'err' ); msg.textContent = e.message; }
    }
  }

  gate.addEventListener( 'submit', function ( e ) {
    e.preventDefault();
    open( document.getElementById( 'pw' ).value, false );
  } );
  try { var saved = sessionStorage.getItem( 'health-pw' ); if ( saved ) open( saved, true ); } catch ( e ) { /* optional */ }
} )();
