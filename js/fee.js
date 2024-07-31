document.querySelectorAll(".checkBox").forEach(function (button) {
  button.addEventListener("click", function () {
    document.querySelectorAll(".checkBox").forEach(function (btn) {
      btn.classList.remove("clicked");
    });
    this.classList.toggle("clicked");
  });
});
