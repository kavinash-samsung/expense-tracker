const usernameField = document.getElementById("usernameField");
const invalidUsernameField = document.querySelector(".invalid-username");
const usernameSuccessOutput = document.querySelector(".usernameSuccessOutput");

usernameField.addEventListener("keyup", (e)=>{
    const usernameVal = e.target.value;
    usernameSuccessOutput.style.display="block";
    usernameSuccessOutput.textContent = `Checking ${usernameVal}`;
   
    usernameField.classList.remove("is-invalid");
    invalidUsernameField.style.display="none";
    if(usernameVal.length>0){
        fetch("/authentication/validate-username/", {
            body:JSON.stringify({username:usernameVal}),
            method:"POST",
        }).then(res=> res.json()).then((data) =>{
            usernameSuccessOutput.style.display="none";
            if(data.username_error){
                usernameField.classList.add("is-invalid");
                invalidUsernameField.style.display="block";
                invalidUsernameField.innerHTML = `<p>${data.username_error}</p>`;
            }
        });
    }
});

const emailField = document.getElementById("emailField");
const invalidEmailField = document.querySelector(".invalid-email");
const emailSuccessOutput = document.querySelector(".emailSuccessOutput");


emailField.addEventListener("keyup", (e)=>{
    const emailVal = e.target.value;
    emailSuccessOutput.style.display = "block";
    emailSuccessOutput.textContent = `Checking ${emailVal}`
    
    emailField.classList.remove("is-invalid");
    invalidEmailField.style.display="none";
    if(emailVal.length>0){
        fetch("/authentication/validate-email/", {
            body:JSON.stringify({email:emailVal}),
            method:"POST",
        }).then(res=> res.json()).then((data) =>{
            emailSuccessOutput.style.display="none";
            if(data.email_error){
                emailField.classList.add("is-invalid");
                invalidEmailField.style.display="block";
                invalidEmailField.innerHTML = `<p>${data.email_error}</p>`;
            }
        });
    }
});


