/*
Template Name: Reback - Responsive 5 Admin Dashboard
Author: Techzaa
File: touchspin js
*/

class TouchSpin {

  constructor() {
    this.body = document.getElementsByTagName("body")[0];
    this.window = window;
  }

  initTouchspin() {

    document.querySelectorAll('[data-toggle="touchspin"]').forEach(function (touchspin) {

      let value = touchspin.getAttribute('value');
      const btsPrefix = touchspin.getAttribute('data-bts-prefix');
      const btsPostfix = touchspin.getAttribute('data-bts-postfix');
      const btsPrefixExtraClass = touchspin.getAttribute('data-bts-prefix-extra-class');
      const btsPostfixExtraClass = touchspin.getAttribute('data-bts-prefix-extra-class');
      const btsBtnDownClass = touchspin.getAttribute('data-bts-button-down-class');
      const btsBtnUpClass = touchspin.getAttribute('data-bts-button-up-class');
      const step = touchspin.getAttribute('data-step') ?? 1;
      const max = touchspin.getAttribute('data-bts-max');
      const decimals = touchspin.getAttribute('data-decimals') ?? 0;
      const longPressInterval = 150;

      const mainContainer = document.createElement('div');
      touchspin.parentNode.appendChild(mainContainer);
      touchspin.classList.add("form-control");

      mainContainer.setAttribute("class", "input-group bootstrap-touchspin bootstrap-touchspin-injected");

      const touchDownBtn = document.createElement('button');
      touchDownBtn.setAttribute("class", "bootstrap-touchspin-down input-group-text ".concat(btsBtnDownClass ? btsBtnDownClass : "btn btn-primary"));
      touchDownBtn.type = "button";
      touchDownBtn.innerHTML = "-";

      let btsPrefixInnerText;
      if (btsPrefix) {
        btsPrefixInnerText = document.createElement('span');
        btsPrefixInnerText.setAttribute("class", "input-group-text ".concat(btsPrefixExtraClass ? btsPrefixExtraClass : ""));
        btsPrefixInnerText.innerHTML = btsPrefix;
      }

      let btsPostfixInnerText;
      if (btsPostfix) {
        btsPostfixInnerText = document.createElement('span');
        btsPostfixInnerText.setAttribute("class", "input-group-text ".concat(btsPostfixExtraClass ? btsPrefixExtraClass : ""));
        btsPostfixInnerText.innerHTML = btsPostfix;
      }

      const touchUpBtn = document.createElement('button');
      touchUpBtn.setAttribute("class", "bootstrap-touchspin-up ".concat(btsBtnUpClass ? btsBtnUpClass : "btn btn-primary"));
      touchUpBtn.type = "button";
      touchUpBtn.innerHTML = "+";

      mainContainer.appendChild(touchDownBtn);

      if (btsPrefixInnerText) {
        mainContainer.appendChild(btsPrefixInnerText);
      }

      mainContainer.appendChild(touchspin);

      if (btsPostfixInnerText) {
        mainContainer.appendChild(btsPostfixInnerText);
      }

      mainContainer.appendChild(touchUpBtn);

      //*-------------------- Click --------------------*//

      var timerDown, timerUp;

      touchDownBtn.addEventListener('click', function (e) {
        let value;
        if (isNaN(parseFloat(touchspin.getAttribute('value')))) {
          value = 0;
        } else {
          value = parseFloat(touchspin.getAttribute('value'));
        }
        if (value - step >= 0) {
          touchspin.setAttribute("value", (value - step).toFixed(decimals));
          touchspin.value = (value - step).toFixed(decimals);
        } else {
          touchspin.setAttribute("value", 0);
          touchspin.value = 0;
        }
      });

      touchDownBtn.addEventListener('mousedown', function (e) {


        timerDown = setInterval(function () {
          let value;
          if (isNaN(parseFloat(touchspin.getAttribute('value')))) {
            value = 0;
          } else {
            value = parseFloat(touchspin.getAttribute('value'));
          }
          if (value - step >= 0) {
            touchspin.setAttribute("value", (value - step).toFixed(decimals));
            touchspin.value = (value - step).toFixed(decimals);
          } else {
            touchspin.setAttribute("value", 0);
            touchspin.value = 0;
          }
        }, longPressInterval)


      });
      touchDownBtn.addEventListener('mouseup', function (e) {
        clearInterval(timerDown);
      });
      touchDownBtn.addEventListener('mouseleave', function (e) {
        clearInterval(timerDown);
      });
      touchDownBtn.addEventListener('mouseout', function (e) {
        clearInterval(timerDown);
      });


      touchUpBtn.addEventListener('click', function (e) {
        let value;
        if (isNaN(parseFloat(touchspin.getAttribute('value')))) {
          value = 0;
        } else {
          value = parseFloat(touchspin.getAttribute('value'));
        }


        if (max == null || (parseFloat(value) + parseFloat(step)) <= max) {
          touchspin.setAttribute("value", (parseFloat(value) + parseFloat(step)).toFixed(decimals));

          touchspin.value = (parseFloat(value) + parseFloat(step)).toFixed(decimals);
        }
      });

      touchUpBtn.addEventListener('mousedown', function (e) {

        timerUp = setInterval(function () {
          let value;
          if (isNaN(parseFloat(touchspin.getAttribute('value')))) {
            value = 0;
          } else {
            value = parseFloat(touchspin.getAttribute('value'));
          }


          if (max == null || (parseFloat(value) + parseFloat(step)) <= max) {
            touchspin.setAttribute("value", (parseFloat(value) + parseFloat(step)).toFixed(decimals));
            touchspin.value = (parseFloat(value) + parseFloat(step)).toFixed(decimals);
          }
        }, longPressInterval)

      });
      touchUpBtn.addEventListener('mouseup', function (e) {
        clearInterval(timerUp);
      });
      touchUpBtn.addEventListener('mouseleave', function (e) {
        clearInterval(timerUp);
      });
      touchUpBtn.addEventListener('mouseout', function (e) {
        clearInterval(timerUp);
      });


      touchspin.addEventListener('input', function (event) {
        touchspin.setAttribute('value', touchspin.value);
      });

    });

  }

  init = () => {
    this.initTouchspin();
  }

}

document.addEventListener('DOMContentLoaded', function (e) {
  new TouchSpin().init();
});

