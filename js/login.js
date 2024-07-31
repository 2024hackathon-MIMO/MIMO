document.addEventListener("DOMContentLoaded", function () {
  const pwdInput = document.getElementById("password");
  const togglePwd = document.getElementById("togglePwd");
  const clearPwd = document.getElementById("clearPwd");

  // 비밀번호 보이게/숨기게
  togglePwd.addEventListener("click", function () {
    if (pwdInput.type === "password") {
      pwdInput.type = "text";
      togglePwd.src = "/MIMO/img/signup.html_eyeopened.svg";
    } else {
      pwdInput.type = "password";
      togglePwd.src = "/MIMO/img/signup.html_eyeclosed.svg";
    }
  });

  // 비밀번호 지우기
  clearPwd.addEventListener("click", function () {
    pwdInput.value = "";
    validatePassword();
  });

  pwdInput.addEventListener("input", validatePassword);
});
