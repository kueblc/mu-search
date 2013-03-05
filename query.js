/* query.js
 * written by Colin Kuebler 2013 for CSCI 4961 Web Science
 * http://www.github.com/kueblc/mu-search
 * mu-search's frontend, sends queries to the server and displays the results
 */

/* AJAX request MSIE polyfill */
if( !window.XMLHttpRequest ){
	window.XMLHttpRequest = function(){
		return ActiveXObject('Microsoft.XMLHTTP');
	};
}

/* JSON parse polyfill */
if( !(window.JSON && window.JSON.parse) ){
	window.JSON = {
		parse: function( str ){
			// strict mode for safer eval (can't make globals)
			"use strict";
			var obj;
			try {
				eval( "obj = (" + str + ");" );
			} catch(e) {}
			return obj;
		}
	};
}

/* convenient method for synchronous requests */
function sjax( url, options ){
	// encode the parameters
	var s = [];
	for( var key in options )
		s.push( encodeURIComponent(key) +
			'=' + encodeURIComponent(options[key]) );
	if( s.length ) url += '?' + s.join('&');
	// send an HTTP request
	var r = new XMLHttpRequest();
	r.open( 'GET', url, false );
	r.send();
	// parse the response as JSON
	return JSON.parse( r.responseText );
}

/* shortcut to access an element by its ID */
function $(e){ return document.getElementById(e); };

/* emphasizes select words */
function highlight( str, focus ){
	var words = focus.match( /\w+/g );
	for( var i in words )
		str = str.replace( new RegExp( words[i], 'gi' ), "<b>$&</b>" );
	return str;
}

/* page initialization */
window.onload = function(){
	var page = 0;
	var query = $('query'),
		results = $('results');
	
	function submit(){
		document.body.className = 'show';
		results.innerHTML = '';
		var response = sjax( 'http://www.faroo.com/api', {
			'q': query.value,
			'start': page * 10 + 1,
			'length': 10 } );
		for( var i in response.results ){
			var result = response.results[i];
			results.innerHTML += "<li><a href='" + result.url + "'>" +
				highlight( result.title, query.value ) +
				"</a><span class='url'>" +
				highlight( result.url, query.value ) +
				"</span>" + highlight( result.kwic, query.value ) + "</li>";
		}
	}
	
	query.onkeypress = function(e){
		// detect return key
		var e = e || window.event;
		var key = e.which || e.keyCode || e.charCode;
		if( key === 13 ) submit();
	};
	
	$('submit').onclick = submit;
};
