document.addEventListener("DOMContentLoaded", function () {
    const showNavbar = (toggleId, navId, bodyId, headerId) => {
      const toggle = document.getElementById(toggleId),
        nav = document.getElementById(navId),
        bodypd = document.getElementById(bodyId),
        headerpd = document.getElementById(headerId);

      const navbarState = localStorage.getItem("navbarState");

      if (navbarState === "expanded") {
        nav.classList.add("show");
        nav.classList.remove("navbar-collapsed");
        toggle.classList.add("bx-x");
        bodypd.classList.add("body-pd");
        headerpd.classList.add("body-pd");
      } else {
        nav.classList.remove("show");
        nav.classList.add("navbar-collapsed");
        toggle.classList.remove("bx-x");
        bodypd.classList.remove("body-pd");
        headerpd.classList.remove("body-pd");
      }

      if (toggle && nav && bodypd && headerpd) {
        toggle.addEventListener("click", () => {
          nav.classList.toggle("show");
          nav.classList.toggle("navbar-collapsed");
          bodypd.classList.toggle("body-pd");
          headerpd.classList.toggle("body-pd");

          if (nav.classList.contains("show")) {
            localStorage.setItem("navbarState", "expanded");
          } else {
            localStorage.setItem("navbarState", "collapsed");
          }
        });
      }
    };

    showNavbar("header-toggle", "nav-bar", "body-pd", "header");

    const linkColor = document.querySelectorAll(".nav_link");

    function colorLink() {
      if (linkColor) {
        linkColor.forEach((l) => l.classList.remove("active"));
        this.classList.add("active");
      }
    }
    linkColor.forEach((l) => l.addEventListener("click", colorLink));
  });