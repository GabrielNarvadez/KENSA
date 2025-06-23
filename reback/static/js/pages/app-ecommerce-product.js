/*
Template Name: Reback - Responsive 5 Admin Dashboard
Author: Techzaa
File: product js
*/

class EcommerceProduct {

    constructor() {
        this.body = document.getElementsByTagName("body")[0];
        this.window = window;
    }

    initEditors() {

        if (document.getElementById('bubble-editor')) {
            new Quill('#bubble-editor', {
                theme: 'bubble'
            });
        }
        if (document.getElementById('snow-editor')) {
            new Quill('#snow-editor', {
                theme: 'snow',
                modules: {
                    'toolbar': [[{ 'font': [] }, { 'size': [] }], ['bold', 'italic', 'underline', 'strike'], [{ 'color': [] }, { 'background': [] }], [{ 'script': 'super' }, { 'script': 'sub' }], [{ 'header': [false, 1, 2, 3, 4, 5, 6] }, 'blockquote', 'code-block'], [{ 'list': 'ordered' }, { 'list': 'bullet' }, { 'indent': '-1' }, { 'indent': '+1' }], ['direction', { 'align': [] }], ['link', 'image', 'video'], ['clean']]
                },
            });
        }
        if (document.getElementById('simplemde1')) {
            new SimpleMDE({
                element: document.getElementById('simplemde1'),
                spellChecker: false,
                placeholder: 'Write something..',
                tabSize: 2,
                status: ["autosave", "lines", "words", "cursor"],
                autosave: {
                    enabled: true,
                    uniqueId: "MyUniqueID",
                }
            });
        }
    }

    initSelect2() {
        document.querySelectorAll('[data-toggle="select2"]').forEach(function (element) {

            if (element.multiple) {
                new Choices(element, {
                    itemSelectText: '',
                    placeholderValue: 'select',
                    placeholder: true,
                    removeItemButton: true,
                    removeItems: true,
                    choices: [
                        { value: 'select', label: "Select", selected: true }
                    ]
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
        this.initEditors();
        this.initSelect2();

        new Wizard('#horizontalwizard');
    }
}

document.addEventListener('DOMContentLoaded', function (e) {
    new EcommerceProduct().init();
});