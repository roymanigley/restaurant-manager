import{b as n}from"./chunk-MZ4LUD7G.js";import{j as i,s as o}from"./chunk-ZVRC6D75.js";var m=(()=>{class t extends n{getBaseUrl(){return"/api/staff/items"}addImage(e,a){let r=new FormData;return r.append("image",a,a.name),this.http.post(`${this.getBaseUrl()}/${e}/image/`,r)}static{this.\u0275fac=(()=>{let e;return function(r){return(e||(e=o(t)))(r||t)}})()}static{this.\u0275prov=i({token:t,factory:t.\u0275fac,providedIn:"root"})}}return t})();export{m as a};
