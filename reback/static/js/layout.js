/**
* Theme: Reback - Responsive Bootstrap 5 Admin Dashboard
* Author: Techzaa
* Module/App: Theme Layout Customizer Js
*/

class ThemeLayout {

     constructor() {
          this.html = document.getElementsByTagName('html')[0]
          this.config = window.config;
     }

     // Main Nav
     initVerticalMenu() {
          const navCollapse = document.querySelectorAll('.navbar-nav li .collapse');
          const navToggle = document.querySelectorAll(".navbar-nav li [data-bs-toggle='collapse']");

          navToggle.forEach(toggle => {
               toggle.addEventListener('click', function (e) {
                    e.preventDefault();
               });
          });

          // open one menu at a time only (Auto Close Menu)
          navCollapse.forEach(collapse => {
               collapse.addEventListener('show.bs.collapse', function (event) {
                    const parent = event.target.closest('.collapse.show');
                    document.querySelectorAll('.navbar-nav .collapse.show').forEach(element => {
                         if (element !== event.target && element !== parent) {
                              const collapseInstance = new bootstrap.Collapse(element);
                              collapseInstance.hide();
                         }
                    });
               });
          });


          if (document.querySelector(".navbar-nav")) {
               // Activate the menu in left side bar based on url
               document.querySelectorAll(".navbar-nav a").forEach(function (link) {
                    var pageUrl = window.location.href.split(/[?#]/)[0];

                    if (link.href === pageUrl) {
                         link.classList.add("active");
                         link.parentNode.classList.add("active");

                         let parentCollapseDiv = link.closest(".collapse");
                         while (parentCollapseDiv) {
                              parentCollapseDiv.classList.add("show");
                              parentCollapseDiv.parentElement.children[0].classList.add("active");
                              parentCollapseDiv.parentElement.children[0].setAttribute("aria-expanded", "true");
                              parentCollapseDiv = parentCollapseDiv.parentElement.closest(".collapse");
                         }
                    }
               });

               setTimeout(function () {
                    var activatedItem = document.querySelector('.nav-item li a.active');

                    if (activatedItem != null) {
                         var simplebarContent = document.querySelector('.main-nav .simplebar-content-wrapper');
                         var offset = activatedItem.offsetTop - 300;
                         if (simplebarContent && offset > 100) {
                              scrollTo(simplebarContent, offset, 600);
                         }
                    }
               }, 200);

               // scrollTo (Left Side Bar Active Menu)
               function easeInOutQuad(t, b, c, d) {
                    t /= d / 2;
                    if (t < 1) return c / 2 * t * t + b;
                    t--;
                    return -c / 2 * (t * (t - 2) - 1) + b;
               }

               function scrollTo(element, to, duration) {
                    var start = element.scrollTop, change = to - start, currentTime = 0, increment = 20;
                    var animateScroll = function () {
                         currentTime += increment;
                         var val = easeInOutQuad(currentTime, start, change, duration);
                         element.scrollTop = val;
                         if (currentTime < duration) {
                              setTimeout(animateScroll, increment);
                         }
                    };
                    animateScroll();
               }
          }
     }

     initConfig() {
          this.config = JSON.parse(JSON.stringify(window.config));
          this.setSwitchFromConfig();
     }

     changeMenuColor(color) {
          this.config.menu.color = color;
          this.html.setAttribute('data-menu-color', color);
          this.setSwitchFromConfig();
     }

     changeMenuSize(size, save = true) {
          this.html.setAttribute('data-menu-size', size);
          if (save) {
               this.config.menu.size = size;
               this.setSwitchFromConfig();
          }
     }

     changeThemeMode(color) {
          this.config.theme = color;
          this.html.setAttribute('data-bs-theme', color);
          this.setSwitchFromConfig();
     }

     changeTopbarColor(color) {
          this.config.topbar.color = color;
          this.html.setAttribute('data-topbar-color', color);
          this.setSwitchFromConfig();
     }

     resetTheme() {
          this.config = JSON.parse(JSON.stringify(window.defaultConfig));
          this.changeMenuColor(this.config.menu.color);
          this.changeMenuSize(this.config.menu.size);
          this.changeThemeMode(this.config.theme);
          this.changeTopbarColor(this.config.topbar.color);
     }

     initSwitchListener() {
          var self = this;
          document.querySelectorAll('input[name=data-menu-color]').forEach(function (element) {
               element.addEventListener('change', function (e) {
                    self.changeMenuColor(element.value);
               })
          });

          document.querySelectorAll('input[name=data-menu-size]').forEach(function (element) {
               element.addEventListener('change', function (e) {
                    self.changeMenuSize(element.value);
               })
          });

          document.querySelectorAll('input[name=data-bs-theme]').forEach(function (element) {
               element.addEventListener('change', function (e) {
                    self.changeThemeMode(element.value);
               })
          });

          document.querySelectorAll('input[name=data-topbar-color]').forEach(function (element) {
               element.addEventListener('change', function (e) {
                    self.changeTopbarColor(element.value);
               })
          });

          //TopBar Light Dark
          var themeColorToggle = document.getElementById('light-dark-mode');
          if (themeColorToggle) {
               themeColorToggle.addEventListener('click', function (e) {
                    if (self.config.theme === 'light') {
                         self.changeThemeMode('dark');
                    } else {
                         self.changeThemeMode('light');
                    }
               });
          }

          var resetBtn = document.querySelector('#reset-layout')
          if (resetBtn) {
               resetBtn.addEventListener('click', function (e) {
                    self.resetTheme();
               });
          }

          var menuToggleBtn = document.querySelector('.button-toggle-menu');
          if (menuToggleBtn) {
               menuToggleBtn.addEventListener('click', function () {
                    var configSize = self.config.menu.size;
                    var size = self.html.getAttribute('data-menu-size', configSize);

                    if (size !== 'hidden') {
                         if (size === 'condensed') {
                              self.changeMenuSize(configSize == 'condensed' ? 'default' : configSize, false);
                         } else {
                              self.changeMenuSize('condensed', false);
                         }
                    } else {
                         self.showBackdrop();
                    }

                    // Todo: old implementation
                    self.html.classList.toggle('sidebar-enable');
               });
          }

          var hoverBtn = document.querySelectorAll('.button-sm-hover');
          hoverBtn.forEach(function (element) {
               element.addEventListener('click', function () {
                    var configSize = self.config.menu.size;
                    var size = self.html.getAttribute('data-menu-size', configSize);

                    if (configSize === 'sm-hover-active') {
                         if (size === 'sm-hover-active') {
                              self.changeMenuSize('sm-hover', true);
                         } else {
                              self.changeMenuSize('sm-hover-active', true);
                         }
                    }

                    if (configSize === 'sm-hover') {
                         if (size === 'sm-hover') {
                              self.changeMenuSize('sm-hover-active', true);
                         } else {
                              self.changeMenuSize('sm-hover', true);
                         }
                    }
               });
          })
     }

     showBackdrop() {
          const backdrop = document.createElement('div');
          backdrop.classList = 'offcanvas-backdrop fade show';
          document.body.appendChild(backdrop);
          document.body.style.overflow = "hidden";
          if (window.innerWidth > 1040) {
               document.body.style.paddingRight = "15px";
          }
          const self = this
          backdrop.addEventListener('click', function (e) {
               self.html.classList.remove('sidebar-enable');
               document.body.removeChild(backdrop);
               document.body.style.overflow = null;
               document.body.style.paddingRight = null;
          })
     }

     initWindowSize() {
          var self = this;
          window.addEventListener('resize', function (e) {
               self._adjustLayout();
          })
     }

     _adjustLayout() {
          var self = this;

          if (window.innerWidth <= 1140) {
               self.changeMenuSize('hidden', false);
          } else {
               self.changeMenuSize(self.config.menu.size);
               // self.changeLayoutMode(self.config.layout.mode);
          }
     }

     setSwitchFromConfig() {

          localStorage.setItem('__REBACK_CONFIG__', JSON.stringify(this.config));
          // sessionStorage.setItem('__REBACK_CONFIG__', JSON.stringify(this.config));

          document.querySelectorAll('.settings-bar input[type=radio]').forEach(function (checkbox) {
               checkbox.checked = false;
          })

          var config = this.config;
          if (config) {
               var layoutColorSwitch = document.querySelector('input[type=radio][name=data-bs-theme][value=' + config.theme + ']');
               var topbarColorSwitch = document.querySelector('input[type=radio][name=data-topbar-color][value=' + config.topbar.color + ']');
               var leftbarSizeSwitch = document.querySelector('input[type=radio][name=data-menu-size][value=' + config.menu.size + ']');
               var leftbarColorSwitch = document.querySelector('input[type=radio][name=data-menu-color][value=' + config.menu.color + ']');

               if (layoutColorSwitch) layoutColorSwitch.checked = true;
               if (topbarColorSwitch) topbarColorSwitch.checked = true;
               if (leftbarSizeSwitch) leftbarSizeSwitch.checked = true;
               if (leftbarColorSwitch) leftbarColorSwitch.checked = true;
          }
     }

     init() {
          this.initVerticalMenu();
          this.initConfig();
          this.initSwitchListener();
          this.initWindowSize();
          this._adjustLayout();
          this.setSwitchFromConfig();
     }
}

new ThemeLayout().init();