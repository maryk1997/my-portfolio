(() => {
  const root = document.documentElement;
  const menu = document.getElementById("mobileMenu");
  const menuBtn = document.getElementById("menuBtn");
  const menuClose = document.getElementById("menuClose");
  const nav = document.getElementById("nav");
  const scrollLine = document.getElementById("scrollLine");
  const themeToggle = document.getElementById("themeToggle");
  const themeLabel = themeToggle?.querySelector(".theme-label");
  const themeIcon = themeToggle?.querySelector(".theme-icon");

  const applyTheme = (theme) => {
    root.dataset.theme = theme;
    localStorage.setItem("mk-theme", theme);

    if (theme === "dark") {
      if (themeLabel) themeLabel.textContent = "Light";
      if (themeIcon) themeIcon.textContent = "☼";
    } else {
      if (themeLabel) themeLabel.textContent = "Night";
      if (themeIcon) themeIcon.textContent = "◐";
    }
  };

  const savedTheme = localStorage.getItem("mk-theme");
  const initialTheme = savedTheme || (matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
  applyTheme(initialTheme);

  themeToggle?.addEventListener("click", () => {
    applyTheme(root.dataset.theme === "dark" ? "light" : "dark");
  });

  const openMenu = () => {
    menu.classList.add("is-open");
    document.body.style.overflow = "hidden";
  };

  const closeMenu = () => {
    menu.classList.remove("is-open");
    document.body.style.overflow = "";
  };

  menuBtn?.addEventListener("click", openMenu);
  menuClose?.addEventListener("click", closeMenu);
  menu?.querySelectorAll("a").forEach(a => a.addEventListener("click", closeMenu));

  const onScroll = () => {
    const max = document.documentElement.scrollHeight - innerHeight;
    const percent = max > 0 ? (scrollY / max) * 100 : 0;
    scrollLine.style.width = percent + "%";
    nav.classList.toggle("is-scrolled", scrollY > 8);
  };

  addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  const reduceMotion = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const reveals = document.querySelectorAll(".reveal");

  if (reduceMotion || !("IntersectionObserver" in window)) {
    reveals.forEach(el => el.classList.add("is-visible"));
  } else {
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: .1, rootMargin: "0px 0px -35px 0px" });

    reveals.forEach(el => observer.observe(el));
  }
})();
