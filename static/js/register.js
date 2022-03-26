const usernameField = document.getElementById("usernameField");
const invalidUsernameField = document.querySelector(".invalid-username");
const usernameSuccessOutput = document.querySelector(".usernameSuccessOutput");
const passwordField = document.querySelector("#passwordField");
const emailField = document.getElementById("emailField");
const invalidEmailField = document.querySelector(".invalid-email");
const emailSuccessOutput = document.querySelector(".emailSuccessOutput");

const showPasswordToggle = document.querySelector(".showPasswordToggle");

const submitButton = document.querySelector(".submit-button");

usernameCheck = false;
emailCheck = false;
passwordCheck = false;
function submitButtonDisabledCheck(){
    if(emailCheck && usernameCheck && passwordCheck){
        submitButton.disabled = false;
    }
    else{
        submitButton.disabled = true;
    }
    
}

function clearField(element){
    element.style.display = "none";
}

const handleToggleInput = (e)=>{
     if(showPasswordToggle.textContent==="Show"){
         showPasswordToggle.textContent = "Hide";
         passwordField.setAttribute("type", "text");
        }else{
            showPasswordToggle.textContent = "Show";
            passwordField.setAttribute("type", "password");
     }
}
showPasswordToggle.addEventListener('click', handleToggleInput);

usernameField.addEventListener("keyup", (e)=>{
    const usernameVal = e.target.value;
    if(usernameVal.length==0){
        clearField(usernameSuccessOutput);
    }
    usernameField.classList.remove("is-invalid");
    usernameField.classList.remove("is-valid");
    invalidUsernameField.style.display="none";
    if(usernameVal.length>0){
        usernameSuccessOutput.style.display="block";
        usernameSuccessOutput.textContent = `Checking ${usernameVal.toLowerCase()}`;
        fetch("/authentication/validate-username/", {
            body:JSON.stringify({username:usernameVal}),
            method:"POST",
        }).then(res=> res.json()).then((data) =>{
            if(data.username_error){
                usernameSuccessOutput.style.display="none";
                usernameCheck = false;
                usernameField.classList.add("is-invalid");
                invalidUsernameField.style.display="block";
                invalidUsernameField.innerHTML = `<p>${data.username_error}</p>`;
            } 
            else{
                usernameField.classList.add("is-valid");
                usernameCheck = true;
                usernameSuccessOutput.textContent = `Username Available`;
            }   
            submitButtonDisabledCheck();
        });    
    }    
});    

emailField.addEventListener("keyup", (e)=>{
    const emailVal = e.target.value;
    if(emailVal.length==0){
        clearField(emailSuccessOutput);
    }
    emailField.classList.remove("is-invalid");
    emailField.classList.remove("is-valid");
    invalidEmailField.style.display="none";
    if(emailVal.length>0){
        emailSuccessOutput.style.display = "block";
        emailSuccessOutput.textContent = `Checking ${emailVal.toLowerCase()}`
        fetch("/authentication/validate-email/", {
            body:JSON.stringify({email:emailVal}),
            method:"POST",
        }).then(res=> res.json()).then((data) =>{
            if(data.email_error){
                emailSuccessOutput.style.display="none";
                emailCheck = false;
                emailField.classList.add("is-invalid");
                invalidEmailField.style.display="block";
                invalidEmailField.innerHTML = `<p>${data.email_error}</p>`;
            }
            else{
                emailCheck = true;
                emailField.classList.add("is-valid");
                emailSuccessOutput.textContent = `Email Valid`
            }
            submitButtonDisabledCheck();
        });
    }
});

passwordField.addEventListener("keyup", (e)=>{
    passwordValue = e.target.value;
    if(passwordValue.length<6){
        passwordField.classList.remove("is-valid");
        passwordField.classList.add("is-invalid");
        passwordCheck = false;
        if(passwordValue.length==0){
            passwordField.classList.remove("is-invalid");
        }
    }
    else{
        passwordField.classList.remove("is-invalid");
        passwordField.classList.add("is-valid");
        passwordCheck = true;
    }
    submitButtonDisabledCheck();
});



