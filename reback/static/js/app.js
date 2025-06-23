/**
* Theme: Reback - Responsive Bootstrap 5 Admin Dashboard
* Author: Techzaa
* Module/App: Main Js
*/

// Components
class Components {
    initBootstrapComponents() {

        // Popovers
        const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]')
        const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl))

        // Tooltips
        const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
        const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))

        // offcanvas
        const offcanvasElementList = document.querySelectorAll('.offcanvas')
        const offcanvasList = [...offcanvasElementList].map(offcanvasEl => new bootstrap.Offcanvas(offcanvasEl))

        //Toasts
        var toastPlacement = document.getElementById("toastPlacement");
        if (toastPlacement) {
            document.getElementById("selectToastPlacement").addEventListener("change", function () {
                if (!toastPlacement.dataset.originalClass) {
                    toastPlacement.dataset.originalClass = toastPlacement.className;
                }
                toastPlacement.className = toastPlacement.dataset.originalClass + " " + this.value;
            });
        }

        var toastElList = [].slice.call(document.querySelectorAll('.toast'))
        var toastList = toastElList.map(function (toastEl) {
            return new bootstrap.Toast(toastEl)
        })


        const alertTrigger = document.getElementById('liveAlertBtn')
        if (alertTrigger) {
            alertTrigger.addEventListener('click', () => {
                alert('Nice, you triggered this alert message!', 'success')
            })
        }

    }

    initfullScreenListener() {
        var fullScreenBtn = document.querySelector('[data-toggle="fullscreen"]');

        if (fullScreenBtn) {
            fullScreenBtn.addEventListener('click', function (e) {
                e.preventDefault();
                document.body.classList.toggle('fullscreen-enable')
                if (!document.fullscreenElement && /* alternative standard method */ !document.mozFullScreenElement && !document.webkitFullscreenElement) {
                    // current working methods
                    if (document.documentElement.requestFullscreen) {
                        document.documentElement.requestFullscreen();
                    } else if (document.documentElement.mozRequestFullScreen) {
                        document.documentElement.mozRequestFullScreen();
                    } else if (document.documentElement.webkitRequestFullscreen) {
                        document.documentElement.webkitRequestFullscreen(Element.ALLOW_KEYBOARD_INPUT);
                    }
                } else {
                    if (document.cancelFullScreen) {
                        document.cancelFullScreen();
                    } else if (document.mozCancelFullScreen) {
                        document.mozCancelFullScreen();
                    } else if (document.webkitCancelFullScreen) {
                        document.webkitCancelFullScreen();
                    }
                }
            });
        }
    }

    // App Search
    initAppSearch() {
        this.searchOption = document.getElementById('search-options');
        this.searchDropdown = document.getElementById('search-dropdown');
        this.searchClose = document.getElementById('search-close-options');
        const self = this;
        if (this.searchOption) {
            ['focus', 'keyup'].forEach(function (event) {
                self.searchOption.addEventListener(event, function (e) {
                    if (self.searchOption.value.length > 0) {
                        self.searchDropdown.classList.add('show');
                        self.searchClose.classList.remove('d-none');
                    } else {
                        self.searchDropdown.classList.remove('show');
                        self.searchClose.classList.add('d-none');
                    }
                })
            })
        }
        if (self.searchClose) {
            self.searchClose.addEventListener('click', function () {
                self.searchDropdown.classList.remove('show');
                self.searchClose.classList.add('d-none');
                self.searchOption.value = "";
            });
        }
    }

    // Counter Number
    initCounter() {
        var counter = document.querySelectorAll(".counter-value");
        var speed = 250; // The lower the slower
        counter &&
            counter.forEach(function (counter_value) {
                function updateCount() {
                    var target = +counter_value.getAttribute("data-target");
                    var count = +counter_value.innerText;
                    var inc = target / speed;
                    if (inc < 1) {
                        inc = 1;
                    }
                    // Check if target is reached
                    if (count < target) {
                        // Add inc to count and output in counter_value
                        counter_value.innerText = (count + inc).toFixed(0);
                        // Call function every ms
                        setTimeout(updateCount, 1);
                    } else {
                        counter_value.innerText = numberWithCommas(target);
                    }
                    numberWithCommas(counter_value.innerText);
                }
                updateCount();
            });

        function numberWithCommas(x) {
            return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        }
    }

    init() {
        this.initBootstrapComponents();
        this.initfullScreenListener();
        this.initAppSearch();
        this.initCounter();
    }
}

