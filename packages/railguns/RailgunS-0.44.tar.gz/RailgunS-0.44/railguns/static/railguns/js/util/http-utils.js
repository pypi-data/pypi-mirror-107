"use strict";axios.defaults.xsrfCookieName="csrftoken",axios.defaults.xsrfHeaderName="X-CSRFToken";var httpUtilrequest=function(s,t,r,o,n,e){var a="GET"===(s=s.toUpperCase());axios({method:s,url:t,params:a?r:{},data:a?{}:r}).then(function(e){var a=e.status;console.debug("%c".concat(s),c(s),"".concat(location.origin).concat(t),"✅",a,e.statusText),r&&r.password&&(r.password="******"),r&&console.debug("⬆️ 参数",JSON.stringify(r)),o&&o(a,e.data)}).catch(function(e){var a;if(e.response){var s=e.response.data;a=s?JSON.stringify(s):e.response.statusText}else a=e.request?e.request:e.message;console.error(a),n&&n(e.response.status,a)}).then(function(){e&&e()});var c=function(e){var a;switch(e){case"OPTIONS":case"GET":a="#248fb2";break;case"POST":a="#6bbd5b";break;case"PATCH":a="#e09d43";break;case"DELETE":a="#e27a7a";break;default:a="#9b708b"}return"background-color: ".concat(a,"; color: #fff; padding: 1px 9px; border-radius: 2px;")}};