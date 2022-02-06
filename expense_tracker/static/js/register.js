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
emailCheck = true;
function submitButtonDisabledCheck(){
    if(emailCheck && usernameCheck){
        submitButton.disabled = false;
    }
    else{
        submitButton.disabled = true;
    }
    
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
    
    usernameField.classList.remove("is-invalid");
    invalidUsernameField.style.display="none";
    if(usernameVal.length>0){
        usernameSuccessOutput.style.display="block";
        usernameSuccessOutput.textContent = `Checking ${usernameVal}`;
        fetch("/authentication/validate-username/", {
            body:JSON.stringify({username:usernameVal}),
            method:"POST",
        }).then(res=> res.json()).then((data) =>{
            usernameSuccessOutput.style.display="none";
            if(data.username_error){
                usernameCheck = false;
                usernameField.classList.add("is-invalid");
                invalidUsernameField.style.display="block";
                invalidUsernameField.innerHTML = `<p>${data.username_error}</p>`;
            } 
            else{
                usernameCheck = true;
            }   
            submitButtonDisabledCheck();
        });    
    }    
});    

emailField.addEventListener("keyup", (e)=>{
    const emailVal = e.target.value;
    
    emailField.classList.remove("is-invalid");
    invalidEmailField.style.display="none";
    if(emailVal.length>0){
        emailSuccessOutput.style.display = "block";
        emailSuccessOutput.textContent = `Checking ${emailVal}`
        fetch("/authentication/validate-email/", {
            body:JSON.stringify({email:emailVal}),
            method:"POST",
        }).then(res=> res.json()).then((data) =>{
            emailSuccessOutput.style.display="none";
            if(data.email_error){
                emailCheck = false;
                emailField.classList.add("is-invalid");
                invalidEmailField.style.display="block";
                invalidEmailField.innerHTML = `<p>${data.email_error}</p>`;
            }
            else{
                emailCheck = true;
            }
            submitButtonDisabledCheck();
        });
    }
});




