(self.webpackChunkmitosheet3=self.webpackChunkmitosheet3||[]).push([[7],{2007:(e,n,l)=>{"use strict";l.r(n),l.d(n,{default:()=>f});var r={fullscreenEnabled:0,fullscreenElement:1,requestFullscreen:2,exitFullscreen:3,fullscreenchange:4,fullscreenerror:5,fullscreen:6},u=["webkitFullscreenEnabled","webkitFullscreenElement","webkitRequestFullscreen","webkitExitFullscreen","webkitfullscreenchange","webkitfullscreenerror","-webkit-full-screen"],s=["mozFullScreenEnabled","mozFullScreenElement","mozRequestFullScreen","mozCancelFullScreen","mozfullscreenchange","mozfullscreenerror","-moz-full-screen"],t=["msFullscreenEnabled","msFullscreenElement","msRequestFullscreen","msExitFullscreen","MSFullscreenChange","MSFullscreenError","-ms-fullscreen"],c="undefined"!=typeof window&&void 0!==window.document?window.document:{},o="fullscreenEnabled"in c&&Object.keys(r)||u[0]in c&&u||s[0]in c&&s||t[0]in c&&t||[];const f={requestFullscreen:function(e){return e[o[r.requestFullscreen]]()},requestFullscreenFunction:function(e){return e[o[r.requestFullscreen]]},get exitFullscreen(){return c[o[r.exitFullscreen]].bind(c)},get fullscreenPseudoClass(){return":"+o[r.fullscreen]},addEventListener:function(e,n,l){return c.addEventListener(o[r[e]],n,l)},removeEventListener:function(e,n,l){return c.removeEventListener(o[r[e]],n,l)},get fullscreenEnabled(){return Boolean(c[o[r.fullscreenEnabled]])},set fullscreenEnabled(e){},get fullscreenElement(){return c[o[r.fullscreenElement]]},set fullscreenElement(e){},get onfullscreenchange(){return c[("on"+o[r.fullscreenchange]).toLowerCase()]},set onfullscreenchange(e){return c[("on"+o[r.fullscreenchange]).toLowerCase()]=e},get onfullscreenerror(){return c[("on"+o[r.fullscreenerror]).toLowerCase()]},set onfullscreenerror(e){return c[("on"+o[r.fullscreenerror]).toLowerCase()]=e}}}}]);