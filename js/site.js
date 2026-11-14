document.addEventListener("click", (event) => {
  const target = event.target;
  if (!(target instanceof HTMLImageElement)) return;
  if (!target.closest(".gallery, .hero")) return;

  let box = document.getElementById("lightbox");
  if (!box) {
    box = document.createElement("div");
    box.id = "lightbox";
    box.innerHTML = "<img alt=''>";
    document.body.appendChild(box);
    box.addEventListener("click", () => box.classList.remove("open"));
  }
  box.querySelector("img").src = target.src;
  box.classList.add("open");
});

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") {
    document.getElementById("lightbox")?.classList.remove("open");
  }
});
