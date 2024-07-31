//닉네임 조건 만족하면 체크표시, 만족하지 않으면 x표시
document.addEventListener("DOMContentLoaded", function () {
  const nicknameInput = document.getElementById("nickname");
  const idInput = document.getElementById("id");
  const emailInput = document.getElementById("email");
  const password1Input = document.getElementById("password1");
  const password2Input = document.getElementById("password2");
  const submitButton = document.getElementById("submit");

  //닉네임
  const validateNickname = () => {
    const value = nicknameInput.value;
    const box = nicknameInput.parentElement;
    const validImg = box.querySelector(".valid");
    const invalidImg = box.querySelector(".invalid");

    if (value === "") {
      validImg.style.display = "none";
      invalidImg.style.display = "none";
    } else {
      const isValid = /^[가-힣a-zA-Z0-9]{1,10}$/.test(value);
      validImg.style.display = isValid ? "inline" : "none";
      invalidImg.style.display = isValid ? "none" : "inline";
    }

    checkFormValidity();
  };

  //아이디
  const validateId = () => {
    const value = idInput.value;
    const box = idInput.parentElement;
    const validImg = box.querySelector(".valid");
    const invalidImg = box.querySelector(".invalid");

    if (value === "") {
      validImg.style.display = "none";
      invalidImg.style.display = "none";
    } else {
      const isValid = /^[가-힣a-zA-Z0-9]{6,10}$/.test(value);
      validImg.style.display = isValid ? "inline" : "none";
      invalidImg.style.display = isValid ? "none" : "inline";
    }

    checkFormValidity();
  };

  //이메일
  const validateEmail = () => {
    const value = emailInput.value;
    const box = emailInput.parentElement;
    const validImg = box.querySelector(".valid");
    const invalidImg = box.querySelector(".invalid");

    if (value === "") {
      validImg.style.display = "none";
      invalidImg.style.display = "none";
    } else {
      const isValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
      validImg.style.display = isValid ? "inline" : "none";
      invalidImg.style.display = isValid ? "none" : "inline";
    }

    checkFormValidity();
  };

  //비밀번호
  const validatePassword1 = () => {
    const password = password1Input.value;
    const box = password1Input.parentElement;
    const validImg = box.querySelector(".valid");
    const invalidImg = box.querySelector(".invalid");

    const isValid = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/.test(password);

    if (password === "") {
      validImg.style.display = "none";
      invalidImg.style.display = "none";
    } else {
      validImg.style.display = isValid ? "inline" : "none";
      invalidImg.style.display = isValid ? "none" : "inline";
    }

    checkFormValidity();
  };

  //비밀번호 확인
  const validatePassword2 = () => {
    const password1 = password1Input.value;
    const password2 = password2Input.value;
    const box = password2Input.parentElement;
    const validImg = box.querySelector(".valid");
    const invalidImg = box.querySelector(".invalid");

    if (password2 === "") {
      validImg.style.display = "none";
      invalidImg.style.display = "none";
    } else {
      const isValid = password1 === password2;
      validImg.style.display = isValid ? "inline" : "none";
      invalidImg.style.display = isValid ? "none" : "inline";
    }

    checkFormValidity();
  };

  //다음 버튼 색 변경
  const checkFormValidity = () => {
    const isNicknameValid = /^[가-힣a-zA-Z0-9]{1,10}$/.test(nicknameInput.value);
    const isIdValid = /^[가-힣a-zA-Z0-9]{6,10}$/.test(idInput.value);
    const isEmailValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(emailInput.value);
    const isPassword1Valid = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/.test(password1Input.value);
    const isPassword2Valid = password1Input.value === password2Input.value;

    if (isNicknameValid && isIdValid && isEmailValid && isPassword1Valid && isPassword2Valid) {
      submitButton.style.backgroundColor = "#FCFCA8";
    } else {
      submitButton.style.backgroundColor = "";
    }
  };

  nicknameInput.addEventListener("input", validateNickname);
  idInput.addEventListener("input", validateId);
  emailInput.addEventListener("input", validateEmail);
  password1Input.addEventListener("input", validatePassword1);
  password2Input.addEventListener("input", validatePassword2);
});
//비밀번호 보이게
const pwdInput1 = document.getElementById("password1");
const togglePwd1 = document.getElementById("togglePwd1");

togglePwd1.addEventListener("click", function () {
  if (pwdInput1.type === "password") {
    pwdInput1.type = "text";
    togglePwd1.src = "/MIMO/img/signup.html_eyeopened.svg";
  } else {
    pwdInput1.type = "password";
    togglePwd1.src = "/MIMO/img/signup.html_eyeclosed.svg";
  }
});

const pwdInput2 = document.getElementById("password2");
const togglePwd2 = document.getElementById("togglePwd2");

togglePwd2.addEventListener("click", function () {
  if (pwdInput2.type === "password") {
    pwdInput2.type = "text";
    togglePwd2.src = "/MIMO/img/signup.html_eyeopened.svg";
  } else {
    pwdInput2.type = "password";
    togglePwd2.src = "/MIMO/img/signup.html_eyeclosed.svg";
  }
});

// 비밀번호 지우기
const clearPwd1 = document.getElementById("clearPwd1");
const clearPwd2 = document.getElementById("clearPwd2");

clearPwd1.addEventListener("click", function () {
  pwdInput1.value = "";
  validatePassword1();
  validatePassword2(); // 비밀번호 확인 칸도 업데이트
});

clearPwd2.addEventListener("click", function () {
  pwdInput2.value = "";
  validatePassword2();
});
