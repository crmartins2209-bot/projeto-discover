function toggleMode() {
  const html = document.documentElement
  html.classList.toggle("light")

  const img = document.querySelector("#profile img")
  if (html.classList.contains("light")) {
    img.setAttribute("src", "../assets/avatar-light.png")
    img.setAttribute(
      "alt",
      "Foto de Mayk Brito sorrindo, usando oculos e camiseta preta",
    )
  } else {
    img.setAttribute("src", "../assets/avatar.png")
    img.setAttribute(
      "alt",
      "Foto de Mayk Brito usando moletom preto, sorrindo e oculos escuros",
    )
  }

  /* if(html.classList.contains("light")) {
    html.classList.remove("light")
  } else {
    html.classList.add("light")
  } */
}
