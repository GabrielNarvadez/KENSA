/*
Template Name: Reback - Responsive 5 Admin Dashboard
Author: Techzaa
File: customer js
*/

class ECommerceCustomer {

    initMask() {
        document.querySelectorAll('[data-toggle="input-mask"]').forEach(e => {
            const maskFormat = e.getAttribute('data-mask-format').toString().replaceAll('0', '9');
            e.setAttribute("data-mask-format", maskFormat);
            const im = new Inputmask(maskFormat);
            im.mask(e);
        });
    }

    init() {
        new Wizard('#horizontalwizard');
        this.initMask();
    }

}

document.addEventListener('DOMContentLoaded', function (e) {
    new ECommerceCustomer().init();
});