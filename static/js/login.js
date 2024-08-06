// 비밀번호 표시 토글 기능

document.addEventListener("DOMContentLoaded", function () {
  const passwordToggles = document.querySelectorAll(".password-toggle");

  passwordToggles.forEach((toggle) => {
    toggle.addEventListener("click", function () {
      const inputId = toggle.id.replace("togglePwd", "password");
      const pwdInput = document.getElementById(inputId);
      const eyeOpenSrc = toggle.getAttribute("data-eye-open");
      const eyeClosedSrc = toggle.getAttribute("data-eye-closed");

      if (pwdInput.type === "password") {
        pwdInput.type = "text";
        toggle.src = eyeOpenSrc;
      } else {
        pwdInput.type = "password";
        toggle.src = eyeClosedSrc;
      }
    });
  });
});

// 비밀번호 지우기
document.addEventListener("DOMContentLoaded", function () {
  const pwdInput = document.getElementById("password");
  const clearPwd = document.getElementById("clearPwd");

  clearPwd.addEventListener("click", function () {
    pwdInput.value = "";
  });
});
