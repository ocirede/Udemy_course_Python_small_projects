
document.addEventListener("DOMContentLoaded", function () {
    const data = window.portfolioData;

    if (!data) return;

    const isMobile = data.isMobile === true || data.isMobile === "true";
    const emailParts = data.emailParts;
    const phoneParts = data.phoneParts;
    const addressParts = data.addressParts;

    const email = `${emailParts[0]}@${emailParts[1]}.${emailParts[2]}`;
    const emailLink = document.getElementById("email-link");

    if (!emailLink) return;

    if (isMobile) {
        emailLink.href = `mailto:${email}`;
    } else {
        emailLink.href = `https://mail.google.com/mail/?view=cm&fs=1&to=${email}`;
        emailLink.target = "_blank";
    }

    emailLink.textContent = email;
    // important
    const phoneElement = document.getElementById("phone-text");
    if (phoneElement) {
        phoneElement.textContent = phoneParts.join(" ");
    }

    const addressElement = document.getElementById("address-text")
    if (addressElement){
       addressElement.textContent = addressParts.join(" ")
    }

});
