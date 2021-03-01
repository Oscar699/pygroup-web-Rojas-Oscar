
//Codigo js para cuenta.html

function editLoginName(){
    document.getElementById("login_name_old").style.display="none";
    document.getElementById("login_name").style.display="block";
    document.getElementById("login-name-button-container").style.display="block";
    document.getElementById("login_name").focus();
}
function editPassword(){
    document.getElementById("password").style.display="block";
    document.getElementById("password-button-container").style.display="block";
    document.getElementById("password").focus();
}

function editEmail(){
    document.getElementById("email_old").style.display="none";
    document.getElementById("email").style.display="block";
    document.getElementById("email-button-container").style.display="block";
    document.getElementById("email").focus();
}
function editFirstName(){
    document.getElementById("first_name_old").style.display="none";
    document.getElementById("first_name").style.display="block";
    document.getElementById("first_name-button-container").style.display="block";
    document.getElementById("first_name").focus();
}
function editLastName(){
    document.getElementById("last_name_old").style.display="none";
    document.getElementById("last_name").style.display="block";
    document.getElementById("last_name-button-container").style.display="block";
    document.getElementById("last_name").focus();
}
function editAddress(){
    document.getElementById("address_old").style.display="none";
    document.getElementById("address").style.display="block";
    document.getElementById("address-button-container").style.display="block";
    document.getElementById("address").focus();
}
function editPhoneNumber(){
    document.getElementById("phone_number_old").style.display="none";
    document.getElementById("phone_number").style.display="block";
    document.getElementById("phone-number-button-container").style.display="block";
    document.getElementById("phone_number").focus();
}

function  sendFirstNameForm(){
    document.getElementById("first_name_form").submit()
}
function  sendLastNameForm(){
    document.getElementById("last_name_form").submit()
}
function  sendEmailForm(){
    document.getElementById("email_form").submit()
}
function  sendloginNameForm(){
    document.getElementById("login_name_form").submit()
}
function sendEmailForm(){
    document.getElementById("email_form").submit()
}
function sendPasswordForm(){
    document.getElementById("password_form").submit()
}
function sendAddressForm(){
    document.getElementById("address_form").submit()
}
function sendPhoneNumberForm(){
    document.getElementById("phone_number_form").submit()
}

function formAccuounActivation(){
    document.getElementById("account-form").submit();
}

// Funcion para ir al panel del admin


