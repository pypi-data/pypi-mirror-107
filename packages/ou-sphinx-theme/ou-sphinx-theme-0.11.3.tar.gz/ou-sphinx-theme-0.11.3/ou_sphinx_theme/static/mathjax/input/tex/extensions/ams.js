!function(){"use strict";var t,e,a,r,n={577:function(t,e,a){var r,n,l=this&&this.__extends||(r=function(t,e){return(r=Object.setPrototypeOf||{__proto__:[]}instanceof Array&&function(t,e){t.__proto__=e}||function(t,e){for(var a in e)Object.prototype.hasOwnProperty.call(e,a)&&(t[a]=e[a])})(t,e)},function(t,e){if("function"!=typeof e&&null!==e)throw new TypeError("Class extends value "+String(e)+" is not a constructor or null");function a(){this.constructor=t}r(t,e),t.prototype=null===e?Object.create(e):(a.prototype=e.prototype,new a)});Object.defineProperty(e,"__esModule",{value:!0}),e.AmsConfiguration=e.AmsTags=void 0;var i=a(251),o=a(971),s=a(680),m=a(16);a(829);var u=a(871),c=function(t){function e(){return null!==t&&t.apply(this,arguments)||this}return l(e,t),e}(s.AbstractTags);e.AmsTags=c;e.AmsConfiguration=i.Configuration.create("ams",{handler:{delimiter:["AMSsymbols-delimiter","AMSmath-delimiter"],macro:["AMSsymbols-mathchar0mi","AMSsymbols-mathchar0mo","AMSsymbols-delimiter","AMSsymbols-macros","AMSmath-mathchar0mo","AMSmath-macros","AMSmath-delimiter"],environment:["AMSmath-environment"]},items:(n={},n[o.MultlineItem.prototype.kind]=o.MultlineItem,n),tags:{ams:c},init:function(t){new u.CommandMap(m.NEW_OPS,{},{}),t.append(i.Configuration.local({handler:{macro:[m.NEW_OPS]},priority:-1}))}})},971:function(t,e,a){var r,n=this&&this.__extends||(r=function(t,e){return(r=Object.setPrototypeOf||{__proto__:[]}instanceof Array&&function(t,e){t.__proto__=e}||function(t,e){for(var a in e)Object.prototype.hasOwnProperty.call(e,a)&&(t[a]=e[a])})(t,e)},function(t,e){if("function"!=typeof e&&null!==e)throw new TypeError("Class extends value "+String(e)+" is not a constructor or null");function a(){this.constructor=t}r(t,e),t.prototype=null===e?Object.create(e):(a.prototype=e.prototype,new a)});Object.defineProperty(e,"__esModule",{value:!0}),e.MultlineItem=void 0;var l=a(935),i=a(398),o=a(748),s=a(402),m=a(108),u=function(t){function e(e){for(var a=[],r=1;r<arguments.length;r++)a[r-1]=arguments[r];var n=t.call(this,e)||this;return n.factory.configuration.tags.start("multline",!0,a[0]),n}return n(e,t),Object.defineProperty(e.prototype,"kind",{get:function(){return"multline"},enumerable:!1,configurable:!0}),e.prototype.EndEntry=function(){this.table.length&&i.default.fixInitialMO(this.factory.configuration,this.nodes);var t=this.getProperty("shove"),e=this.create("node","mtd",this.nodes,t?{columnalign:t}:{});this.setProperty("shove",null),this.row.push(e),this.Clear()},e.prototype.EndRow=function(){if(1!==this.row.length)throw new s.default("MultlineRowsOneCol","The rows within the %1 environment must have exactly one column","multline");var t=this.create("node","mtr",this.row);this.table.push(t),this.row=[]},e.prototype.EndTable=function(){if(t.prototype.EndTable.call(this),this.table.length){var e=this.table.length-1,a=-1;o.default.getAttribute(o.default.getChildren(this.table[0])[0],"columnalign")||o.default.setAttribute(o.default.getChildren(this.table[0])[0],"columnalign",m.TexConstant.Align.LEFT),o.default.getAttribute(o.default.getChildren(this.table[e])[0],"columnalign")||o.default.setAttribute(o.default.getChildren(this.table[e])[0],"columnalign",m.TexConstant.Align.RIGHT);var r=this.factory.configuration.tags.getTag();if(r){a=this.arraydef.side===m.TexConstant.Align.LEFT?0:this.table.length-1;var n=this.table[a],l=this.create("node","mlabeledtr",[r].concat(o.default.getChildren(n)));o.default.copyAttributes(n,l),this.table[a]=l}}this.factory.configuration.tags.end()},e}(l.ArrayItem);e.MultlineItem=u},829:function(t,e,a){Object.defineProperty(e,"__esModule",{value:!0});var r=a(16),n=a(871),l=a(108),i=a(945),o=a(398),s=a(801),m=a(230),u=function(t){for(var e=[],a=0,r=t.length;a<r;a++)e[a]=o.default.Em(t[a]);return e.join(" ")};new n.CharacterMap("AMSmath-mathchar0mo",i.default.mathchar0mo,{iiiint:["\u2a0c",{texClass:s.TEXCLASS.OP}]}),new n.CommandMap("AMSmath-macros",{mathring:["Accent","02DA"],nobreakspace:"Tilde",negmedspace:["Spacer",m.MATHSPACE.negativemediummathspace],negthickspace:["Spacer",m.MATHSPACE.negativethickmathspace],idotsint:["MultiIntegral","\\int\\cdots\\int"],dddot:["Accent","20DB"],ddddot:["Accent","20DC"],sideset:["Macro","\\mathop{\\mathop{\\rlap{\\phantom{#3}}}\\nolimits#1\\!\\mathop{#3}\\nolimits#2}",3],boxed:["Macro","\\fbox{$\\displaystyle{#1}$}",1],tag:"HandleTag",notag:"HandleNoTag",eqref:["HandleRef",!0],substack:["Macro","\\begin{subarray}{c}#1\\end{subarray}",1],injlim:["NamedOp","inj&thinsp;lim"],projlim:["NamedOp","proj&thinsp;lim"],varliminf:["Macro","\\mathop{\\underline{\\mmlToken{mi}{lim}}}"],varlimsup:["Macro","\\mathop{\\overline{\\mmlToken{mi}{lim}}}"],varinjlim:["Macro","\\mathop{\\underrightarrow{\\mmlToken{mi}{lim}}}"],varprojlim:["Macro","\\mathop{\\underleftarrow{\\mmlToken{mi}{lim}}}"],DeclareMathOperator:"HandleDeclareOp",operatorname:"HandleOperatorName",SkipLimits:"SkipLimits",genfrac:"Genfrac",frac:["Genfrac","","","",""],tfrac:["Genfrac","","","","1"],dfrac:["Genfrac","","","","0"],binom:["Genfrac","(",")","0",""],tbinom:["Genfrac","(",")","0","1"],dbinom:["Genfrac","(",")","0","0"],cfrac:"CFrac",shoveleft:["HandleShove",l.TexConstant.Align.LEFT],shoveright:["HandleShove",l.TexConstant.Align.RIGHT],xrightarrow:["xArrow",8594,7,12],xleftarrow:["xArrow",8592,10,5]},r.AmsMethods),new n.EnvironmentMap("AMSmath-environment",i.default.environment,{"eqnarray*":["EqnArray",null,!1,!0,"rcl","0 "+m.em(m.MATHSPACE.thickmathspace),".5em"],align:["EqnArray",null,!0,!0,"rlrlrlrlrlrl",u([0,2,0,2,0,2,0,2,0,2,0])],"align*":["EqnArray",null,!1,!0,"rlrlrlrlrlrl",u([0,2,0,2,0,2,0,2,0,2,0])],multline:["Multline",null,!0],"multline*":["Multline",null,!1],split:["EqnArray",null,!1,!1,"rl",u([0])],gather:["EqnArray",null,!0,!0,"c"],"gather*":["EqnArray",null,!1,!0,"c"],alignat:["AlignAt",null,!0,!0],"alignat*":["AlignAt",null,!1,!0],alignedat:["AlignAt",null,!1,!1],aligned:["AmsEqnArray",null,null,null,"rlrlrlrlrlrl",u([0,2,0,2,0,2,0,2,0,2,0]),".5em","D"],gathered:["AmsEqnArray",null,null,null,"c",null,".5em","D"],subarray:["Array",null,null,null,null,u([0]),"0.1em","S",1],smallmatrix:["Array",null,null,null,"c",u([1/3]),".2em","S",1],matrix:["Array",null,null,null,"c"],pmatrix:["Array",null,"(",")","c"],bmatrix:["Array",null,"[","]","c"],Bmatrix:["Array",null,"\\{","\\}","c"],vmatrix:["Array",null,"\\vert","\\vert","c"],Vmatrix:["Array",null,"\\Vert","\\Vert","c"],cases:["Array",null,"\\{",".","ll",null,".2em","T"]},r.AmsMethods),new n.DelimiterMap("AMSmath-delimiter",i.default.delimiter,{"\\lvert":["|",{texClass:s.TEXCLASS.OPEN}],"\\rvert":["|",{texClass:s.TEXCLASS.CLOSE}],"\\lVert":["\u2016",{texClass:s.TEXCLASS.OPEN}],"\\rVert":["\u2016",{texClass:s.TEXCLASS.CLOSE}]}),new n.CharacterMap("AMSsymbols-mathchar0mi",i.default.mathchar0mi,{digamma:"\u03dd",varkappa:"\u03f0",varGamma:["\u0393",{mathvariant:l.TexConstant.Variant.ITALIC}],varDelta:["\u0394",{mathvariant:l.TexConstant.Variant.ITALIC}],varTheta:["\u0398",{mathvariant:l.TexConstant.Variant.ITALIC}],varLambda:["\u039b",{mathvariant:l.TexConstant.Variant.ITALIC}],varXi:["\u039e",{mathvariant:l.TexConstant.Variant.ITALIC}],varPi:["\u03a0",{mathvariant:l.TexConstant.Variant.ITALIC}],varSigma:["\u03a3",{mathvariant:l.TexConstant.Variant.ITALIC}],varUpsilon:["\u03a5",{mathvariant:l.TexConstant.Variant.ITALIC}],varPhi:["\u03a6",{mathvariant:l.TexConstant.Variant.ITALIC}],varPsi:["\u03a8",{mathvariant:l.TexConstant.Variant.ITALIC}],varOmega:["\u03a9",{mathvariant:l.TexConstant.Variant.ITALIC}],beth:"\u2136",gimel:"\u2137",daleth:"\u2138",backprime:["\u2035",{variantForm:!0}],hslash:"\u210f",varnothing:["\u2205",{variantForm:!0}],blacktriangle:"\u25b4",triangledown:["\u25bd",{variantForm:!0}],blacktriangledown:"\u25be",square:"\u25fb",Box:"\u25fb",blacksquare:"\u25fc",lozenge:"\u25ca",Diamond:"\u25ca",blacklozenge:"\u29eb",circledS:["\u24c8",{mathvariant:l.TexConstant.Variant.NORMAL}],bigstar:"\u2605",sphericalangle:"\u2222",measuredangle:"\u2221",nexists:"\u2204",complement:"\u2201",mho:"\u2127",eth:["\xf0",{mathvariant:l.TexConstant.Variant.NORMAL}],Finv:"\u2132",diagup:"\u2571",Game:"\u2141",diagdown:"\u2572",Bbbk:["k",{mathvariant:l.TexConstant.Variant.DOUBLESTRUCK}],yen:"\xa5",circledR:"\xae",checkmark:"\u2713",maltese:"\u2720"}),new n.CharacterMap("AMSsymbols-mathchar0mo",i.default.mathchar0mo,{dotplus:"\u2214",ltimes:"\u22c9",smallsetminus:["\u2216",{variantForm:!0}],rtimes:"\u22ca",Cap:"\u22d2",doublecap:"\u22d2",leftthreetimes:"\u22cb",Cup:"\u22d3",doublecup:"\u22d3",rightthreetimes:"\u22cc",barwedge:"\u22bc",curlywedge:"\u22cf",veebar:"\u22bb",curlyvee:"\u22ce",doublebarwedge:"\u2a5e",boxminus:"\u229f",circleddash:"\u229d",boxtimes:"\u22a0",circledast:"\u229b",boxdot:"\u22a1",circledcirc:"\u229a",boxplus:"\u229e",centerdot:["\u22c5",{variantForm:!0}],divideontimes:"\u22c7",intercal:"\u22ba",leqq:"\u2266",geqq:"\u2267",leqslant:"\u2a7d",geqslant:"\u2a7e",eqslantless:"\u2a95",eqslantgtr:"\u2a96",lesssim:"\u2272",gtrsim:"\u2273",lessapprox:"\u2a85",gtrapprox:"\u2a86",approxeq:"\u224a",lessdot:"\u22d6",gtrdot:"\u22d7",lll:"\u22d8",llless:"\u22d8",ggg:"\u22d9",gggtr:"\u22d9",lessgtr:"\u2276",gtrless:"\u2277",lesseqgtr:"\u22da",gtreqless:"\u22db",lesseqqgtr:"\u2a8b",gtreqqless:"\u2a8c",doteqdot:"\u2251",Doteq:"\u2251",eqcirc:"\u2256",risingdotseq:"\u2253",circeq:"\u2257",fallingdotseq:"\u2252",triangleq:"\u225c",backsim:"\u223d",thicksim:["\u223c",{variantForm:!0}],backsimeq:"\u22cd",thickapprox:["\u2248",{variantForm:!0}],subseteqq:"\u2ac5",supseteqq:"\u2ac6",Subset:"\u22d0",Supset:"\u22d1",sqsubset:"\u228f",sqsupset:"\u2290",preccurlyeq:"\u227c",succcurlyeq:"\u227d",curlyeqprec:"\u22de",curlyeqsucc:"\u22df",precsim:"\u227e",succsim:"\u227f",precapprox:"\u2ab7",succapprox:"\u2ab8",vartriangleleft:"\u22b2",lhd:"\u22b2",vartriangleright:"\u22b3",rhd:"\u22b3",trianglelefteq:"\u22b4",unlhd:"\u22b4",trianglerighteq:"\u22b5",unrhd:"\u22b5",vDash:["\u22a8",{variantForm:!0}],Vdash:"\u22a9",Vvdash:"\u22aa",smallsmile:["\u2323",{variantForm:!0}],shortmid:["\u2223",{variantForm:!0}],smallfrown:["\u2322",{variantForm:!0}],shortparallel:["\u2225",{variantForm:!0}],bumpeq:"\u224f",between:"\u226c",Bumpeq:"\u224e",pitchfork:"\u22d4",varpropto:["\u221d",{variantForm:!0}],backepsilon:"\u220d",blacktriangleleft:"\u25c2",blacktriangleright:"\u25b8",therefore:"\u2234",because:"\u2235",eqsim:"\u2242",vartriangle:["\u25b3",{variantForm:!0}],Join:"\u22c8",nless:"\u226e",ngtr:"\u226f",nleq:"\u2270",ngeq:"\u2271",nleqslant:["\u2a87",{variantForm:!0}],ngeqslant:["\u2a88",{variantForm:!0}],nleqq:["\u2270",{variantForm:!0}],ngeqq:["\u2271",{variantForm:!0}],lneq:"\u2a87",gneq:"\u2a88",lneqq:"\u2268",gneqq:"\u2269",lvertneqq:["\u2268",{variantForm:!0}],gvertneqq:["\u2269",{variantForm:!0}],lnsim:"\u22e6",gnsim:"\u22e7",lnapprox:"\u2a89",gnapprox:"\u2a8a",nprec:"\u2280",nsucc:"\u2281",npreceq:["\u22e0",{variantForm:!0}],nsucceq:["\u22e1",{variantForm:!0}],precneqq:"\u2ab5",succneqq:"\u2ab6",precnsim:"\u22e8",succnsim:"\u22e9",precnapprox:"\u2ab9",succnapprox:"\u2aba",nsim:"\u2241",ncong:"\u2247",nshortmid:["\u2224",{variantForm:!0}],nshortparallel:["\u2226",{variantForm:!0}],nmid:"\u2224",nparallel:"\u2226",nvdash:"\u22ac",nvDash:"\u22ad",nVdash:"\u22ae",nVDash:"\u22af",ntriangleleft:"\u22ea",ntriangleright:"\u22eb",ntrianglelefteq:"\u22ec",ntrianglerighteq:"\u22ed",nsubseteq:"\u2288",nsupseteq:"\u2289",nsubseteqq:["\u2288",{variantForm:!0}],nsupseteqq:["\u2289",{variantForm:!0}],subsetneq:"\u228a",supsetneq:"\u228b",varsubsetneq:["\u228a",{variantForm:!0}],varsupsetneq:["\u228b",{variantForm:!0}],subsetneqq:"\u2acb",supsetneqq:"\u2acc",varsubsetneqq:["\u2acb",{variantForm:!0}],varsupsetneqq:["\u2acc",{variantForm:!0}],leftleftarrows:"\u21c7",rightrightarrows:"\u21c9",leftrightarrows:"\u21c6",rightleftarrows:"\u21c4",Lleftarrow:"\u21da",Rrightarrow:"\u21db",twoheadleftarrow:"\u219e",twoheadrightarrow:"\u21a0",leftarrowtail:"\u21a2",rightarrowtail:"\u21a3",looparrowleft:"\u21ab",looparrowright:"\u21ac",leftrightharpoons:"\u21cb",rightleftharpoons:["\u21cc",{variantForm:!0}],curvearrowleft:"\u21b6",curvearrowright:"\u21b7",circlearrowleft:"\u21ba",circlearrowright:"\u21bb",Lsh:"\u21b0",Rsh:"\u21b1",upuparrows:"\u21c8",downdownarrows:"\u21ca",upharpoonleft:"\u21bf",upharpoonright:"\u21be",downharpoonleft:"\u21c3",restriction:"\u21be",multimap:"\u22b8",downharpoonright:"\u21c2",leftrightsquigarrow:"\u21ad",rightsquigarrow:"\u21dd",leadsto:"\u21dd",dashrightarrow:"\u21e2",dashleftarrow:"\u21e0",nleftarrow:"\u219a",nrightarrow:"\u219b",nLeftarrow:"\u21cd",nRightarrow:"\u21cf",nleftrightarrow:"\u21ae",nLeftrightarrow:"\u21ce"}),new n.DelimiterMap("AMSsymbols-delimiter",i.default.delimiter,{"\\ulcorner":"\u231c","\\urcorner":"\u231d","\\llcorner":"\u231e","\\lrcorner":"\u231f"}),new n.CommandMap("AMSsymbols-macros",{implies:["Macro","\\;\\Longrightarrow\\;"],impliedby:["Macro","\\;\\Longleftarrow\\;"]},r.AmsMethods)},16:function(t,e,a){Object.defineProperty(e,"__esModule",{value:!0}),e.NEW_OPS=e.AmsMethods=void 0;var r=a(398),n=a(748),l=a(108),i=a(193),o=a(402),s=a(924),m=a(360),u=a(801);e.AmsMethods={},e.AmsMethods.AmsEqnArray=function(t,e,a,n,l,i,o){var s=t.GetBrackets("\\begin{"+e.getName()+"}"),u=m.default.EqnArray(t,e,a,n,l,i,o);return r.default.setArrayAlign(u,s)},e.AmsMethods.AlignAt=function(t,a,n,l){var i,s,m=a.getName(),u="",c=[];if(l||(s=t.GetBrackets("\\begin{"+m+"}")),(i=t.GetArgument("\\begin{"+m+"}")).match(/[^0-9]/))throw new o.default("PositiveIntegerArg","Argument to %1 must me a positive integer","\\begin{"+m+"}");for(var d=parseInt(i,10);d>0;)u+="rl",c.push("0em 0em"),d--;var h=c.join(" ");if(l)return e.AmsMethods.EqnArray(t,a,n,l,u,h);var p=e.AmsMethods.EqnArray(t,a,n,l,u,h);return r.default.setArrayAlign(p,s)},e.AmsMethods.Multline=function(t,e,a){t.Push(e),r.default.checkEqnEnv(t);var n=t.itemFactory.create("multline",a,t.stack);return n.arraydef={displaystyle:!0,rowspacing:".5em",columnwidth:"100%",width:t.options.multlineWidth,side:t.options.tagSide,minlabelspacing:t.options.tagIndent},n},e.NEW_OPS="ams-declare-ops",e.AmsMethods.HandleDeclareOp=function(t,a){var n=t.GetStar()?"":"\\nolimits\\SkipLimits",l=r.default.trimSpaces(t.GetArgument(a));"\\"===l.charAt(0)&&(l=l.substr(1));var i=t.GetArgument(a);i.match(/\\text/)||(i=i.replace(/\*/g,"\\text{*}").replace(/-/g,"\\text{-}")),t.configuration.handlers.retrieve(e.NEW_OPS).add(l,new s.Macro(l,e.AmsMethods.Macro,["\\mathop{\\rm "+i+"}"+n]))},e.AmsMethods.HandleOperatorName=function(t,e){var a=t.GetStar()?"":"\\nolimits\\SkipLimits",n=r.default.trimSpaces(t.GetArgument(e));n.match(/\\text/)||(n=n.replace(/\*/g,"\\text{*}").replace(/-/g,"\\text{-}")),t.string="\\mathop{\\rm "+n+"}"+a+" "+t.string.slice(t.i),t.i=0},e.AmsMethods.SkipLimits=function(t,e){var a=t.GetNext(),r=t.i;"\\"===a&&++t.i&&"limits"!==t.GetCS()&&(t.i=r)},e.AmsMethods.MultiIntegral=function(t,e,a){var r=t.GetNext();if("\\"===r){var n=t.i;r=t.GetArgument(e),t.i=n,"\\limits"===r&&(a="\\idotsint"===e?"\\!\\!\\mathop{\\,\\,"+a+"}":"\\!\\!\\!\\mathop{\\,\\,\\,"+a+"}")}t.string=a+" "+t.string.slice(t.i),t.i=0},e.AmsMethods.xArrow=function(t,e,a,l,o){var s={width:"+"+r.default.Em((l+o)/18),lspace:r.default.Em(l/18)},m=t.GetBrackets(e),c=t.ParseArg(e),d=t.create("node","mspace",[],{depth:".25em"}),h=t.create("token","mo",{stretchy:!0,texClass:u.TEXCLASS.REL},String.fromCodePoint(a));h=t.create("node","mstyle",[h],{scriptlevel:0});var p=t.create("node","munderover",[h]),g=t.create("node","mpadded",[c,d],s);if(n.default.setAttribute(g,"voffset","-.2em"),n.default.setAttribute(g,"height","-.2em"),n.default.setChild(p,p.over,g),m){var f=new i.default(m,t.stack.env,t.configuration).mml(),M=t.create("node","mspace",[],{height:".75em"});g=t.create("node","mpadded",[f,M],s),n.default.setAttribute(g,"voffset",".15em"),n.default.setAttribute(g,"depth","-.15em"),n.default.setChild(p,p.under,g)}n.default.setProperty(p,"subsupOK",!0),t.Push(p)},e.AmsMethods.HandleShove=function(t,e,a){var r=t.stack.Top();if("multline"!==r.kind)throw new o.default("CommandOnlyAllowedInEnv","%1 only allowed in %2 environment",t.currentCS,"multline");if(r.Size())throw new o.default("CommandAtTheBeginingOfLine","%1 must come at the beginning of the line",t.currentCS);r.setProperty("shove",a)},e.AmsMethods.CFrac=function(t,e){var a=r.default.trimSpaces(t.GetBrackets(e,"")),s=t.GetArgument(e),m=t.GetArgument(e),u={l:l.TexConstant.Align.LEFT,r:l.TexConstant.Align.RIGHT,"":""},c=new i.default("\\strut\\textstyle{"+s+"}",t.stack.env,t.configuration).mml(),d=new i.default("\\strut\\textstyle{"+m+"}",t.stack.env,t.configuration).mml(),h=t.create("node","mfrac",[c,d]);if(null==(a=u[a]))throw new o.default("IllegalAlign","Illegal alignment specified in %1",t.currentCS);a&&n.default.setProperties(h,{numalign:a,denomalign:a}),t.Push(h)},e.AmsMethods.Genfrac=function(t,e,a,l,i,s){null==a&&(a=t.GetDelimiterArg(e)),null==l&&(l=t.GetDelimiterArg(e)),null==i&&(i=t.GetArgument(e)),null==s&&(s=r.default.trimSpaces(t.GetArgument(e)));var m=t.ParseArg(e),u=t.ParseArg(e),c=t.create("node","mfrac",[m,u]);if(""!==i&&n.default.setAttribute(c,"linethickness",i),(a||l)&&(n.default.setProperty(c,"withDelims",!0),c=r.default.fixedFence(t.configuration,a,c,l)),""!==s){var d=parseInt(s,10),h=["D","T","S","SS"][d];if(null==h)throw new o.default("BadMathStyleFor","Bad math style for %1",t.currentCS);c=t.create("node","mstyle",[c]),"D"===h?n.default.setProperties(c,{displaystyle:!0,scriptlevel:0}):n.default.setProperties(c,{displaystyle:!1,scriptlevel:d-1})}t.Push(c)},e.AmsMethods.HandleTag=function(t,e){if(!t.tags.currentTag.taggable&&t.tags.env)throw new o.default("CommandNotAllowedInEnv","%1 not allowed in %2 environment",t.currentCS,t.tags.env);if(t.tags.currentTag.tag)throw new o.default("MultipleCommand","Multiple %1",t.currentCS);var a=t.GetStar(),n=r.default.trimSpaces(t.GetArgument(e));t.tags.tag(n,a)},e.AmsMethods.HandleNoTag=m.default.HandleNoTag,e.AmsMethods.HandleRef=m.default.HandleRef,e.AmsMethods.Macro=m.default.Macro,e.AmsMethods.Accent=m.default.Accent,e.AmsMethods.Tilde=m.default.Tilde,e.AmsMethods.Array=m.default.Array,e.AmsMethods.Spacer=m.default.Spacer,e.AmsMethods.NamedOp=m.default.NamedOp,e.AmsMethods.EqnArray=m.default.EqnArray},955:function(t,e){MathJax._.components.global.isObject,MathJax._.components.global.combineConfig,MathJax._.components.global.combineDefaults,e.r8=MathJax._.components.global.combineWithMathJax,MathJax._.components.global.MathJax},801:function(t,e){Object.defineProperty(e,"__esModule",{value:!0}),e.TEXCLASS=MathJax._.core.MmlTree.MmlNode.TEXCLASS,e.TEXCLASSNAMES=MathJax._.core.MmlTree.MmlNode.TEXCLASSNAMES,e.indentAttributes=MathJax._.core.MmlTree.MmlNode.indentAttributes,e.AbstractMmlNode=MathJax._.core.MmlTree.MmlNode.AbstractMmlNode,e.AbstractMmlTokenNode=MathJax._.core.MmlTree.MmlNode.AbstractMmlTokenNode,e.AbstractMmlLayoutNode=MathJax._.core.MmlTree.MmlNode.AbstractMmlLayoutNode,e.AbstractMmlBaseNode=MathJax._.core.MmlTree.MmlNode.AbstractMmlBaseNode,e.AbstractMmlEmptyNode=MathJax._.core.MmlTree.MmlNode.AbstractMmlEmptyNode,e.TextNode=MathJax._.core.MmlTree.MmlNode.TextNode,e.XMLNode=MathJax._.core.MmlTree.MmlNode.XMLNode},230:function(t,e){Object.defineProperty(e,"__esModule",{value:!0}),e.BIGDIMEN=MathJax._.util.lengths.BIGDIMEN,e.UNITS=MathJax._.util.lengths.UNITS,e.RELUNITS=MathJax._.util.lengths.RELUNITS,e.MATHSPACE=MathJax._.util.lengths.MATHSPACE,e.length2em=MathJax._.util.lengths.length2em,e.percent=MathJax._.util.lengths.percent,e.em=MathJax._.util.lengths.em,e.emRounded=MathJax._.util.lengths.emRounded,e.px=MathJax._.util.lengths.px},251:function(t,e){Object.defineProperty(e,"__esModule",{value:!0}),e.Configuration=MathJax._.input.tex.Configuration.Configuration,e.ConfigurationHandler=MathJax._.input.tex.Configuration.ConfigurationHandler,e.ParserConfiguration=MathJax._.input.tex.Configuration.ParserConfiguration},748:function(t,e){Object.defineProperty(e,"__esModule",{value:!0}),e.default=MathJax._.input.tex.NodeUtil.default},945:function(t,e){Object.defineProperty(e,"__esModule",{value:!0}),e.default=MathJax._.input.tex.ParseMethods.default},398:function(t,e){Object.defineProperty(e,"__esModule",{value:!0}),e.default=MathJax._.input.tex.ParseUtil.default},924:function(t,e){Object.defineProperty(e,"__esModule",{value:!0}),e.Symbol=MathJax._.input.tex.Symbol.Symbol,e.Macro=MathJax._.input.tex.Symbol.Macro},871:function(t,e){Object.defineProperty(e,"__esModule",{value:!0}),e.AbstractSymbolMap=MathJax._.input.tex.SymbolMap.AbstractSymbolMap,e.RegExpMap=MathJax._.input.tex.SymbolMap.RegExpMap,e.AbstractParseMap=MathJax._.input.tex.SymbolMap.AbstractParseMap,e.CharacterMap=MathJax._.input.tex.SymbolMap.CharacterMap,e.DelimiterMap=MathJax._.input.tex.SymbolMap.DelimiterMap,e.MacroMap=MathJax._.input.tex.SymbolMap.MacroMap,e.CommandMap=MathJax._.input.tex.SymbolMap.CommandMap,e.EnvironmentMap=MathJax._.input.tex.SymbolMap.EnvironmentMap},680:function(t,e){Object.defineProperty(e,"__esModule",{value:!0}),e.Label=MathJax._.input.tex.Tags.Label,e.TagInfo=MathJax._.input.tex.Tags.TagInfo,e.AbstractTags=MathJax._.input.tex.Tags.AbstractTags,e.NoTags=MathJax._.input.tex.Tags.NoTags,e.AllTags=MathJax._.input.tex.Tags.AllTags,e.TagsFactory=MathJax._.input.tex.Tags.TagsFactory},108:function(t,e){Object.defineProperty(e,"__esModule",{value:!0}),e.TexConstant=MathJax._.input.tex.TexConstants.TexConstant},402:function(t,e){Object.defineProperty(e,"__esModule",{value:!0}),e.default=MathJax._.input.tex.TexError.default},193:function(t,e){Object.defineProperty(e,"__esModule",{value:!0}),e.default=MathJax._.input.tex.TexParser.default},935:function(t,e){Object.defineProperty(e,"__esModule",{value:!0}),e.StartItem=MathJax._.input.tex.base.BaseItems.StartItem,e.StopItem=MathJax._.input.tex.base.BaseItems.StopItem,e.OpenItem=MathJax._.input.tex.base.BaseItems.OpenItem,e.CloseItem=MathJax._.input.tex.base.BaseItems.CloseItem,e.PrimeItem=MathJax._.input.tex.base.BaseItems.PrimeItem,e.SubsupItem=MathJax._.input.tex.base.BaseItems.SubsupItem,e.OverItem=MathJax._.input.tex.base.BaseItems.OverItem,e.LeftItem=MathJax._.input.tex.base.BaseItems.LeftItem,e.Middle=MathJax._.input.tex.base.BaseItems.Middle,e.RightItem=MathJax._.input.tex.base.BaseItems.RightItem,e.BeginItem=MathJax._.input.tex.base.BaseItems.BeginItem,e.EndItem=MathJax._.input.tex.base.BaseItems.EndItem,e.StyleItem=MathJax._.input.tex.base.BaseItems.StyleItem,e.PositionItem=MathJax._.input.tex.base.BaseItems.PositionItem,e.CellItem=MathJax._.input.tex.base.BaseItems.CellItem,e.MmlItem=MathJax._.input.tex.base.BaseItems.MmlItem,e.FnItem=MathJax._.input.tex.base.BaseItems.FnItem,e.NotItem=MathJax._.input.tex.base.BaseItems.NotItem,e.DotsItem=MathJax._.input.tex.base.BaseItems.DotsItem,e.ArrayItem=MathJax._.input.tex.base.BaseItems.ArrayItem,e.EqnArrayItem=MathJax._.input.tex.base.BaseItems.EqnArrayItem,e.EquationItem=MathJax._.input.tex.base.BaseItems.EquationItem},360:function(t,e){Object.defineProperty(e,"__esModule",{value:!0}),e.default=MathJax._.input.tex.base.BaseMethods.default}},l={};function i(t){var e=l[t];if(void 0!==e)return e.exports;var a=l[t]={exports:{}};return n[t].call(a.exports,a,a.exports,i),a.exports}t=i(955),e=i(577),a=i(971),r=i(16),(0,t.r8)({_:{input:{tex:{ams:{AmsConfiguration:e,AmsItems:a,AmsMethods:r}}}}})}();