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

// In-page anchor scrolling. The published site renders inside a srcdoc iframe,
// where native href="#id" fragment navigation does not scroll, so handle it in JS.
document.querySelectorAll('a[href^="#"]').forEach((link) => {
  link.addEventListener("click", (e) => {
    const hash = link.getAttribute("href");
    if (hash.length <= 1) return; // ignore bare "#"
    const target = document.querySelector(hash);
    if (!target) return;
    e.preventDefault();
    target.scrollIntoView({ behavior: "smooth", block: "start" });
    if (mobileMenu) mobileMenu.classList.add("hidden");
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

AOS.init({
  duration: 1000,
  once: true,
  offset: 100,
  easing: "ease-out-cubic",
});
