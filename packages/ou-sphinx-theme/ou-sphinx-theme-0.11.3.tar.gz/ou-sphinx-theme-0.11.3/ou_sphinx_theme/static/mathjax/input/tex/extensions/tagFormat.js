!function(n){var e={};function a(t){if(e[t])return e[t].exports;var o=e[t]={i:t,l:!1,exports:{}};return n[t].call(o.exports,o,o.exports,a),o.l=!0,o.exports}a.m=n,a.c=e,a.d=function(t,o,n){a.o(t,o)||Object.defineProperty(t,o,{enumerable:!0,get:n})},a.r=function(t){"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(t,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(t,"__esModule",{value:!0})},a.t=function(o,t){if(1&t&&(o=a(o)),8&t)return o;if(4&t&&"object"==typeof o&&o&&o.__esModule)return o;var n=Object.create(null);if(a.r(n),Object.defineProperty(n,"default",{enumerable:!0,value:o}),2&t&&"string"!=typeof o)for(var e in o)a.d(n,e,function(t){return o[t]}.bind(null,e));return n},a.n=function(t){var o=t&&t.__esModule?function(){return t.default}:function(){return t};return a.d(o,"a",o),o},a.o=function(t,o){return Object.prototype.hasOwnProperty.call(t,o)},a.p="",a(a.s=4)}([function(t,o,n){"use strict";Object.defineProperty(o,"__esModule",{value:!0}),o.isObject=MathJax._.components.global.isObject,o.combineConfig=MathJax._.components.global.combineConfig,o.combineDefaults=MathJax._.components.global.combineDefaults,o.combineWithMathJax=MathJax._.components.global.combineWithMathJax,o.MathJax=MathJax._.components.global.MathJax},function(t,o,n){"use strict";var e,s=this&&this.__extends||(e=function(t,o){return(e=Object.setPrototypeOf||{__proto__:[]}instanceof Array&&function(t,o){t.__proto__=o}||function(t,o){for(var n in o)o.hasOwnProperty(n)&&(t[n]=o[n])})(t,o)},function(t,o){function n(){this.constructor=t}e(t,o),t.prototype=null===o?Object.create(o):(n.prototype=o.prototype,new n)});Object.defineProperty(o,"__esModule",{value:!0});var a=n(2),c=n(3),p=0;function r(t,n){var o=n.parseOptions.options.tags;"base"!==o&&t.tags.hasOwnProperty(o)&&c.TagsFactory.add(o,t.tags[o]);var e,a=c.TagsFactory.create(n.parseOptions.options.tags).constructor,r=(s(i,e=a),i.prototype.formatNumber=function(t){return n.parseOptions.options.tagFormat.number(t)},i.prototype.formatTag=function(t){return n.parseOptions.options.tagFormat.tag(t)},i.prototype.formatId=function(t){return n.parseOptions.options.tagFormat.id(t)},i.prototype.formatUrl=function(t,o){return n.parseOptions.options.tagFormat.url(t,o)},i);function i(){return null!==e&&e.apply(this,arguments)||this}var u="configTags-"+ ++p;c.TagsFactory.add(u,r),n.parseOptions.options.tags=u}o.tagFormatConfig=r,o.TagFormatConfiguration=a.Configuration.create("tagFormat",{config:r,configPriority:10,options:{tagFormat:{number:function(t){return t.toString()},tag:function(t){return"("+t+")"},id:function(t){return"mjx-eqn-"+t.replace(/\s/g,"_")},url:function(t,o){return o+"#"+encodeURIComponent(t)}}}})},function(t,o,n){"use strict";Object.defineProperty(o,"__esModule",{value:!0}),o.Configuration=MathJax._.input.tex.Configuration.Configuration,o.ConfigurationHandler=MathJax._.input.tex.Configuration.ConfigurationHandler},function(t,o,n){"use strict";Object.defineProperty(o,"__esModule",{value:!0}),o.Label=MathJax._.input.tex.Tags.Label,o.TagInfo=MathJax._.input.tex.Tags.TagInfo,o.AbstractTags=MathJax._.input.tex.Tags.AbstractTags,o.NoTags=MathJax._.input.tex.Tags.NoTags,o.AllTags=MathJax._.input.tex.Tags.AllTags,o.TagsFactory=MathJax._.input.tex.Tags.TagsFactory},function(t,o,n){"use strict";n.r(o);var e=n(0),a=n(1);Object(e.combineWithMathJax)({_:{input:{tex:{tag_format:{TagFormatConfiguration:a}}}}})}]);