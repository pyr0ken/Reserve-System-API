const replaceDigits = function () {
    const map = ["&#1776;", "&#1777;", "&#1778;", "&#1779;", "&#1780;", "&#1781;", "&#1782;", "&#1783;", "&#1784;", "&#1785;"];
    const elements = document.getElementsByClassName("persian-digit");
    for (let i = 0; i < elements.length; i++) {
        elements[i].innerHTML = elements[i].innerHTML.replace(/\d(?=[^<>]*(<|$))/g, function ($0) {
            return map[$0];
        });
    }
};
window.onload = replaceDigits;

// ------------ Start Menubar ----------------

const marker = document.querySelector('#marker');
const item = document.querySelectorAll('ul li a');

function Indicator(e) {
    marker.style.left = e.offsetLeft + 'px'
    marker.style.width = e.offsetWidth + 'px'
}


item.forEach(link => {
    link.addEventListener('mousemove', (e) => {
        Indicator(e.target)
    })
});

window.addEventListener('DOMContentLoaded', (event) => {
    const homeLink = document.querySelector('.Home');
    const tableLink = document.querySelector('.Table');
    const profileLink = document.querySelector('.Profile');
    const registerLink = document.querySelector('.Register');
    const loginLink = document.querySelector('.Login');
    const url = window.location.href
    const pathArray = url.split('/');
    if (pathArray[4] === "profile") {
        Indicator(profileLink)
    } else if (pathArray[3] === "table") {
        Indicator(tableLink)
    } else if (pathArray[4] === "register") {
        Indicator(registerLink)
    } else if (pathArray[4] === "login") {
        Indicator(loginLink)
    } else {
        Indicator(homeLink);
    }
});
// ------------ End Menubar ----------------

// ------------ Start Logout Confirm ----------------
function doLogout() {
    Swal.fire({
        title: "اعلان",
        text: 'آیا مطمئن هستید که میخواهید خارج شوید؟',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'خارج شو',
        cancelButtonText: 'بستن',
        confirmButtonColor: "red",
        cancelButtonColor: "blue",
        focusCancel: true,
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href = "/accounts/logout/";
        }
    })
}

// ------------ End Logout Confirm ----------------

