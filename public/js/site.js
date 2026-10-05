/* taliferro.tech: theme toggle, universal menu, menu search. */
( function () {
  var root = document.documentElement;
  var dark = window.matchMedia ? window.matchMedia( '(prefers-color-scheme: dark)' ) : null;

  function currentTheme () {
    var set = root.dataset.theme;
    if ( set === 'light' || set === 'dark' ) return set;
    return dark && dark.matches ? 'dark' : 'light';
  }

  // The pill names the theme you'd switch to, as in the design ("Dark" in light mode).
  function paintToggles () {
    var mode = currentTheme();
    document.querySelectorAll( '.theme-toggle' ).forEach( function ( btn ) {
      btn.dataset.mode = mode;
      var label = mode === 'dark' ? 'Light' : 'Dark';
      btn.querySelector( '.theme-toggle__label' ).textContent = label;
      btn.setAttribute( 'aria-label', 'Switch to ' + label.toLowerCase() + ' mode' );
    } );
  }

  document.addEventListener( 'click', function ( e ) {
    if ( !e.target.closest( '.theme-toggle' ) ) return;
    var next = currentTheme() === 'dark' ? 'light' : 'dark';
    root.dataset.theme = next;
    try { localStorage.setItem( 'theme', next ); } catch ( err ) { /* storage optional */ }
    paintToggles();
  } );
  if ( dark && dark.addEventListener ) dark.addEventListener( 'change', paintToggles );
  paintToggles();

  // GA4 key events: contact (mail, phone, /contact), app_store_click, and
  // get_started (any link out to a product or TODD on *.taliferro.tech).
  document.addEventListener( 'click', function ( e ) {
    var a = e.target.closest && e.target.closest( 'a[href]' );
    if ( !a || typeof gtag !== 'function' ) return;
    var params = { link_url: a.href, link_text: ( a.textContent || '' ).trim().slice( 0, 80 ) };
    var name = null;
    if ( /(^|\.)apps\.apple\.com$/.test( a.hostname ) ) {
      name = 'app_store_click';
    } else if ( a.protocol === 'mailto:' || a.protocol === 'tel:' ) {
      name = 'contact'; params.method = a.protocol.slice( 0, -1 );
    } else if ( a.host === location.host && a.pathname.replace( /\.html$/, '' ) === '/contact' ) {
      name = 'contact'; params.method = 'page';
    } else if ( a.host !== location.host && /\.taliferro\.tech$/.test( a.hostname ) ) {
      name = 'get_started'; params.product = a.hostname.split( '.' )[0];
    }
    if ( name ) gtag( 'event', name, params );
  } );

  // Universal menu
  var menu = document.getElementById( 'menu' );
  if ( !menu ) return;
  var search = menu.querySelector( 'input[type="search"]' );
  var empty = menu.querySelector( '.menu__empty' );
  var opener = null;

  function openMenu ( focusSearch ) {
    opener = document.activeElement;
    menu.hidden = false;
    document.body.classList.add( 'menu-is-open' );
    ( focusSearch ? search : menu.querySelector( '.menu-close' ) ).focus();
  }

  function closeMenu () {
    menu.hidden = true;
    document.body.classList.remove( 'menu-is-open' );
    search.value = '';
    filter( '' );
    if ( opener && opener.focus ) opener.focus();
  }

  function filter ( q ) {
    q = q.trim().toLowerCase();
    var shown = 0;
    menu.querySelectorAll( '.mgrid [data-search]' ).forEach( function ( el ) {
      var hit = !q || el.dataset.search.indexOf( q ) !== -1;
      el.classList.toggle( 'is-hidden', !hit );
      if ( hit ) shown++;
    } );
    menu.querySelectorAll( '.menu__site [data-search]' ).forEach( function ( el ) {
      el.classList.toggle( 'is-hidden', !!q && el.dataset.search.indexOf( q ) === -1 );
    } );
    empty.hidden = shown > 0;
  }

  document.querySelectorAll( '.menu-open' ).forEach( function ( b ) {
    b.addEventListener( 'click', function () { openMenu( false ); } );
  } );
  menu.querySelector( '.menu-close' ).addEventListener( 'click', closeMenu );
  search.addEventListener( 'input', function () { filter( search.value ); } );
  search.addEventListener( 'keydown', function ( e ) {
    if ( e.key !== 'Enter' ) return;
    var first = menu.querySelector( 'a[data-search]:not(.is-hidden)' );
    if ( first ) first.click();
  } );

  document.addEventListener( 'keydown', function ( e ) {
    if ( ( e.metaKey || e.ctrlKey ) && e.key.toLowerCase() === 'k' ) {
      e.preventDefault();
      if ( menu.hidden ) openMenu( true ); else search.focus();
      return;
    }
    if ( menu.hidden ) return;
    if ( e.key === 'Escape' ) { closeMenu(); return; }
    if ( e.key === 'Tab' ) {
      // Keep focus inside the open menu.
      var items = Array.prototype.filter.call(
        menu.querySelectorAll( 'a[href], button, input' ),
        function ( el ) { return el.offsetParent !== null; }
      );
      var first = items[0], last = items[items.length - 1];
      if ( e.shiftKey && document.activeElement === first ) { e.preventDefault(); last.focus(); }
      else if ( !e.shiftKey && document.activeElement === last ) { e.preventDefault(); first.focus(); }
    }
  } );
} )();
