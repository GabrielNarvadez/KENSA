/**
* Theme: Reback - Responsive Bootstrap 5 Admin Dashboard
* Author: Techzaa
* Module/App: Theme Config Js
*/

class Config {

     //  Default Config Value (config value Change )
     constructor() {
          this.config = {
               theme: "light",             // ['light', 'dark']

               topbar: {
                    color: "light",       // ['light', 'dark']
               },

               menu: {
                    size: "sm-hover-active",   // [ 'default', sm-hover-active', 'condensed', 'full']
                    color: "light",            // ['light', 'dark']
               },
          };
          window.defaultConfig = this.config
     }

     setConfig() {
          let config = this.config;
          var savedConfig = localStorage.getItem("__REBACK_CONFIG__");
          // var savedConfig = sessionStorage.getItem("__REBACK_CONFIG__");

          let html = document.getElementsByTagName('html')[0];
          window.html = html;

          if (savedConfig !== null) {
               config = JSON.parse(savedConfig);
          }

          window.config = config;

          if (config) {
               html.setAttribute("data-bs-theme", config.theme);
               html.setAttribute("data-topbar-color", config.topbar.color);
               html.setAttribute("data-menu-color", config.menu.color);

               if (window.innerWidth <= 1140) {
                    html.setAttribute("data-menu-size", "hidden");
               } else {
                    html.setAttribute("data-menu-size", config.menu.size);
               }
          }
     }

     init() {
          try {
               this.setConfig();
          } catch (e) {
               localStorage.setItem('__REBACK_CONFIG__', JSON.stringify(this.config));
               this.setConfig();
          }
     }
}

new Config().init();