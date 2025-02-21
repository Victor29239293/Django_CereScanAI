const $eye = document.querySelector(".fa-eye-slash")

document.addEventListener("click",  e => { 
  if (e.target === $eye) { 
    if ($eye.classList.contains("fa-eye")) {
      $eye.classList.remove("fa-eye")
      $eye.classList.add("fa-eye-slash")

      const $sibling = $eye.nextElementSibling 
      $sibling.setAttribute("type", "password")
    } else  {
      $eye.classList.remove("fa-eye-slash")
      $eye.classList.add("fa-eye")

      const $sibling = $eye.nextElementSibling 
      $sibling.setAttribute("type", "text")
    }
  }
})