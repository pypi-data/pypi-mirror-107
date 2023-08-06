/*! For license information please see chunk.91415572192f9bf336a5.js.LICENSE.txt */
(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[2445],{49075:(t,e,i)=>{"use strict";i.d(e,{S:()=>o,B:()=>a});i(65233);var s=i(51644),n=i(26110),r=i(84938);const o={observers:["_focusedChanged(receivedFocusFromKeyboard)"],_focusedChanged:function(t){t&&this.ensureRipple(),this.hasRipple()&&(this._ripple.holdDown=t)},_createRipple:function(){var t=r.o._createRipple();return t.id="ink",t.setAttribute("center",""),t.classList.add("circle"),t}},a=[s.P,n.a,r.o,o]},84938:(t,e,i)=>{"use strict";i.d(e,{o:()=>r});i(65233),i(60748);var s=i(51644),n=i(87156);const r={properties:{noink:{type:Boolean,observer:"_noinkChanged"},_rippleContainer:{type:Object}},_buttonStateChanged:function(){this.focused&&this.ensureRipple()},_downHandler:function(t){s.$._downHandler.call(this,t),this.pressed&&this.ensureRipple(t)},ensureRipple:function(t){if(!this.hasRipple()){this._ripple=this._createRipple(),this._ripple.noink=this.noink;var e=this._rippleContainer||this.root;if(e&&(0,n.vz)(e).appendChild(this._ripple),t){var i=(0,n.vz)(this._rippleContainer||this),s=(0,n.vz)(t).rootTarget;i.deepContains(s)&&this._ripple.uiDownAction(t)}}},getRipple:function(){return this.ensureRipple(),this._ripple},hasRipple:function(){return Boolean(this._ripple)},_createRipple:function(){return document.createElement("paper-ripple")},_noinkChanged:function(t){this.hasRipple()&&(this._ripple.noink=t)}}},32333:(t,e,i)=>{"use strict";var s=i(55704);class n extends s.oi{static get properties(){return{value:{type:Number},high:{type:Number},low:{type:Number},min:{type:Number},max:{type:Number},step:{type:Number},startAngle:{type:Number},arcLength:{type:Number},handleSize:{type:Number},handleZoom:{type:Number},readonly:{type:Boolean},disabled:{type:Boolean},dragging:{type:Boolean,reflect:!0},rtl:{type:Boolean},_scale:{type:Number},valueLabel:{type:String},lowLabel:{type:String},highLabel:{type:String}}}constructor(){super(),this.min=0,this.max=100,this.step=1,this.startAngle=135,this.arcLength=270,this.handleSize=6,this.handleZoom=1.5,this.readonly=!1,this.disabled=!1,this.dragging=!1,this.rtl=!1,this._scale=1,this.attachedListeners=!1}get _start(){return this.startAngle*Math.PI/180}get _len(){return Math.min(this.arcLength*Math.PI/180,2*Math.PI-.01)}get _end(){return this._start+this._len}get _showHandle(){return!this.readonly&&(null!=this.value||null!=this.high&&null!=this.low)}_angleInside(t){let e=(this.startAngle+this.arcLength/2-t+180+360)%360-180;return e<this.arcLength/2&&e>-this.arcLength/2}_angle2xy(t){return this.rtl?{x:-Math.cos(t),y:Math.sin(t)}:{x:Math.cos(t),y:Math.sin(t)}}_xy2angle(t,e){return this.rtl&&(t=-t),(Math.atan2(e,t)-this._start+2*Math.PI)%(2*Math.PI)}_value2angle(t){const e=((t=Math.min(this.max,Math.max(this.min,t)))-this.min)/(this.max-this.min);return this._start+e*this._len}_angle2value(t){return Math.round((t/this._len*(this.max-this.min)+this.min)/this.step)*this.step}get _boundaries(){const t=this._angle2xy(this._start),e=this._angle2xy(this._end);let i=1;this._angleInside(270)||(i=Math.max(-t.y,-e.y));let s=1;this._angleInside(90)||(s=Math.max(t.y,e.y));let n=1;this._angleInside(180)||(n=Math.max(-t.x,-e.x));let r=1;return this._angleInside(0)||(r=Math.max(t.x,e.x)),{up:i,down:s,left:n,right:r,height:i+s,width:n+r}}_mouse2value(t){const e=t.type.startsWith("touch")?t.touches[0].clientX:t.clientX,i=t.type.startsWith("touch")?t.touches[0].clientY:t.clientY,s=this.shadowRoot.querySelector("svg").getBoundingClientRect(),n=this._boundaries,r=e-(s.left+n.left*s.width/n.width),o=i-(s.top+n.up*s.height/n.height),a=this._xy2angle(r,o);return this._angle2value(a)}dragStart(t){if(!this._showHandle||this.disabled)return;let e,i=t.target;if(this._rotation&&"focus"!==this._rotation.type)return;if(i.classList.contains("shadowpath"))if("touchstart"===t.type&&(e=window.setTimeout((()=>{this._rotation&&(this._rotation.cooldown=void 0)}),200)),null==this.low)i=this.shadowRoot.querySelector("#value");else{const e=this._mouse2value(t);i=Math.abs(e-this.low)<Math.abs(e-this.high)?this.shadowRoot.querySelector("#low"):this.shadowRoot.querySelector("#high")}if(i.classList.contains("overflow")&&(i=i.nextElementSibling),!i.classList.contains("handle"))return;i.setAttribute("stroke-width",2*this.handleSize*this.handleZoom*this._scale);const s="high"===i.id?this.low:this.min,n="low"===i.id?this.high:this.max;this._rotation={handle:i,min:s,max:n,start:this[i.id],type:t.type,cooldown:e},this.dragging=!0}_cleanupRotation(){const t=this._rotation.handle;t.setAttribute("stroke-width",2*this.handleSize*this._scale),this._rotation=!1,this.dragging=!1,t.blur()}dragEnd(t){if(!this._showHandle||this.disabled)return;if(!this._rotation)return;const e=this._rotation.handle;this._cleanupRotation();let i=new CustomEvent("value-changed",{detail:{[e.id]:this[e.id]},bubbles:!0,composed:!0});this.dispatchEvent(i),this.low&&this.low>=.99*this.max?this._reverseOrder=!0:this._reverseOrder=!1}drag(t){if(!this._showHandle||this.disabled)return;if(!this._rotation)return;if(this._rotation.cooldown)return window.clearTimeout(this._rotation.coldown),void this._cleanupRotation();if("focus"===this._rotation.type)return;t.preventDefault();const e=this._mouse2value(t);this._dragpos(e)}_dragpos(t){if(t<this._rotation.min||t>this._rotation.max)return;const e=this._rotation.handle;this[e.id]=t;let i=new CustomEvent("value-changing",{detail:{[e.id]:t},bubbles:!0,composed:!0});this.dispatchEvent(i)}_keyStep(t){if(!this._showHandle||this.disabled)return;if(!this._rotation)return;const e=this._rotation.handle;"ArrowLeft"!==t.key&&"ArrowDown"!==t.key||(t.preventDefault(),this.rtl?this._dragpos(this[e.id]+this.step):this._dragpos(this[e.id]-this.step)),"ArrowRight"!==t.key&&"ArrowUp"!==t.key||(t.preventDefault(),this.rtl?this._dragpos(this[e.id]-this.step):this._dragpos(this[e.id]+this.step)),"Home"===t.key&&(t.preventDefault(),this._dragpos(this.min)),"End"===t.key&&(t.preventDefault(),this._dragpos(this.max))}firstUpdated(){document.addEventListener("mouseup",this.dragEnd.bind(this)),document.addEventListener("touchend",this.dragEnd.bind(this),{passive:!1}),document.addEventListener("mousemove",this.drag.bind(this)),document.addEventListener("touchmove",this.drag.bind(this),{passive:!1}),document.addEventListener("keydown",this._keyStep.bind(this))}updated(t){if(this.shadowRoot.querySelector(".slider")){const t=window.getComputedStyle(this.shadowRoot.querySelector(".slider"));if(t&&t.strokeWidth){const e=parseFloat(t.strokeWidth);if(e>this.handleSize*this.handleZoom){const t=this._boundaries,i=`\n          ${e/2*Math.abs(t.up)}px\n          ${e/2*Math.abs(t.right)}px\n          ${e/2*Math.abs(t.down)}px\n          ${e/2*Math.abs(t.left)}px`;this.shadowRoot.querySelector("svg").style.margin=i}}}if(this.shadowRoot.querySelector("svg")&&void 0===this.shadowRoot.querySelector("svg").style.vectorEffect){t.has("_scale")&&1!=this._scale&&this.shadowRoot.querySelector("svg").querySelectorAll("path").forEach((t=>{if(t.getAttribute("stroke-width"))return;const e=parseFloat(getComputedStyle(t).getPropertyValue("stroke-width"));t.style.strokeWidth=e*this._scale+"px"}));const e=this.shadowRoot.querySelector("svg").getBoundingClientRect(),i=Math.max(e.width,e.height);this._scale=2/i}}_renderArc(t,e){const i=e-t;return t=this._angle2xy(t),e=this._angle2xy(e+.001),`\n      M ${t.x} ${t.y}\n      A 1 1,\n        0,\n        ${i>Math.PI?"1":"0"} ${this.rtl?"0":"1"},\n        ${e.x} ${e.y}\n    `}_renderHandle(t){const e=this._value2angle(this[t]),i=this._angle2xy(e),n={value:this.valueLabel,low:this.lowLabel,high:this.highLabel}[t]||"";return s.YP`
      <g class="${t} handle">
        <path
          id=${t}
          class="overflow"
          d="
          M ${i.x} ${i.y}
          L ${i.x+.001} ${i.y+.001}
          "
          vector-effect="non-scaling-stroke"
          stroke="rgba(0,0,0,0)"
          stroke-width="${4*this.handleSize*this._scale}"
          />
        <path
          id=${t}
          class="handle"
          d="
          M ${i.x} ${i.y}
          L ${i.x+.001} ${i.y+.001}
          "
          vector-effect="non-scaling-stroke"
          stroke-width="${2*this.handleSize*this._scale}"
          tabindex="0"
          @focus=${this.dragStart}
          @blur=${this.dragEnd}
          role="slider"
          aria-valuemin=${this.min}
          aria-valuemax=${this.max}
          aria-valuenow=${this[t]}
          aria-disabled=${this.disabled}
          aria-label=${n||""}
          />
        </g>
      `}render(){const t=this._boundaries;return s.dy`
      <svg
        @mousedown=${this.dragStart}
        @touchstart=${this.dragStart}
        xmln="http://www.w3.org/2000/svg"
        viewBox="${-t.left} ${-t.up} ${t.width} ${t.height}"
        style="margin: ${this.handleSize*this.handleZoom}px;"
        ?disabled=${this.disabled}
        focusable="false"
      >
        <g class="slider">
          <path
            class="path"
            d=${this._renderArc(this._start,this._end)}
            vector-effect="non-scaling-stroke"
          />
          <path
            class="bar"
            vector-effect="non-scaling-stroke"
            d=${this._renderArc(this._value2angle(null!=this.low?this.low:this.min),this._value2angle(null!=this.high?this.high:this.value))}
          />
          <path
            class="shadowpath"
            d=${this._renderArc(this._start,this._end)}
            vector-effect="non-scaling-stroke"
            stroke="rgba(0,0,0,0)"
            stroke-width="${3*this.handleSize*this._scale}"
            stroke-linecap="butt"
          />

        </g>

        <g class="handles">
        ${this._showHandle?null!=this.low?this._reverseOrder?s.dy`${this._renderHandle("high")} ${this._renderHandle("low")}`:s.dy`${this._renderHandle("low")} ${this._renderHandle("high")}`:s.dy`${this._renderHandle("value")}`:""}
        </g>
      </svg>
    `}static get styles(){return s.iv`
      :host {
        display: inline-block;
        width: 100%;
      }
      svg {
        overflow: visible;
        display: block;
      }
      path {
        transition: stroke 1s ease-out, stroke-width 200ms ease-out;
      }
      .slider {
        fill: none;
        stroke-width: var(--round-slider-path-width, 3);
        stroke-linecap: var(--round-slider-linecap, round);
      }
      .path {
        stroke: var(--round-slider-path-color, lightgray);
      }
      .bar {
        stroke: var(--round-slider-bar-color, deepskyblue);
      }
      svg[disabled] .bar {
        stroke: var(--round-slider-disabled-bar-color, darkgray);
      }
      g.handles {
        stroke: var(--round-slider-handle-color, var(--round-slider-bar-color, deepskyblue));
        stroke-linecap: round;
        cursor: var(--round-slider-handle-cursor, pointer);
      }
      g.low.handle {
        stroke: var(--round-slider-low-handle-color);
      }
      g.high.handle {
        stroke: var(--round-slider-high-handle-color);
      }
      svg[disabled] g.handles {
        stroke: var(--round-slider-disabled-bar-color, darkgray);
      }
      .handle:focus {
        outline: unset;
      }
    `}}customElements.define("round-slider",n)},68928:(t,e,i)=>{"use strict";i.d(e,{WU:()=>k});var s=/d{1,4}|M{1,4}|YY(?:YY)?|S{1,3}|Do|ZZ|Z|([HhMsDm])\1?|[aA]|"[^"]*"|'[^']*'/g,n="[1-9]\\d?",r="\\d\\d",o="[^\\s]+",a=/\[([^]*?)\]/gm;function h(t,e){for(var i=[],s=0,n=t.length;s<n;s++)i.push(t[s].substr(0,e));return i}var l=function(t){return function(e,i){var s=i[t].map((function(t){return t.toLowerCase()})).indexOf(e.toLowerCase());return s>-1?s:null}};function d(t){for(var e=[],i=1;i<arguments.length;i++)e[i-1]=arguments[i];for(var s=0,n=e;s<n.length;s++){var r=n[s];for(var o in r)t[o]=r[o]}return t}var u=["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],c=["January","February","March","April","May","June","July","August","September","October","November","December"],g=h(c,3),p={dayNamesShort:h(u,3),dayNames:u,monthNamesShort:g,monthNames:c,amPm:["am","pm"],DoFn:function(t){return t+["th","st","nd","rd"][t%10>3?0:(t-t%10!=10?1:0)*t%10]}},f=d({},p),m=function(t,e){for(void 0===e&&(e=2),t=String(t);t.length<e;)t="0"+t;return t},v={D:function(t){return String(t.getDate())},DD:function(t){return m(t.getDate())},Do:function(t,e){return e.DoFn(t.getDate())},d:function(t){return String(t.getDay())},dd:function(t){return m(t.getDay())},ddd:function(t,e){return e.dayNamesShort[t.getDay()]},dddd:function(t,e){return e.dayNames[t.getDay()]},M:function(t){return String(t.getMonth()+1)},MM:function(t){return m(t.getMonth()+1)},MMM:function(t,e){return e.monthNamesShort[t.getMonth()]},MMMM:function(t,e){return e.monthNames[t.getMonth()]},YY:function(t){return m(String(t.getFullYear()),4).substr(2)},YYYY:function(t){return m(t.getFullYear(),4)},h:function(t){return String(t.getHours()%12||12)},hh:function(t){return m(t.getHours()%12||12)},H:function(t){return String(t.getHours())},HH:function(t){return m(t.getHours())},m:function(t){return String(t.getMinutes())},mm:function(t){return m(t.getMinutes())},s:function(t){return String(t.getSeconds())},ss:function(t){return m(t.getSeconds())},S:function(t){return String(Math.round(t.getMilliseconds()/100))},SS:function(t){return m(Math.round(t.getMilliseconds()/10),2)},SSS:function(t){return m(t.getMilliseconds(),3)},a:function(t,e){return t.getHours()<12?e.amPm[0]:e.amPm[1]},A:function(t,e){return t.getHours()<12?e.amPm[0].toUpperCase():e.amPm[1].toUpperCase()},ZZ:function(t){var e=t.getTimezoneOffset();return(e>0?"-":"+")+m(100*Math.floor(Math.abs(e)/60)+Math.abs(e)%60,4)},Z:function(t){var e=t.getTimezoneOffset();return(e>0?"-":"+")+m(Math.floor(Math.abs(e)/60),2)+":"+m(Math.abs(e)%60,2)}},_=function(t){return+t-1},y=[null,n],b=[null,o],w=["isPm",o,function(t,e){var i=t.toLowerCase();return i===e.amPm[0]?0:i===e.amPm[1]?1:null}],M=["timezoneOffset","[^\\s]*?[\\+\\-]\\d\\d:?\\d\\d|[^\\s]*?Z?",function(t){var e=(t+"").match(/([+-]|\d\d)/gi);if(e){var i=60*+e[1]+parseInt(e[2],10);return"+"===e[0]?i:-i}return 0}],S=(l("monthNamesShort"),l("monthNames"),{default:"ddd MMM DD YYYY HH:mm:ss",shortDate:"M/D/YY",mediumDate:"MMM D, YYYY",longDate:"MMMM D, YYYY",fullDate:"dddd, MMMM D, YYYY",isoDate:"YYYY-MM-DD",isoDateTime:"YYYY-MM-DDTHH:mm:ssZ",shortTime:"HH:mm",mediumTime:"HH:mm:ss",longTime:"HH:mm:ss.SSS"}),k=function(t,e,i){if(void 0===e&&(e=S.default),void 0===i&&(i={}),"number"==typeof t&&(t=new Date(t)),"[object Date]"!==Object.prototype.toString.call(t)||isNaN(t.getTime()))throw new Error("Invalid Date pass to format");var n=[];e=(e=S[e]||e).replace(a,(function(t,e){return n.push(e),"@@@"}));var r=d(d({},f),i);return(e=e.replace(s,(function(e){return v[e](t,r)}))).replace(/@@@/g,(function(){return n.shift()}))}},78389:(t,e,i)=>{"use strict";i.d(e,{s:()=>c});var s=i(99602),n=i(55122),r=i(57724);const o=(t,e)=>{var i,s;const n=t.N;if(void 0===n)return!1;for(const t of n)null===(s=(i=t).O)||void 0===s||s.call(i,e,!1),o(t,e);return!0},a=t=>{let e,i;do{if(void 0===(e=t.M))break;i=e.N,i.delete(t),t=e}while(0===(null==i?void 0:i.size))},h=t=>{for(let e;e=t.M;t=e){let i=e.N;if(void 0===i)e.N=i=new Set;else if(i.has(t))break;i.add(t),u(e)}};function l(t){void 0!==this.N?(a(this),this.M=t,h(this)):this.M=t}function d(t,e=!1,i=0){const s=this.H,n=this.N;if(void 0!==n&&0!==n.size)if(e)if(Array.isArray(s))for(let t=i;t<s.length;t++)o(s[t],!1),a(s[t]);else null!=s&&(o(s,!1),a(s));else o(this,t)}const u=t=>{var e,i,s,r;t.type==n.pX.CHILD&&(null!==(e=(s=t).P)&&void 0!==e||(s.P=d),null!==(i=(r=t).Q)&&void 0!==i||(r.Q=l))};class c extends n.Xe{constructor(){super(...arguments),this.isConnected=!0,this.ut=s.Jb,this.N=void 0}T(t,e,i){super.T(t,e,i),h(this)}O(t,e=!0){this.at(t),e&&(o(this,t),a(this))}at(t){var e,i;t!==this.isConnected&&(t?(this.isConnected=!0,this.ut!==s.Jb&&(this.setValue(this.ut),this.ut=s.Jb),null===(e=this.reconnected)||void 0===e||e.call(this)):(this.isConnected=!1,null===(i=this.disconnected)||void 0===i||i.call(this)))}S(t,e){if(!this.isConnected)throw Error(`AsyncDirective ${this.constructor.name} was rendered while its tree was disconnected.`);return super.S(t,e)}setValue(t){if(this.isConnected)if((0,r.OR)(this.Σdt))this.Σdt.I(t,this);else{const e=[...this.Σdt.H];e[this.Σct]=t,this.Σdt.I(e,this,0)}else this.ut=t}disconnected(){}reconnected(){}}},57724:(t,e,i)=>{"use strict";i.d(e,{E_:()=>f,i9:()=>g,_Y:()=>l,pt:()=>r,OR:()=>a,hN:()=>o,ws:()=>p,fk:()=>d,hl:()=>c});var s=i(99602);const{et:n}=s.Vm,r=t=>null===t||"object"!=typeof t&&"function"!=typeof t,o=(t,e)=>{var i,s;return void 0===e?void 0!==(null===(i=t)||void 0===i?void 0:i._$litType$):(null===(s=t)||void 0===s?void 0:s._$litType$)===e},a=t=>void 0===t.strings,h=()=>document.createComment(""),l=(t,e,i)=>{var s;const r=t.A.parentNode,o=void 0===e?t.B:e.A;if(void 0===i){const e=r.insertBefore(h(),o),s=r.insertBefore(h(),o);i=new n(e,s,t,t.options)}else{const e=i.B.nextSibling,n=i.M!==t;if(n&&(null===(s=i.Q)||void 0===s||s.call(i,t),i.M=t),e!==o||n){let t=i.A;for(;t!==e;){const e=t.nextSibling;r.insertBefore(t,o),t=e}}}return i},d=(t,e,i=t)=>(t.I(e,i),t),u={},c=(t,e=u)=>t.H=e,g=t=>t.H,p=t=>{var e;null===(e=t.P)||void 0===e||e.call(t,!1,!0);let i=t.A;const s=t.B.nextSibling;for(;i!==s;){const t=i.nextSibling;i.remove(),i=t}},f=t=>{t.R()}},11716:(t,e,i)=>{"use strict";i.d(e,{C:()=>h});var s=i(99602),n=i(55122),r=i(57724),o=i(78389);const a=t=>!(0,r.pt)(t)&&"function"==typeof t.then,h=(0,n.XM)(class extends o.s{constructor(){super(...arguments),this.Ct=2147483647,this.Rt=[]}render(...t){var e;return null!==(e=t.find((t=>!a(t))))&&void 0!==e?e:s.Jb}update(t,e){const i=this.Rt;let n=i.length;this.Rt=e;for(let t=0;t<e.length&&!(t>this.Ct);t++){const s=e[t];if(!a(s))return this.Ct=t,s;t<n&&s===i[t]||(this.Ct=2147483647,n=0,Promise.resolve(s).then((t=>{const e=this.Rt.indexOf(s);e>-1&&e<this.Ct&&(this.Ct=e,this.setValue(t))})))}return s.Jb}})}}]);
//# sourceMappingURL=chunk.91415572192f9bf336a5.js.map