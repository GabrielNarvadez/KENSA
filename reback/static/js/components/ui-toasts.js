/*
Template Name: Reback - Responsive 5 Admin Dashboard
Author: Techzaa
File: Bootstrap UI Toast
*/


// Default Example
const toastDefaultTrigger = document.getElementById('liveToastDefaultBtn')
const toastDefaultLiveExample = document.getElementById('liveToastDefault')
if (toastDefaultTrigger) {
    toastDefaultTrigger.addEventListener('click', () => {
        const toast = new bootstrap.Toast(toastDefaultLiveExample)

        toast.show()
    })
}

// Stacking Example
const toastTrigger = document.getElementById('liveToastBtn')
const toastLiveExample = document.getElementById('liveToast')
if (toastTrigger) {
    toastTrigger.addEventListener('click', () => {
        const toast = new bootstrap.Toast(toastLiveExample)

        toast.show()
    })
}

const toastTrigger2 = document.getElementById('liveToastBtn2')
const toastLiveExample2 = document.getElementById('liveToast2')
if (toastTrigger2) {
    toastTrigger2.addEventListener('click', () => {
        const toast = new bootstrap.Toast(toastLiveExample2)
        toast.show()
    })
}