// Form Validation ( Bootstrap )
class FormValidation {
    initFormValidation() {
        // Example starter JavaScript for disabling form submissions if there are invalid fields
        // Fetch all the forms we want to apply custom Bootstrap validation styles to
        // Loop over them and prevent submission
        document.querySelectorAll('.needs-validation').forEach(form => {
            form.addEventListener('submit', event => {
                if (!form.checkValidity()) {
                    event.preventDefault()
                    event.stopPropagation()
                }

                form.classList.add('was-validated')
            }, false)
        })
    }

    init() {
        this.initFormValidation();
    }
}

//  Form Advanced
class FormAdvanced {

    initMask() {
        document.querySelectorAll('[data-toggle="input-mask"]').forEach(e => {
            const maskFormat = e.getAttribute('data-mask-format').toString().replaceAll('0', '9');
            e.setAttribute("data-mask-format", maskFormat);
            const im = new Inputmask(maskFormat);
            im.mask(e);
        });
    }

    // Choices Select plugin
    initFormChoices() {
        var choicesExamples = document.querySelectorAll("[data-choices]");
        choicesExamples.forEach(function (item) {
            var choiceData = {};
            var isChoicesVal = item.attributes;
            if (isChoicesVal["data-choices-groups"]) {
                choiceData.placeholderValue = "This is a placeholder set in the config";
            }
            if (isChoicesVal["data-choices-search-false"]) {
                choiceData.searchEnabled = false;
            }
            if (isChoicesVal["data-choices-search-true"]) {
                choiceData.searchEnabled = true;
            }
            if (isChoicesVal["data-choices-removeItem"]) {
                choiceData.removeItemButton = true;
            }
            if (isChoicesVal["data-choices-sorting-false"]) {
                choiceData.shouldSort = false;
            }
            if (isChoicesVal["data-choices-sorting-true"]) {
                choiceData.shouldSort = true;
            }
            if (isChoicesVal["data-choices-multiple-remove"]) {
                choiceData.removeItemButton = true;
            }
            if (isChoicesVal["data-choices-limit"]) {
                choiceData.maxItemCount = isChoicesVal["data-choices-limit"].value.toString();
            }
            if (isChoicesVal["data-choices-limit"]) {
                choiceData.maxItemCount = isChoicesVal["data-choices-limit"].value.toString();
            }
            if (isChoicesVal["data-choices-editItem-true"]) {
                choiceData.maxItemCount = true;
            }
            if (isChoicesVal["data-choices-editItem-false"]) {
                choiceData.maxItemCount = false;
            }
            if (isChoicesVal["data-choices-text-unique-true"]) {
                choiceData.duplicateItemsAllowed = false;
                choiceData.paste = false;
            }
            if (isChoicesVal["data-choices-text-disabled-true"]) {
                choiceData.addItems = false;
            }
            isChoicesVal["data-choices-text-disabled-true"] ? new Choices(item, choiceData).disable() : new Choices(item, choiceData);
        });
    }

    init() {
        this.initMask();
        this.initFormChoices();
    }

}

// Card Portlet
class Portlet {
    constructor() {
        this.portletIdentifier = ".card";
        this.portletCloser = '.card a[data-toggle="remove"]';
        this.portletRefresher = '.card a[data-toggle="reload"]'
    }

    initCloser() {
        const self = this;
        document.querySelectorAll(this.portletCloser).forEach(element => {
            element.addEventListener('click', function (e) {
                e.preventDefault();
                const portlet = element.closest(self.portletIdentifier);
                const portlet_parent = portlet?.parentElement;
                if (portlet) portlet.remove();
                if (portlet_parent?.children.length === 0) portlet_parent?.remove();
                self.init();
            });
        });
    }

    initRefresher() {
        const self = this;
        const elements = document.querySelectorAll(this.portletRefresher);
        elements.forEach(function (element) {
            element.addEventListener('click', function (e) {
                e.preventDefault();
                const portlet = element.closest(self.portletIdentifier);
                if (portlet) portlet.innerHTML += ('<div class="card-disabled"><div class="card-portlets-loader"></div></div>');
                let pd;
                portlet?.children.forEach(element => {
                    if (element.classList.contains('card-disabled')) pd = element;
                });
                setTimeout(function () {
                    pd?.remove();
                    self.init();
                }, 500 + 300 * (Math.random() * 5));
            })
        });
    }

    init = () => {
        this.initRefresher();
        this.initCloser();
    }
}

// Code Highlight and Copy ( Clipboard ) and Components nav Link Active
class Code {

