document.querySelectorAll("[data-card-menu]").forEach(el => {
    const
    menuBtn = el.querySelector("[data-card-menu-btn]"),
    menuItems = el.querySelectorAll("[data-card-menu-item]");
  
    menuBtn.addEventListener("click", e => menuItems.forEach(el => {
      if (el.classList.contains("visible")) {
        el.classList.remove("visible")
      } else {
        el.classList.add("visible")
      }
    }));
});