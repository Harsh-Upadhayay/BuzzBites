(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[834],{7166:function(e,t,n){Promise.resolve().then(n.bind(n,1597))},1597:function(e,t,n){"use strict";n.r(t),n.d(t,{default:function(){return d}});var a=n(7437),i=n(2265),s=n(5592),r=n(8721),l=n(9327),c=n(2160);let o=e=>"CB"===e?"Cricbuzz":"HT"===e?"Hindustan Times":"Unknown";function d(){let[e,t]=(0,i.useState)([]),[n,d]=(0,i.useState)(1),[u,m]=(0,i.useState)(!1),[h,f]=(0,i.useState)(!0);(0,i.useRef)(),(0,i.useEffect)(()=>{(async()=>{if(h&&!u){m(!0);try{let e=await fetch("/api/news/?page=".concat(n)),a=await e.json();if("Invalid page."===a.detail)f(!1);else{let e=a.results.map(e=>({...e,selectedRadio:"summary_en"}));t(t=>[...t,...e])}}catch(e){console.error("Error fetching data:",e)}m(!1)}})()},[n]),(0,i.useEffect)(()=>{let e=()=>{Math.ceil(window.innerHeight+window.scrollY)>=document.documentElement.scrollHeight&&!u&&d(e=>e+1)};return window.addEventListener("scroll",e),()=>{window.removeEventListener("scroll",e)}},[u]);let g=(e,n)=>{let{value:a}=e.target;t(e=>{let t=[...e];return t[n].selectedRadio=a,t})};return(0,a.jsxs)("div",{className:"",children:[(0,a.jsx)(s.d,{variant:"splitted",selectionMode:"multiple",className:"",children:e.map((e,t)=>(0,a.jsxs)(r.G,{"aria-label":"Accordion ".concat(e.id),title:e.title,subtitle:(0,a.jsx)("div",{dangerouslySetInnerHTML:{__html:"Published : ".concat(new Date(e.published_at).toLocaleString("en-US",{weekday:"long",year:"numeric",month:"long",day:"numeric"}),"<br>Source : ").concat(o(e.source))}}),children:[(0,a.jsxs)(l.X,{className:"mb-3",orientation:"horizontal",color:"warning",value:e.selectedRadio,onChange:e=>g(e,t),children:[(0,a.jsx)(c.J,{value:"summary_en",children:"Read in English"}),(0,a.jsx)(c.J,{value:"summary_hi",children:"Read in Hindi"})]}),"summary_en"===e.selectedRadio&&(0,a.jsx)("p",{className:"font-normal text-gray-900 dark:text-gray-400",children:e.summary}),"summary_hi"===e.selectedRadio&&(0,a.jsx)("p",{className:"font-normal text-gray-900 dark:text-gray-400",children:e.summary_hindi})]},e.id))}),u&&(0,a.jsx)("p",{children:"Loading..."}),!u&&!h&&(0,a.jsx)("p",{children:"End of News List"})]})}}},function(e){e.O(0,[212,358,663,971,69,744],function(){return e(e.s=7166)}),_N_E=e.O()}]);