// Run once the DOM is ready
document.addEventListener("DOMContentLoaded", () => {
  // Footer year (guard in case the element is missing)
  const yearEl = document.getElementById("year");
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  // Smooth scroll for in-page links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener("click", e => {
      const targetSel = anchor.getAttribute("href");
      if (!targetSel || targetSel === "#") return;
      const target = document.querySelector(targetSel);
      if (!target) return;
      e.preventDefault();
      target.scrollIntoView({ behavior: "smooth" });
    });
  });
});

// Make these global so onclick="openVideo()" in HTML can find them
window.openVideo = () => {
  const lb = document.getElementById("lightbox");
  if (lb) lb.style.display = "flex";
};

window.closeVideo = () => {
  const lb = document.getElementById("lightbox");
  if (lb) lb.style.display = "none";
};
