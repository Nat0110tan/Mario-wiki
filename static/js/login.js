window.addEventListener("load", function() {
    function sign_up(){
        login.style.transform = "rotateY(180deg)"
        signup.style.transform = "rotateY(0deg)";
    }

    function log_in(){
        login.style.transform = "rotateY(0deg)"
        signup.style.transform = "rotateY(-180deg)";
    }

    let login = document.querySelector(".login");
    let signup = document.querySelector(".signup");
    let loginbtn = document.querySelector(".loginbtn");
    let signupbtn = document.querySelector(".signupbtn");

    loginbtn.onclick = log_in;
    signupbtn.onclick = sign_up;
    

});