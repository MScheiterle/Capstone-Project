var clicked = Cookies.get("active");

if (clicked == "true" && $("#sidebar").hasClass("active") == false) {
  $("#sidebar").toggleClass("active");
  $("#sidebarCollapse").toggleClass("active");
} else {
  $("#sidebar").toggleClass("deactive");
  $("#sidebarCollapse").toggleClass("deactive");
}

$("#sidebarCollapse").on("click", function () {
  $("#sidebar").toggleClass("active");
  $("#sidebarCollapse").toggleClass("active");
  $("#sidebar").toggleClass("deactive");
  $("#sidebarCollapse").toggleClass("deactive");
  Cookies.set("active", $("#sidebar").hasClass("active"));
});
$("#gamertagSubmit").on("click", function () {
  var search = $("#userSearchTermSideBar").val();
  if ($.trim(search) != "") {
    window.location.href = "/search/" + search;
  } else {
    window.location.href = "/search";
  }
});
var input = document.getElementById("userSearchTermSideBar");
input.addEventListener("keypress", function (event) {
  var search = $("#userSearchTermSideBar").val();
  if ($.trim(search) != "") {
    if (event.key === "Enter") {
      event.preventDefault();
      document.getElementById("gamertagSubmit").click();
    }
  }
});
const errors = document.querySelectorAll(".error-bar");
errors.forEach((error) => {
  setTimeout(function () {
    error.remove();
  }, 10000);
  error.addEventListener("click", function () {
    error.remove();
  });
});
