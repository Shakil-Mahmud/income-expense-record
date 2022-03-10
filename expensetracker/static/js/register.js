console.log("register js");
const usernameField = document.querySelector("#usernameField");
const feedbackField = document.querySelector(".invalid-feedback");
const passwordField = document.querySelector("#passwordField");
const emailFeedbackField = document.querySelector(".email-invalid-feedback");
const showPasswordToggle = document.querySelector(".showPasswordToggle");

const handleToggleInput = (e) => {
    if (showPasswordToggle.textContent === "SHOW") {
      showPasswordToggle.textContent = "HIDE";
      passwordField.setAttribute("type", "text");
    } else {
      showPasswordToggle.textContent = "SHOW";
      passwordField.setAttribute("type", "password");
    }
  };
  
showPasswordToggle.addEventListener("click", handleToggleInput);

emailField.addEventListener("keyup", (e)=>{
    const emailVal = e.target.value;
    if(emailVal.length > 0){
        emailField.classList.remove("is-invalid");
        emailFeedbackField.style.display= "none"; 
        fetch("/authentication/validate-email", {
            body: JSON.stringify({email: emailVal}),
            method: "POST",
        })
            .then(res=>res.json())
            .then(data=>{
                console.log("data", data);
                if(data.email_error){
                    emailField.classList.add("is-invalid");
                    emailFeedbackField.style.display= "block"; 
                    emailFeedbackField.innerHTML=`${data.email_error}`
                }
            })
    }
});

usernameField.addEventListener("keyup", (e)=>{
    const usernameVal = e.target.value;
    if(usernameVal.length > 0){
        usernameField.classList.remove("is-invalid");
        feedbackField.style.display= "none"; 
        fetch("/authentication/validate-username", {
            body: JSON.stringify({username: usernameVal}),
            method: "POST",
        })
            .then(res=>res.json())
            .then(data=>{
                console.log("data", data);
                if(data.username_error){
                    usernameField.classList.add("is-invalid");
                    feedbackField.style.display= "block"; 
                    feedbackField.innerHTML=`${data.username_error}`
                }
            })
    }
});
