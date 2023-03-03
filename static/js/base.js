window.addEventListener("load", function() {
  function showHamburgerNavLinks() {
    let hamburgerLinks = document.getElementById("hamburgerNavBar");
    if (hamburgerLinks.style.display === "block") {
      hamburgerLinks.style.display = "none";
    } else {
      hamburgerLinks.style.display = "block";
    }
  }

  // function showDropdown(filter) {
  //   let id = filter+"_dropdown_list";
  //   let dropdown = document.getElementById(id);
  //   if (dropdown.style.display === "block") {
  //     dropdown.style.display = "none";
  //   } else {
  //     dropdown.style.display = "block";
  //   }
  // }

  let hamburgerButton = document.getElementById("hamburger");
  hamburgerButton.onclick = showHamburgerNavLinks;

  // let characterButton = document.getElementById("character_dropdown_link");
  // characterButton.addEventListener("click", function() {
  //   showDropdown("character");
  // });

  // let gamesButton = document.getElementById("games_dropdown_link");
  // gamesButton.addEventListener("click", function() {
  //   showDropdown("games");
  // });

  // let contentButton = document.getElementById("content_dropdown_link");
  // contentButton.addEventListener("click", function() {
  //   showDropdown("content");
  // });
})