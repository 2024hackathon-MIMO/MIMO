document.addEventListener("DOMContentLoaded", () => {
  const buttons = document.querySelectorAll(".button_box button");
  buttons.forEach((button) => {
    button.addEventListener("click", () => {
      buttons.forEach((btn) => {
        btn.classList.remove("active");
        const img = btn.querySelector("img");
        const imgSrc = img.getAttribute("src").replace("_active", "");
        img.setAttribute("src", imgSrc);
      });
      button.classList.add("active");
      const img = button.querySelector("img");
      const imgSrc = img.getAttribute("src").replace(".svg", "_active.svg");
      img.setAttribute("src", imgSrc);
    });
  });
});

document.querySelector(".select-selected").addEventListener("click", function () {
  this.nextElementSibling.classList.toggle("select-hide");
  this.classList.toggle("select-arrow-active");
});

document.querySelectorAll(".select-items div").forEach(function (item) {
  item.addEventListener("click", function () {
    var selected = document.querySelector(".select-selected");
    selected.textContent = this.textContent;
    selected.nextElementSibling.classList.add("select-hide");
  });
});

document.addEventListener("click", function (e) {
  if (!e.target.matches(".select-selected")) {
    document.querySelector(".select-items").classList.add("select-hide");
  }
});
