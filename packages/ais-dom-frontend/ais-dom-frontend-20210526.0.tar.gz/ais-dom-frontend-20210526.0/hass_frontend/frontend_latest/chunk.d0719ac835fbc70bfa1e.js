/*! For license information please see chunk.d0719ac835fbc70bfa1e.js.LICENSE.txt */
(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[7891,9995],{18601:(t,i,e)=>{"use strict";e.d(i,{qN:()=>n.q,Wg:()=>o});var n=e(78220);class o extends n.H{click(){this.formElement&&(this.formElement.focus(),this.formElement.click())}setAriaLabel(t){this.formElement&&this.formElement.setAttribute("aria-label",t)}firstUpdated(){super.firstUpdated(),this.shadowRoot&&this.mdcRoot.addEventListener("change",(t=>{this.dispatchEvent(new Event("change",t))}))}}o.shadowRootOptions={mode:"open",delegatesFocus:!0}},43453:(t,i,e)=>{"use strict";e.d(i,{Y:()=>s});e(65233);var n=/\.splices$/,o=/\.length$/,a=/\.?#?([0-9]+)$/;const s={properties:{data:{type:Object,notify:!0,value:function(){return this.zeroValue}},sequentialTransactions:{type:Boolean,value:!1},log:{type:Boolean,value:!1}},observers:["__dataChanged(data.*)"],created:function(){this.__initialized=!1,this.__syncingToMemory=!1,this.__initializingStoredValue=null,this.__transactionQueueAdvances=Promise.resolve()},ready:function(){this._initializeStoredValue()},get isNew(){return!0},get transactionsComplete(){return this.__transactionQueueAdvances},get zeroValue(){},saveValue:function(t){return Promise.resolve()},reset:function(){},destroy:function(){return this.data=this.zeroValue,this.saveValue()},initializeStoredValue:function(){return this.isNew?Promise.resolve():this._getStoredValue("data").then(function(t){if(this._log("Got stored value!",t,this.data),null==t)return this._setStoredValue("data",this.data||this.zeroValue);this.syncToMemory((function(){this.set("data",t)}))}.bind(this))},getStoredValue:function(t){return Promise.resolve()},setStoredValue:function(t,i){return Promise.resolve(i)},memoryPathToStoragePath:function(t){return t},storagePathToMemoryPath:function(t){return t},syncToMemory:function(t){this.__syncingToMemory||(this._group("Sync to memory."),this.__syncingToMemory=!0,t.call(this),this.__syncingToMemory=!1,this._groupEnd("Sync to memory."))},valueIsEmpty:function(t){return Array.isArray(t)?0===t.length:Object.prototype.isPrototypeOf(t)?0===Object.keys(t).length:null==t},_getStoredValue:function(t){return this.getStoredValue(this.memoryPathToStoragePath(t))},_setStoredValue:function(t,i){return this.setStoredValue(this.memoryPathToStoragePath(t),i)},_enqueueTransaction:function(t){if(this.sequentialTransactions)t=t.bind(this);else{var i=t.call(this);t=function(){return i}}return this.__transactionQueueAdvances=this.__transactionQueueAdvances.then(t).catch(function(t){this._error("Error performing queued transaction.",t)}.bind(this))},_log:function(...t){this.log&&console.log.apply(console,t)},_error:function(...t){this.log&&console.error.apply(console,t)},_group:function(...t){this.log&&console.group.apply(console,t)},_groupEnd:function(...t){this.log&&console.groupEnd.apply(console,t)},_initializeStoredValue:function(){if(!this.__initializingStoredValue){this._group("Initializing stored value.");var t=this.__initializingStoredValue=this.initializeStoredValue().then(function(){this.__initialized=!0,this.__initializingStoredValue=null,this._groupEnd("Initializing stored value.")}.bind(this)).catch(function(t){this.__initializingStoredValue=null,this._groupEnd("Initializing stored value.")}.bind(this));return this._enqueueTransaction((function(){return t}))}},__dataChanged:function(t){if(!this.isNew&&!this.__syncingToMemory&&this.__initialized&&!this.__pathCanBeIgnored(t.path)){var i=this.__normalizeMemoryPath(t.path),e=t.value,n=e&&e.indexSplices;this._enqueueTransaction((function(){return this._log("Setting",i+":",n||e),n&&this.__pathIsSplices(i)&&(i=this.__parentPath(i),e=this.get(i)),this._setStoredValue(i,e)}))}},__normalizeMemoryPath:function(t){for(var i=t.split("."),e=[],n=[],o=[],a=0;a<i.length;++a)n.push(i[a]),/^#/.test(i[a])?o.push(this.get(e).indexOf(this.get(n))):o.push(i[a]),e.push(i[a]);return o.join(".")},__parentPath:function(t){var i=t.split(".");return i.slice(0,i.length-1).join(".")},__pathCanBeIgnored:function(t){return o.test(t)&&Array.isArray(this.get(this.__parentPath(t)))},__pathIsSplices:function(t){return n.test(t)&&Array.isArray(this.get(this.__parentPath(t)))},__pathRefersToArray:function(t){return(n.test(t)||o.test(t))&&Array.isArray(this.get(this.__parentPath(t)))},__pathTailToIndex:function(t){var i=t.split(".").pop();return window.parseInt(i.replace(a,"$1"),10)}}},33760:(t,i,e)=>{"use strict";e.d(i,{U:()=>a});e(65233);var n=e(51644),o=e(26110);const a=[n.P,o.a,{hostAttributes:{role:"option",tabindex:"0"}}]},89194:(t,i,e)=>{"use strict";e(65233),e(65660),e(70019);var n=e(9672),o=e(50856);(0,n.k)({_template:o.d`
    <style>
      :host {
        overflow: hidden; /* needed for text-overflow: ellipsis to work on ff */
        @apply --layout-vertical;
        @apply --layout-center-justified;
        @apply --layout-flex;
      }

      :host([two-line]) {
        min-height: var(--paper-item-body-two-line-min-height, 72px);
      }

      :host([three-line]) {
        min-height: var(--paper-item-body-three-line-min-height, 88px);
      }

      :host > ::slotted(*) {
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }

      :host > ::slotted([secondary]) {
        @apply --paper-font-body1;

        color: var(--paper-item-body-secondary-color, var(--secondary-text-color));

        @apply --paper-item-body-secondary;
      }
    </style>

    <slot></slot>
`,is:"paper-item-body"})},97968:(t,i,e)=>{"use strict";e(65660),e(70019);const n=document.createElement("template");n.setAttribute("style","display: none;"),n.innerHTML="<dom-module id=\"paper-item-shared-styles\">\n  <template>\n    <style>\n      :host, .paper-item {\n        display: block;\n        position: relative;\n        min-height: var(--paper-item-min-height, 48px);\n        padding: 0px 16px;\n      }\n\n      .paper-item {\n        @apply --paper-font-subhead;\n        border:none;\n        outline: none;\n        background: white;\n        width: 100%;\n        text-align: left;\n      }\n\n      :host([hidden]), .paper-item[hidden] {\n        display: none !important;\n      }\n\n      :host(.iron-selected), .paper-item.iron-selected {\n        font-weight: var(--paper-item-selected-weight, bold);\n\n        @apply --paper-item-selected;\n      }\n\n      :host([disabled]), .paper-item[disabled] {\n        color: var(--paper-item-disabled-color, var(--disabled-text-color));\n\n        @apply --paper-item-disabled;\n      }\n\n      :host(:focus), .paper-item:focus {\n        position: relative;\n        outline: 0;\n\n        @apply --paper-item-focused;\n      }\n\n      :host(:focus):before, .paper-item:focus:before {\n        @apply --layout-fit;\n\n        background: currentColor;\n        content: '';\n        opacity: var(--dark-divider-opacity);\n        pointer-events: none;\n\n        @apply --paper-item-focused-before;\n      }\n    </style>\n  </template>\n</dom-module>",document.head.appendChild(n.content)},53973:(t,i,e)=>{"use strict";e(65233),e(65660),e(97968);var n=e(9672),o=e(50856),a=e(33760);(0,n.k)({_template:o.d`
    <style include="paper-item-shared-styles">
      :host {
        @apply --layout-horizontal;
        @apply --layout-center;
        @apply --paper-font-subhead;

        @apply --paper-item;
      }
    </style>
    <slot></slot>
`,is:"paper-item",behaviors:[a.U]})},54444:(t,i,e)=>{"use strict";e(65233);var n=e(9672),o=e(87156),a=e(50856);(0,n.k)({_template:a.d`
    <style>
      :host {
        display: block;
        position: absolute;
        outline: none;
        z-index: 1002;
        -moz-user-select: none;
        -ms-user-select: none;
        -webkit-user-select: none;
        user-select: none;
        cursor: default;
      }

      #tooltip {
        display: block;
        outline: none;
        @apply --paper-font-common-base;
        font-size: 10px;
        line-height: 1;
        background-color: var(--paper-tooltip-background, #616161);
        color: var(--paper-tooltip-text-color, white);
        padding: 8px;
        border-radius: 2px;
        @apply --paper-tooltip;
      }

      @keyframes keyFrameScaleUp {
        0% {
          transform: scale(0.0);
        }
        100% {
          transform: scale(1.0);
        }
      }

      @keyframes keyFrameScaleDown {
        0% {
          transform: scale(1.0);
        }
        100% {
          transform: scale(0.0);
        }
      }

      @keyframes keyFrameFadeInOpacity {
        0% {
          opacity: 0;
        }
        100% {
          opacity: var(--paper-tooltip-opacity, 0.9);
        }
      }

      @keyframes keyFrameFadeOutOpacity {
        0% {
          opacity: var(--paper-tooltip-opacity, 0.9);
        }
        100% {
          opacity: 0;
        }
      }

      @keyframes keyFrameSlideDownIn {
        0% {
          transform: translateY(-2000px);
          opacity: 0;
        }
        10% {
          opacity: 0.2;
        }
        100% {
          transform: translateY(0);
          opacity: var(--paper-tooltip-opacity, 0.9);
        }
      }

      @keyframes keyFrameSlideDownOut {
        0% {
          transform: translateY(0);
          opacity: var(--paper-tooltip-opacity, 0.9);
        }
        10% {
          opacity: 0.2;
        }
        100% {
          transform: translateY(-2000px);
          opacity: 0;
        }
      }

      .fade-in-animation {
        opacity: 0;
        animation-delay: var(--paper-tooltip-delay-in, 500ms);
        animation-name: keyFrameFadeInOpacity;
        animation-iteration-count: 1;
        animation-timing-function: ease-in;
        animation-duration: var(--paper-tooltip-duration-in, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .fade-out-animation {
        opacity: var(--paper-tooltip-opacity, 0.9);
        animation-delay: var(--paper-tooltip-delay-out, 0ms);
        animation-name: keyFrameFadeOutOpacity;
        animation-iteration-count: 1;
        animation-timing-function: ease-in;
        animation-duration: var(--paper-tooltip-duration-out, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .scale-up-animation {
        transform: scale(0);
        opacity: var(--paper-tooltip-opacity, 0.9);
        animation-delay: var(--paper-tooltip-delay-in, 500ms);
        animation-name: keyFrameScaleUp;
        animation-iteration-count: 1;
        animation-timing-function: ease-in;
        animation-duration: var(--paper-tooltip-duration-in, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .scale-down-animation {
        transform: scale(1);
        opacity: var(--paper-tooltip-opacity, 0.9);
        animation-delay: var(--paper-tooltip-delay-out, 500ms);
        animation-name: keyFrameScaleDown;
        animation-iteration-count: 1;
        animation-timing-function: ease-in;
        animation-duration: var(--paper-tooltip-duration-out, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .slide-down-animation {
        transform: translateY(-2000px);
        opacity: 0;
        animation-delay: var(--paper-tooltip-delay-out, 500ms);
        animation-name: keyFrameSlideDownIn;
        animation-iteration-count: 1;
        animation-timing-function: cubic-bezier(0.0, 0.0, 0.2, 1);
        animation-duration: var(--paper-tooltip-duration-out, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .slide-down-animation-out {
        transform: translateY(0);
        opacity: var(--paper-tooltip-opacity, 0.9);
        animation-delay: var(--paper-tooltip-delay-out, 500ms);
        animation-name: keyFrameSlideDownOut;
        animation-iteration-count: 1;
        animation-timing-function: cubic-bezier(0.4, 0.0, 1, 1);
        animation-duration: var(--paper-tooltip-duration-out, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .cancel-animation {
        animation-delay: -30s !important;
      }

      /* Thanks IE 10. */

      .hidden {
        display: none !important;
      }
    </style>

    <div id="tooltip" class="hidden">
      <slot></slot>
    </div>
`,is:"paper-tooltip",hostAttributes:{role:"tooltip",tabindex:-1},properties:{for:{type:String,observer:"_findTarget"},manualMode:{type:Boolean,value:!1,observer:"_manualModeChanged"},position:{type:String,value:"bottom"},fitToVisibleBounds:{type:Boolean,value:!1},offset:{type:Number,value:14},marginTop:{type:Number,value:14},animationDelay:{type:Number,value:500,observer:"_delayChange"},animationEntry:{type:String,value:""},animationExit:{type:String,value:""},animationConfig:{type:Object,value:function(){return{entry:[{name:"fade-in-animation",node:this,timing:{delay:0}}],exit:[{name:"fade-out-animation",node:this}]}}},_showing:{type:Boolean,value:!1}},listeners:{webkitAnimationEnd:"_onAnimationEnd"},get target(){var t=(0,o.vz)(this).parentNode,i=(0,o.vz)(this).getOwnerRoot();return this.for?(0,o.vz)(i).querySelector("#"+this.for):t.nodeType==Node.DOCUMENT_FRAGMENT_NODE?i.host:t},attached:function(){this._findTarget()},detached:function(){this.manualMode||this._removeListeners()},playAnimation:function(t){"entry"===t?this.show():"exit"===t&&this.hide()},cancelAnimation:function(){this.$.tooltip.classList.add("cancel-animation")},show:function(){if(!this._showing){if(""===(0,o.vz)(this).textContent.trim()){for(var t=!0,i=(0,o.vz)(this).getEffectiveChildNodes(),e=0;e<i.length;e++)if(""!==i[e].textContent.trim()){t=!1;break}if(t)return}this._showing=!0,this.$.tooltip.classList.remove("hidden"),this.$.tooltip.classList.remove("cancel-animation"),this.$.tooltip.classList.remove(this._getAnimationType("exit")),this.updatePosition(),this._animationPlaying=!0,this.$.tooltip.classList.add(this._getAnimationType("entry"))}},hide:function(){if(this._showing){if(this._animationPlaying)return this._showing=!1,void this._cancelAnimation();this._onAnimationFinish(),this._showing=!1,this._animationPlaying=!0}},updatePosition:function(){if(this._target&&this.offsetParent){var t=this.offset;14!=this.marginTop&&14==this.offset&&(t=this.marginTop);var i,e,n=this.offsetParent.getBoundingClientRect(),o=this._target.getBoundingClientRect(),a=this.getBoundingClientRect(),s=(o.width-a.width)/2,r=(o.height-a.height)/2,l=o.left-n.left,p=o.top-n.top;switch(this.position){case"top":i=l+s,e=p-a.height-t;break;case"bottom":i=l+s,e=p+o.height+t;break;case"left":i=l-a.width-t,e=p+r;break;case"right":i=l+o.width+t,e=p+r}this.fitToVisibleBounds?(n.left+i+a.width>window.innerWidth?(this.style.right="0px",this.style.left="auto"):(this.style.left=Math.max(0,i)+"px",this.style.right="auto"),n.top+e+a.height>window.innerHeight?(this.style.bottom=n.height-p+t+"px",this.style.top="auto"):(this.style.top=Math.max(-n.top,e)+"px",this.style.bottom="auto")):(this.style.left=i+"px",this.style.top=e+"px")}},_addListeners:function(){this._target&&(this.listen(this._target,"mouseenter","show"),this.listen(this._target,"focus","show"),this.listen(this._target,"mouseleave","hide"),this.listen(this._target,"blur","hide"),this.listen(this._target,"tap","hide")),this.listen(this.$.tooltip,"animationend","_onAnimationEnd"),this.listen(this,"mouseenter","hide")},_findTarget:function(){this.manualMode||this._removeListeners(),this._target=this.target,this.manualMode||this._addListeners()},_delayChange:function(t){500!==t&&this.updateStyles({"--paper-tooltip-delay-in":t+"ms"})},_manualModeChanged:function(){this.manualMode?this._removeListeners():this._addListeners()},_cancelAnimation:function(){this.$.tooltip.classList.remove(this._getAnimationType("entry")),this.$.tooltip.classList.remove(this._getAnimationType("exit")),this.$.tooltip.classList.remove("cancel-animation"),this.$.tooltip.classList.add("hidden")},_onAnimationFinish:function(){this._showing&&(this.$.tooltip.classList.remove(this._getAnimationType("entry")),this.$.tooltip.classList.remove("cancel-animation"),this.$.tooltip.classList.add(this._getAnimationType("exit")))},_onAnimationEnd:function(){this._animationPlaying=!1,this._showing||(this.$.tooltip.classList.remove(this._getAnimationType("exit")),this.$.tooltip.classList.add("hidden"))},_getAnimationType:function(t){if("entry"===t&&""!==this.animationEntry)return this.animationEntry;if("exit"===t&&""!==this.animationExit)return this.animationExit;if(this.animationConfig[t]&&"string"==typeof this.animationConfig[t][0].name){if(this.animationConfig[t][0].timing&&this.animationConfig[t][0].timing.delay&&0!==this.animationConfig[t][0].timing.delay){var i=this.animationConfig[t][0].timing.delay;"entry"===t?this.updateStyles({"--paper-tooltip-delay-in":i+"ms"}):"exit"===t&&this.updateStyles({"--paper-tooltip-delay-out":i+"ms"})}return this.animationConfig[t][0].name}},_removeListeners:function(){this._target&&(this.unlisten(this._target,"mouseenter","show"),this.unlisten(this._target,"focus","show"),this.unlisten(this._target,"mouseleave","hide"),this.unlisten(this._target,"blur","hide"),this.unlisten(this._target,"tap","hide")),this.unlisten(this.$.tooltip,"animationend","_onAnimationEnd"),this.unlisten(this,"mouseenter","hide")}})},78389:(t,i,e)=>{"use strict";e.d(i,{s:()=>u});var n=e(99602),o=e(55122),a=e(57724);const s=(t,i)=>{var e,n;const o=t.N;if(void 0===o)return!1;for(const t of o)null===(n=(e=t).O)||void 0===n||n.call(e,i,!1),s(t,i);return!0},r=t=>{let i,e;do{if(void 0===(i=t.M))break;e=i.N,e.delete(t),t=i}while(0===(null==e?void 0:e.size))},l=t=>{for(let i;i=t.M;t=i){let e=i.N;if(void 0===e)i.N=e=new Set;else if(e.has(t))break;e.add(t),d(i)}};function p(t){void 0!==this.N?(r(this),this.M=t,l(this)):this.M=t}function h(t,i=!1,e=0){const n=this.H,o=this.N;if(void 0!==o&&0!==o.size)if(i)if(Array.isArray(n))for(let t=e;t<n.length;t++)s(n[t],!1),r(n[t]);else null!=n&&(s(n,!1),r(n));else s(this,t)}const d=t=>{var i,e,n,a;t.type==o.pX.CHILD&&(null!==(i=(n=t).P)&&void 0!==i||(n.P=h),null!==(e=(a=t).Q)&&void 0!==e||(a.Q=p))};class u extends o.Xe{constructor(){super(...arguments),this.isConnected=!0,this.ut=n.Jb,this.N=void 0}T(t,i,e){super.T(t,i,e),l(this)}O(t,i=!0){this.at(t),i&&(s(this,t),r(this))}at(t){var i,e;t!==this.isConnected&&(t?(this.isConnected=!0,this.ut!==n.Jb&&(this.setValue(this.ut),this.ut=n.Jb),null===(i=this.reconnected)||void 0===i||i.call(this)):(this.isConnected=!1,null===(e=this.disconnected)||void 0===e||e.call(this)))}S(t,i){if(!this.isConnected)throw Error(`AsyncDirective ${this.constructor.name} was rendered while its tree was disconnected.`);return super.S(t,i)}setValue(t){if(this.isConnected)if((0,a.OR)(this.Σdt))this.Σdt.I(t,this);else{const i=[...this.Σdt.H];i[this.Σct]=t,this.Σdt.I(i,this,0)}else this.ut=t}disconnected(){}reconnected(){}}},57724:(t,i,e)=>{"use strict";e.d(i,{E_:()=>y,i9:()=>c,_Y:()=>p,pt:()=>a,OR:()=>r,hN:()=>s,ws:()=>m,fk:()=>h,hl:()=>u});var n=e(99602);const{et:o}=n.Vm,a=t=>null===t||"object"!=typeof t&&"function"!=typeof t,s=(t,i)=>{var e,n;return void 0===i?void 0!==(null===(e=t)||void 0===e?void 0:e._$litType$):(null===(n=t)||void 0===n?void 0:n._$litType$)===i},r=t=>void 0===t.strings,l=()=>document.createComment(""),p=(t,i,e)=>{var n;const a=t.A.parentNode,s=void 0===i?t.B:i.A;if(void 0===e){const i=a.insertBefore(l(),s),n=a.insertBefore(l(),s);e=new o(i,n,t,t.options)}else{const i=e.B.nextSibling,o=e.M!==t;if(o&&(null===(n=e.Q)||void 0===n||n.call(e,t),e.M=t),i!==s||o){let t=e.A;for(;t!==i;){const i=t.nextSibling;a.insertBefore(t,s),t=i}}}return e},h=(t,i,e=t)=>(t.I(i,e),t),d={},u=(t,i=d)=>t.H=i,c=t=>t.H,m=t=>{var i;null===(i=t.P)||void 0===i||i.call(t,!1,!0);let e=t.A;const n=t.B.nextSibling;for(;e!==n;){const t=e.nextSibling;e.remove(),e=t}},y=t=>{t.R()}},19967:(t,i,e)=>{"use strict";e.d(i,{Xe:()=>n.Xe,pX:()=>n.pX,XM:()=>n.XM});var n=e(55122)},76666:(t,i,e)=>{"use strict";e.d(i,{$:()=>n.$});var n=e(81471)},82816:(t,i,e)=>{"use strict";e.d(i,{o:()=>n.o});var n=e(49629)},92483:(t,i,e)=>{"use strict";e.d(i,{V:()=>n.V});var n=e(79865)}}]);
//# sourceMappingURL=chunk.d0719ac835fbc70bfa1e.js.map