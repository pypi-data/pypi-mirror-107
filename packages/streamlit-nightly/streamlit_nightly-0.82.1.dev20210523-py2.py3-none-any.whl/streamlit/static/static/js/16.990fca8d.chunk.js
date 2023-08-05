/*! For license information please see 16.990fca8d.chunk.js.LICENSE.txt */
(this["webpackJsonpstreamlit-browser"]=this["webpackJsonpstreamlit-browser"]||[]).push([[16],{2882:function(e,t,n){var r;!function(){"use strict";var i={not_string:/[^s]/,not_bool:/[^t]/,not_type:/[^T]/,not_primitive:/[^v]/,number:/[diefg]/,numeric_arg:/[bcdiefguxX]/,json:/[j]/,not_json:/[^j]/,text:/^[^\x25]+/,modulo:/^\x25{2}/,placeholder:/^\x25(?:([1-9]\d*)\$|\(([^)]+)\))?(\+)?(0|'[^$])?(-)?(\d+)?(?:\.(\d+))?([b-gijostTuvxX])/,key:/^([a-z_][a-z_\d]*)/i,key_access:/^\.([a-z_][a-z_\d]*)/i,index_access:/^\[(\d+)\]/,sign:/^[+-]/};function o(e){return a(l(e),arguments)}function s(e,t){return o.apply(null,[e].concat(t||[]))}function a(e,t){var n,r,s,a,c,l,u,p,h,f=1,d=e.length,b="";for(r=0;r<d;r++)if("string"===typeof e[r])b+=e[r];else if("object"===typeof e[r]){if((a=e[r]).keys)for(n=t[f],s=0;s<a.keys.length;s++){if(void 0==n)throw new Error(o('[sprintf] Cannot access property "%s" of undefined value "%s"',a.keys[s],a.keys[s-1]));n=n[a.keys[s]]}else n=a.param_no?t[a.param_no]:t[f++];if(i.not_type.test(a.type)&&i.not_primitive.test(a.type)&&n instanceof Function&&(n=n()),i.numeric_arg.test(a.type)&&"number"!==typeof n&&isNaN(n))throw new TypeError(o("[sprintf] expecting number but found %T",n));switch(i.number.test(a.type)&&(p=n>=0),a.type){case"b":n=parseInt(n,10).toString(2);break;case"c":n=String.fromCharCode(parseInt(n,10));break;case"d":case"i":n=parseInt(n,10);break;case"j":n=JSON.stringify(n,null,a.width?parseInt(a.width):0);break;case"e":n=a.precision?parseFloat(n).toExponential(a.precision):parseFloat(n).toExponential();break;case"f":n=a.precision?parseFloat(n).toFixed(a.precision):parseFloat(n);break;case"g":n=a.precision?String(Number(n.toPrecision(a.precision))):parseFloat(n);break;case"o":n=(parseInt(n,10)>>>0).toString(8);break;case"s":n=String(n),n=a.precision?n.substring(0,a.precision):n;break;case"t":n=String(!!n),n=a.precision?n.substring(0,a.precision):n;break;case"T":n=Object.prototype.toString.call(n).slice(8,-1).toLowerCase(),n=a.precision?n.substring(0,a.precision):n;break;case"u":n=parseInt(n,10)>>>0;break;case"v":n=n.valueOf(),n=a.precision?n.substring(0,a.precision):n;break;case"x":n=(parseInt(n,10)>>>0).toString(16);break;case"X":n=(parseInt(n,10)>>>0).toString(16).toUpperCase()}i.json.test(a.type)?b+=n:(!i.number.test(a.type)||p&&!a.sign?h="":(h=p?"+":"-",n=n.toString().replace(i.sign,"")),l=a.pad_char?"0"===a.pad_char?"0":a.pad_char.charAt(1):" ",u=a.width-(h+n).length,c=a.width&&u>0?l.repeat(u):"",b+=a.align?h+n+c:"0"===l?h+c+n:c+h+n)}return b}var c=Object.create(null);function l(e){if(c[e])return c[e];for(var t,n=e,r=[],o=0;n;){if(null!==(t=i.text.exec(n)))r.push(t[0]);else if(null!==(t=i.modulo.exec(n)))r.push("%");else{if(null===(t=i.placeholder.exec(n)))throw new SyntaxError("[sprintf] unexpected placeholder");if(t[2]){o|=1;var s=[],a=t[2],l=[];if(null===(l=i.key.exec(a)))throw new SyntaxError("[sprintf] failed to parse named argument key");for(s.push(l[1]);""!==(a=a.substring(l[0].length));)if(null!==(l=i.key_access.exec(a)))s.push(l[1]);else{if(null===(l=i.index_access.exec(a)))throw new SyntaxError("[sprintf] failed to parse named argument key");s.push(l[1])}t[2]=s}else o|=2;if(3===o)throw new Error("[sprintf] mixing positional and named placeholders is not (yet) supported");r.push({placeholder:t[0],param_no:t[1],keys:t[2],sign:t[3],pad_char:t[4],align:t[5],width:t[6],precision:t[7],type:t[8]})}n=n.substring(t[0].length)}return c[e]=r}t.sprintf=o,t.vsprintf=s,"undefined"!==typeof window&&(window.sprintf=o,window.vsprintf=s,void 0===(r=function(){return{sprintf:o,vsprintf:s}}.call(t,n,t,e))||(e.exports=r))}()},2908:function(e,t,n){"use strict";n(0);var r,i=n(31),o=n(119),s=n(6),a=n(171),c=n(8),l=n.n(c),u=n(80);const p=Object(u.keyframes)(r||(r=Object(a.a)(["\n  50% {\n    color: rgba(0, 0, 0, 0);\n  }\n"]))),h=l()("span",{target:"e1m4n6jn0"})((({includeDot:e,shouldBlink:t,theme:n})=>Object(s.a)(Object(s.a)({},e?{"&::before":{opacity:1,content:'"\u2022"',animation:"none",color:n.colors.gray,margin:"0 5px"}}:{}),t?{color:n.colors.red,animationName:"".concat(p),animationDuration:"0.5s",animationIterationCount:5}:{})),"");var f=n(5);t.a=({dirty:e,value:t,maxLength:n,className:r,type:s="single"})=>{const a=[],c=(e,t=!1)=>{a.push(Object(f.jsx)(h,{includeDot:a.length>0,shouldBlink:t,children:e},a.length))};return e&&("multiline"===s?Object(i.f)()?c("Press \u2318+Enter to apply"):c("Press Ctrl+Enter to apply"):c("Press Enter to apply")),n&&c("".concat(t.length,"/").concat(n),e&&t.length>=n),Object(f.jsx)(o.a,{className:r,children:a})}},3022:function(e,t,n){"use strict";var r=n(0),i=n(9),o=n(2948),s=n(3028),a=n(2877),c=n(77);function l(e){return(l="function"===typeof Symbol&&"symbol"===typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"===typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e})(e)}function u(){return(u=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var r in n)Object.prototype.hasOwnProperty.call(n,r)&&(e[r]=n[r])}return e}).apply(this,arguments)}function p(e,t){return function(e){if(Array.isArray(e))return e}(e)||function(e,t){if(!(Symbol.iterator in Object(e))&&"[object Arguments]"!==Object.prototype.toString.call(e))return;var n=[],r=!0,i=!1,o=void 0;try{for(var s,a=e[Symbol.iterator]();!(r=(s=a.next()).done)&&(n.push(s.value),!t||n.length!==t);r=!0);}catch(c){i=!0,o=c}finally{try{r||null==a.return||a.return()}finally{if(i)throw o}}return n}(e,t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance")}()}function h(e,t){if(null==e)return{};var n,r,i=function(e,t){if(null==e)return{};var n,r,i={},o=Object.keys(e);for(r=0;r<o.length;r++)n=o[r],t.indexOf(n)>=0||(i[n]=e[n]);return i}(e,t);if(Object.getOwnPropertySymbols){var o=Object.getOwnPropertySymbols(e);for(r=0;r<o.length;r++)n=o[r],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(i[n]=e[n])}return i}function f(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function d(e,t){for(var n=0;n<t.length;n++){var r=t[n];r.enumerable=r.enumerable||!1,r.configurable=!0,"value"in r&&(r.writable=!0),Object.defineProperty(e,r.key,r)}}function b(e,t){return!t||"object"!==l(t)&&"function"!==typeof t?m(e):t}function y(e){return(y=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}function m(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}function g(e,t){return(g=Object.setPrototypeOf||function(e,t){return e.__proto__=t,e})(e,t)}function j(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}var v=function(e){function t(){var e,n;f(this,t);for(var r=arguments.length,i=new Array(r),o=0;o<r;o++)i[o]=arguments[o];return j(m(n=b(this,(e=y(t)).call.apply(e,[this].concat(i)))),"state",{isFocused:n.props.autoFocus||!1}),j(m(n),"onFocus",(function(e){n.setState({isFocused:!0}),n.props.onFocus(e)})),j(m(n),"onBlur",(function(e){n.setState({isFocused:!1}),n.props.onBlur(e)})),n}var n,l,v;return function(e,t){if("function"!==typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),t&&g(e,t)}(t,e),n=t,(l=[{key:"render",value:function(){var e=this.props,t=e.startEnhancer,n=e.endEnhancer,l=e.overrides,f=l.Root,d=l.StartEnhancer,b=l.EndEnhancer,y=h(l,["Root","StartEnhancer","EndEnhancer"]),m=h(e,["startEnhancer","endEnhancer","overrides"]),g=p(Object(i.c)(f,a.d),2),j=g[0],v=g[1],x=p(Object(i.c)(d,a.c),2),O=x[0],k=x[1],S=p(Object(i.c)(b,a.c),2),E=S[0],_=S[1],I=Object(o.a)(this.props,this.state);return r.createElement(j,u({"data-baseweb":"input"},I,v,{$adjoined:w(t,n),$hasIconTrailing:this.props.clearable||"password"==this.props.type}),t&&r.createElement(O,u({},I,k,{$position:c.c.start}),"function"===typeof t?t(I):t),r.createElement(s.a,u({},m,{overrides:y,adjoined:w(t,n),onFocus:this.onFocus,onBlur:this.onBlur})),n&&r.createElement(E,u({},I,_,{$position:c.c.end}),"function"===typeof n?n(I):n))}}])&&d(n.prototype,l),v&&d(n,v),t}(r.Component);function w(e,t){return e&&t?c.a.both:e?c.a.left:t?c.a.right:c.a.none}j(v,"defaultProps",{autoComplete:"on",autoFocus:!1,disabled:!1,name:"",error:!1,onBlur:function(){},onFocus:function(){},overrides:{},required:!1,size:c.d.default,startEnhancer:null,endEnhancer:null,clearable:!1,type:"text"}),t.a=v},3887:function(e,t,n){"use strict";n.r(t),n.d(t,"default",(function(){return O}));var r=n(0),i=n.n(r),o=n(71),s=n(2882),a=n(12),c=n(11),l=n(120),u=n(56),p=n(69),h=n(3022),f=n(2908),d=n(119),b=n(8),y=n.n(b);const m=y()("div",{target:"e1jwn65y0"})((({theme:e})=>({display:"flex",flexDirection:"row",flexWrap:"nowrap",alignItems:"center",input:{MozAppearance:"textfield","&::-webkit-inner-spin-button, &::-webkit-outer-spin-button":{WebkitAppearance:"none",margin:e.spacing.none}}})),""),g=y()("div",{target:"e1jwn65y1"})({name:"fjj0yo",styles:"height:49px;display:flex;flex-direction:row;"}),j=y()("button",{target:"e1jwn65y2"})((({theme:e})=>({margin:e.spacing.none,border:"none",height:e.sizes.full,display:"flex",cursor:"pointer",alignItems:"center",width:"".concat(45,"px"),justifyContent:"center",color:e.colors.bodyText,transition:"color 300ms, backgroundColor 300ms",backgroundColor:e.colors.secondaryBg,"&:hover, &:focus":{color:e.colors.white,backgroundColor:e.colors.primary,transition:"none",outline:"none"},"&:active":{outline:"none",border:"none"},"&:last-of-type":{borderTopRightRadius:e.radii.md,borderBottomRightRadius:e.radii.md}})),""),v=y()("div",{target:"e1jwn65y3"})((({theme:e})=>({position:"absolute",marginRight:e.spacing.twoXS,left:0,right:"".concat(90,"px")})),"");var w=n(5);class x extends i.a.PureComponent{constructor(e){super(e),this.inputRef=i.a.createRef(),this.formatValue=e=>{const t=function(e){return null==e||""===e?void 0:e}(this.props.element.format);if(null==t)return e.toString();try{return Object(s.sprintf)(t,e)}catch(n){return Object(a.d)("Error in sprintf(".concat(t,", ").concat(e,"): ").concat(n)),String(e)}},this.isIntData=()=>this.props.element.dataType===c.l.DataType.INT,this.getMin=()=>this.props.element.hasMin?this.props.element.min:-1/0,this.getMax=()=>this.props.element.hasMax?this.props.element.max:1/0,this.getStep=()=>{const e=this.props.element.step;return e||(this.isIntData()?1:.01)},this.commitWidgetValue=e=>{const t=this.state.value,n=this.props,r=n.element,i=n.widgetMgr,o=this.props.element,s=this.getMin(),a=this.getMax();if(s>t||t>a){const e=this.inputRef.current;e&&e.reportValidity()}else{const n=t||0===t?t:o.default;this.isIntData()?i.setIntValue(r,n,e):i.setDoubleValue(r,n,e),this.setState({dirty:!1,value:n,formattedValue:this.formatValue(n)})}},this.onBlur=()=>{this.state.dirty&&this.commitWidgetValue({fromUi:!0})},this.onChange=e=>{const t=e.target.value;let n=null;n=this.isIntData()?parseInt(t,10):parseFloat(t),this.setState({dirty:!0,value:n,formattedValue:t})},this.onKeyDown=e=>{switch(e.key){case"ArrowUp":e.preventDefault(),this.modifyValueUsingStep("increment")();break;case"ArrowDown":e.preventDefault(),this.modifyValueUsingStep("decrement")()}},this.onKeyPress=e=>{"Enter"===e.key&&this.state.dirty&&this.commitWidgetValue({fromUi:!0})},this.modifyValueUsingStep=e=>()=>{const t=this.state.value,n=this.getStep(),r=this.getMin(),i=this.getMax();switch(e){case"increment":t+n<=i&&this.setState({dirty:!0,value:t+n},(()=>{this.commitWidgetValue({fromUi:!0})}));break;case"decrement":t-n>=r&&this.setState({dirty:!0,value:t-n},(()=>{this.commitWidgetValue({fromUi:!0})}))}},this.render=()=>{const e=this.props,t=e.element,n=e.width,r=e.disabled,i=this.state,s=i.formattedValue,a=i.dirty,c={width:n};return Object(w.jsxs)("div",{className:"stNumberInput",style:c,children:[Object(w.jsx)(d.b,{children:t.label}),t.help&&Object(w.jsx)(d.c,{children:Object(w.jsx)(l.a,{content:t.help,placement:u.a.TOP_RIGHT})}),Object(w.jsxs)(m,{children:[Object(w.jsx)(h.a,{type:"number",inputRef:this.inputRef,value:s,onBlur:this.onBlur,onChange:this.onChange,onKeyPress:this.onKeyPress,onKeyDown:this.onKeyDown,disabled:r,overrides:{Input:{props:{step:this.getStep(),min:this.getMin(),max:this.getMax()}},InputContainer:{style:()=>({borderTopRightRadius:0,borderBottomRightRadius:0})},Root:{style:()=>({borderTopRightRadius:0,borderBottomRightRadius:0})}}}),Object(w.jsxs)(g,{children:[Object(w.jsx)(j,{className:"step-down",onClick:this.modifyValueUsingStep("decrement"),children:Object(w.jsx)(p.a,{content:o.Minus,size:"xs"})}),Object(w.jsx)(j,{className:"step-up",onClick:this.modifyValueUsingStep("increment"),children:Object(w.jsx)(p.a,{content:o.Plus,size:"xs"})})]})]}),Object(w.jsx)(v,{children:Object(w.jsx)(f.a,{dirty:a,value:s,className:"input-instructions"})})]})},this.state={dirty:!1,value:this.initialValue,formattedValue:this.formatValue(this.initialValue)}}get initialValue(){const e=this.props.widgetMgr.getIntValue(this.props.element);return void 0!==e?e:this.props.element.default}componentDidMount(){this.commitWidgetValue({fromUi:!1})}}var O=x}}]);
//# sourceMappingURL=16.990fca8d.chunk.js.map