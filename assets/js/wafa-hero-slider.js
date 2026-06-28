(function () {
  "use strict";

  var root = document.querySelector("[data-wafa-hero]");
  if (!root) return;

  var slides = root.querySelectorAll(".wafa-hero__slide");
  var dots = root.querySelectorAll(".wafa-hero__dot");
  var prev = root.querySelector(".wafa-hero__nav--prev");
  var next = root.querySelector(".wafa-hero__nav--next");
  var total = slides.length;
  var index = 0;
  var timer = null;
  var delay = 6000;
  var paused = false;

  function show(i) {
    index = (i + total) % total;
    slides.forEach(function (slide, n) {
      slide.classList.toggle("is-active", n === index);
      slide.setAttribute("aria-hidden", n === index ? "false" : "true");
    });
    dots.forEach(function (dot, n) {
      dot.classList.toggle("is-active", n === index);
      dot.setAttribute("aria-selected", n === index ? "true" : "false");
    });
  }

  function nextSlide() {
    show(index + 1);
  }

  function prevSlide() {
    show(index - 1);
  }

  function startAutoplay() {
    stopAutoplay();
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    timer = window.setInterval(function () {
      if (!paused) nextSlide();
    }, delay);
  }

  function stopAutoplay() {
    if (timer) window.clearInterval(timer);
    timer = null;
  }

  if (prev) prev.addEventListener("click", function () { prevSlide(); startAutoplay(); });
  if (next) next.addEventListener("click", function () { nextSlide(); startAutoplay(); });

  dots.forEach(function (dot) {
    dot.addEventListener("click", function () {
      show(parseInt(dot.getAttribute("data-index"), 10));
      startAutoplay();
    });
  });

  root.addEventListener("mouseenter", function () { paused = true; });
  root.addEventListener("mouseleave", function () { paused = false; });
  root.addEventListener("focusin", function () { paused = true; });
  root.addEventListener("focusout", function () { paused = false; });

  root.addEventListener("keydown", function (e) {
    if (e.key === "ArrowLeft") { prevSlide(); startAutoplay(); }
    if (e.key === "ArrowRight") { nextSlide(); startAutoplay(); }
  });

  show(0);
  startAutoplay();
})();
