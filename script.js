document.addEventListener("DOMContentLoaded", () => {
  const yearEl = document.getElementById("year");
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  // Smooth scroll
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener("click", e => {
      const sel = a.getAttribute("href");
      if (!sel || sel === "#") return;
      const target = document.querySelector(sel);
      if (!target) return;
      e.preventDefault();
      target.scrollIntoView({ behavior: "smooth" });
    });
  });
});

// Expose for onclick handlers
window.openVideo = () => {
  const lb = document.getElementById("lightbox");
  if (lb) lb.style.display = "flex";
};
window.closeVideo = () => {
  const lb = document.getElementById("lightbox");
  if (lb) lb.style.display = "none";
};
