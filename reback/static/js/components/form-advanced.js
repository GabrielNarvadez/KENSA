/*
Template Name: Reback - Responsive 5 Admin Dashboard
Author: Techzaa
File: form - Advanced js
*/

class FormAdvanced {

    initSelect2() {
        document.querySelectorAll('[data-toggle="select2"]').forEach(function (element) {

            if (element.multiple) {
                new Choices(element, {
                    itemSelectText: '',
                    placeholderValue: 'select',
                    placeholder: true,
                    removeItemButton: true,
                    removeItems: true,
                    choices: [{value: 'select', label: "Select", selected: true}]
                }).setChoiceByValue('select');
            } else {
                new Choices(element, {
                    itemSelectText: '',
                    placeholderValue: 'select',
                    placeholder: true,
                    removeItemButton: false,
                    removeItems: false,

                }).setChoiceByValue('aselect');
            }


            document.querySelectorAll('.choices__group .choices__heading').forEach(function (element) {
                element.innerHTML == "" ? element.parentElement.classList.add('d-none') : null;
            });


        });
    }

    init() {
        this.initSelect2();
    }

}

document.addEventListener('DOMContentLoaded', function (e) {
    new FormAdvanced().init();
});