    initCode() {

        let elements = document.querySelectorAll('.highlight');

        if (elements && elements.length > 0) {
            for (var i = 0; i < elements.length; ++i) {
                var highlight = elements[i];
                var copy = highlight.querySelector('.btn-copy-clipboard');

                if (copy) {
                    var clipboard = new ClipboardJS(copy, {
                        target: function (trigger) {
                            var highlight = trigger.closest('.highlight');
                            var el = highlight.querySelector('.tab-pane.active');

                            if (el == null) {
                                el = highlight.querySelector('.code');
                            }

                            return el;
                        }
                    });

                    clipboard.on('success', function (e) {
                        var caption = e.trigger.innerHTML;

                        e.trigger.innerHTML = 'Copied';
                        e.clearSelection();

                        setTimeout(function () {
                            e.trigger.innerHTML = caption;
                        }, 2000);
                    });
                }
            }
        }

        Prism.plugins.NormalizeWhitespace.setDefaults({
            'remove-trailing': true,
            'remove-indent': true,
            'left-trim': true,
            'right-trim': true,
        });

        // Gumshoe (Link Active)
        if (document.querySelector('.docs-nav a')) {
            new Gumshoe('.docs-nav a');
        }

    }

    init() {
        this.initCode();
    }
}

// Dragula (Draggable Components)
class Dragula {

    initDragula() {

        document.querySelectorAll("[data-plugin=dragula]")

            .forEach(function (element) {

                const containersIds = JSON.parse(element.getAttribute('data-containers'));
                let containers = [];
                if (containersIds) {
                    for (let i = 0; i < containersIds.length; i++) {
                        containers.push(document.querySelectorAll("#" + containersIds[i])[0]);
                    }
                } else {
                    containers = [element];
                }

                // if handle provided
                const handleClass = element.getAttribute('data-handleclass');

                // init dragula
                if (handleClass) {
                    dragula(containers, {
                        moves: function (el, container, handle) {
                            return handle.classList.contains(handleClass);
                        }
                    });
                } else {
                    dragula(containers);
                }

            });

    }

    init() {
        this.initDragula();
    }


}

// Swiper Slider
class SwiperSlider {
    initSwiperSlider() {

        //Default Swiper
        var swiper = new Swiper("[data-swiper='default']", {
            loop: true,
            autoplay: {
                delay: 2500,
                disableOnInteraction: false,
            },
        });

        //Navigation Swiper
        var swiper = new Swiper("[data-swiper='navigation']", {
            loop: true,
            autoplay: {
                delay: 2500,
                disableOnInteraction: false,
            },
            navigation: {
                nextEl: ".swiper-button-next",
                prevEl: ".swiper-button-prev",
            },
            pagination: {
                clickable: true,
                el: ".swiper-pagination",
            },
        });

        //Pagination Dynamic Swiper
        var swiper = new Swiper("[data-swiper='dynamic']", {
            loop: true,
            autoplay: {
                delay: 2500,
                disableOnInteraction: false,
            },
            pagination: {
                clickable: true,
                el: ".swiper-pagination",
                dynamicBullets: true,
            },
        });

        // Pagination fraction Swiper
        var swiper = new Swiper("[data-swiper='fraction']", {
            loop: true,
            autoplay: {
                delay: 2500,
                disableOnInteraction: false,
            },
            pagination: {
                clickable: true,
                el: ".swiper-pagination",
                type: "fraction",
            },
            navigation: {
                nextEl: ".swiper-button-next",
                prevEl: ".swiper-button-prev",
            },
        });

        // Pagination Custom Swiper
        var swiper = new Swiper("[data-swiper='custom']", {
            loop: true,
            autoplay: {
                delay: 2500,
                disableOnInteraction: false,
            },
            pagination: {
                clickable: true,
                el: ".swiper-pagination",
                renderBullet: function (index, className) {
                    return '<span class="' + className + '">' + (index + 1) + "</span>";
                },
            }
        });

        // Pagination Progress Swiper
        var swiper = new Swiper("[data-swiper='progress']", {
            loop: true,
            autoplay: {
                delay: 2500,
                disableOnInteraction: false,
            },
            pagination: {
                el: ".swiper-pagination",
                type: "progressbar",
            },
            navigation: {
                nextEl: ".swiper-button-next",
                prevEl: ".swiper-button-prev",
            },
        });

        // Scrollbar Swiper
        var swiper = new Swiper("[data-swiper='scrollbar']", {
            loop: true,
            autoplay: {
                delay: 2500,
                disableOnInteraction: false,
            },
            scrollbar: {
                el: ".swiper-scrollbar",
                hide: true,
            },
            navigation: {
                nextEl: ".swiper-button-next",
                prevEl: ".swiper-button-prev",
            }
        });

        // Vertical Swiper
        var swiper = new Swiper("[data-swiper='vertical']", {
            loop: true,
            direction: "vertical",
            autoplay: {
                delay: 2500,
                disableOnInteraction: false,
            },
            pagination: {
                el: ".swiper-pagination",
                clickable: true,
            },
        });

        // Mousewheel Control Swiper
        var swiper = new Swiper("[data-swiper='mousewheel']", {
            loop: true,
            direction: "vertical",
            mousewheel: true,
            autoplay: {
                delay: 2500,
                disableOnInteraction: false,
            },
            pagination: {
                el: ".swiper-pagination",
                clickable: true,
            },
        });

        // Effect Fade Swiper
        var swiper = new Swiper("[data-swiper='effect-fade']", {
            loop: true,
            effect: "fade",
            autoplay: {
                delay: 2500,
                disableOnInteraction: false,
            },
            pagination: {
                el: ".swiper-pagination",
                clickable: true,
            },
        });

        // Effect Coverflow Swiper
        var swiper = new Swiper("[data-swiper='coverflow']", {
            loop: true,
            effect: "coverflow",
            grabCursor: true,
            centeredSlides: true,
            slidesPerView: "4",
            coverflowEffect: {
                rotate: 50,
                stretch: 0,
                depth: 100,
                modifier: 1,
                slideShadows: true,
            },
            autoplay: {
                delay: 2500,
                disableOnInteraction: false,
            },
            pagination: {
                el: ".swiper-pagination",
                clickable: true,
                dynamicBullets: true,
            },
        });

        // Effect Flip Swiper
        var swiper = new Swiper("[data-swiper='flip']", {
            loop: true,
            effect: "flip",
            grabCursor: true,
            autoplay: {
                delay: 2500,
                disableOnInteraction: false,
            },
            pagination: {
                el: ".swiper-pagination",
                clickable: true,
            },
        });

        // Effect Creative Swiper
        var swiper = new Swiper("[data-swiper='creative']", {
            loop: true,
            grabCursor: true,
            effect: "creative",
            creativeEffect: {
                prev: {
                    shadow: true,
                    translate: [0, 0, -400],
                },
                next: {
                    translate: ["100%", 0, 0],
                },
            },
            autoplay: {
                delay: 2500,
                disableOnInteraction: false,
            },
            pagination: {
                el: ".swiper-pagination",
                clickable: true,
            },
        });

        // Responsive Swiper
        var swiper = new Swiper("[data-swiper='responsive']", {
            loop: true,
            slidesPerView: 1,
            spaceBetween: 10,
            pagination: {
                el: ".swiper-pagination",
                clickable: true,
            },
            breakpoints: {
                768: {
                    slidesPerView: 2,
                    spaceBetween: 40,
                },
                1200: {
                    slidesPerView: 3,
                    spaceBetween: 50,
                },
            },
        });
    }

