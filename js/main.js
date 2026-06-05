const menuBtn = document.getElementById("menuBtn");
const mobileMenu = document.getElementById("mobileMenu");

menuBtn.addEventListener("click", () => {
  mobileMenu.classList.toggle("hidden");
});

document.querySelectorAll(".nav-mobile-links a[href^='#']").forEach((link) => {
  link.addEventListener("click", () => {
    mobileMenu.classList.add("hidden");
  });
});

document.querySelectorAll(".faq-trigger").forEach((trigger) => {
  trigger.addEventListener("click", () => {
    const content = trigger.nextElementSibling;
    const icon = trigger.querySelector(".faq-icon");

    content.classList.toggle("active");

    icon.textContent = content.classList.contains("active") ? "−" : "+";
  });
});

function initAOS() {
  if (window.AOS) {
    AOS.init({
      duration: 1000,
      once: true,
      offset: 100,
      easing: "ease-out-cubic",
    });
  } else {
    setTimeout(initAOS, 50);
  }
}
initAOS();
