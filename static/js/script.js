var clicked = Cookies.get("active");

if (clicked == "true" && $("#sidebar").hasClass("active") == false) {
  $("#sidebar").toggleClass("active");
}

$("#sidebarCollapse").on("click", function () {
  $("#sidebar").toggleClass("active");
  Cookies.set("active", $("#sidebar").hasClass("active"));
});
$("#gamertagSubmit").on("click", function () {
  var search = $("#userSearchTermSideBar").val();
  if ($.trim(search) != "") {
    window.location.href = "/search/@/" + search;
  }
});
$("#gamertagSubmitNav").on("click", function () {
  var searchMethod = $("#userSearchMethod").val();
  var search = $("#userSearchTerm").val();
  if ($.trim(search) != "") {
    window.location.href = "/search/" + searchMethod + "/" + search;
  }
});
var input = document.getElementById("userSearchTerm");
input.addEventListener("keypress", function (event) {
  var search = $("#userSearchTerm").val();
  if ($.trim(search) != "") {
    if (event.key === "Enter") {
      event.preventDefault();
      document.getElementById("gamertagSubmitNav").click();
    }
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
picture.onchange = (evt) => {
  const [file] = picture.files;
  if (file) {
    document.getElementById("submit").click();
  }
};
var originalUsername = username.value;
var originalEmail = email.value;
username.onchange = (evt) => {
  if (username.value === originalUsername) {
    document.getElementById("usernameButton").style.display = "none";
  }
  if (username.value != originalUsername) {
    document.getElementById("usernameButton").style.display = "block";
  }
};
email.onchange = (evt) => {
  if (email.value === originalEmail) {
    document.getElementById("emailButton").style.display = "none";
  }
  if (email.value != originalEmail) {
    document.getElementById("emailButton").style.display = "block";
  }
};
confirm_password.onchange = (evt) => {
  document.getElementById("confirmButton").style.display = "block";
};