    init() {
        this.initSwiperSlider();
    }
}

// Toast Notification
class ToastNotification {
    initToastNotification() {

        document.querySelectorAll("[data-toast]").forEach(function (element) {
            element.addEventListener("click", function () {
                var toastData = {};
                if (element.attributes["data-toast-text"]) {
                    toastData.text = element.attributes["data-toast-text"].value.toString();
                }
                if (element.attributes["data-toast-gravity"]) {
                    toastData.gravity = element.attributes["data-toast-gravity"].value.toString();
                }
                if (element.attributes["data-toast-position"]) {
                    toastData.position = element.attributes["data-toast-position"].value.toString();
                }
                if (element.attributes["data-toast-className"]) {
                    toastData.className = element.attributes["data-toast-className"].value.toString();
                }
                if (element.attributes["data-toast-duration"]) {
                    toastData.duration = element.attributes["data-toast-duration"].value.toString();
                }
                if (element.attributes["data-toast-close"]) {
                    toastData.close = element.attributes["data-toast-close"].value.toString();
                }
                if (element.attributes["data-toast-style"]) {
                    toastData.style = element.attributes["data-toast-style"].value.toString();
                }
                if (element.attributes["data-toast-offset"]) {
                    toastData.offset = element.attributes["data-toast-offset"];
                }
                Toastify({
                    newWindow: true,
                    text: toastData.text,
                    gravity: toastData.gravity,
                    position: toastData.position,
                    className: "bg-" + toastData.className,
                    stopOnFocus: true,
                    offset: {
                        x: toastData.offset ? 50 : 0, // horizontal axis - can be a number or a string indicating unity. eg: '2em'
                        y: toastData.offset ? 10 : 0, // vertical axis - can be a number or a string indicating unity. eg: '2em'
                    },
                    duration: toastData.duration,
                    close: toastData.close == "close" ? true : false,
                }).showToast();
            });
        });
    }

    init() {
        this.initToastNotification();
    }
}

document.addEventListener('DOMContentLoaded', function (e) {
    new Components().init();
    new FormValidation().init();
    new FormAdvanced().init();
    new Portlet().init();
    new Code().init();
    new Dragula().init();
    new SwiperSlider().init();
    new ToastNotification().init();
});

