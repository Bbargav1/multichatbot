// Shared site JavaScript. Domain-specific chat behavior lives in each chat template.
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll('a[href="#"]').forEach((link) => {
    link.addEventListener("click", (event) => event.preventDefault());
  });
});
