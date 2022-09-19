var clicked = Cookies.get("active");

if (clicked == "true" && $("#sidebar").hasClass("active") == false) {
  $("#sidebar").toggleClass("active");
  $("#sidebarCollapse").toggleClass("active");
}

$("#sidebarCollapse").on("click", function () {
  $("#sidebar").toggleClass("active");
  $("#sidebarCollapse").toggleClass("active");
  Cookies.set("active", $("#sidebar").hasClass("active"));
});
$("#gamertagSubmit").on("click", function () {
  var search = $("#userSearchTermSideBar").val();
  if ($.trim(search) != "") {
    window.location.href = "/search/@/" + search;
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
picture.oninput = (evt) => {
  const [file] = picture.files;
  if (file) {
    document.getElementById("pictureButton").click();
  }
};
var originalUsername = originalusername.value;
var originalEmail = originalemail.value;
var originalMotto = originalmotto.value;
var originalBio = originalbio.value;
var originalBirthDay = originalbirthday.value;
username.oninput = (evt) => {
  if (username.value === originalUsername) {
    document.getElementById("usernameButton").style.display = "none";
    username.classList.remove("changed");
  }
  if (username.value != originalUsername) {
    document.getElementById("usernameButton").style.display = "inline-block";
    username.classList.add("changed");
  }
};
email.oninput = (evt) => {
  if (email.value === originalEmail) {
    document.getElementById("emailButton").style.display = "none";
    email.classList.remove("changed");
  }
  if (email.value != originalEmail) {
    document.getElementById("emailButton").style.display = "inline-block";
    email.classList.add("changed");
  }
};
motto.oninput = (evt) => {
  if (motto.value === originalMotto) {
    document.getElementById("mottoButton").style.display = "none";
    motto.classList.remove("changed");
  }
  if (motto.value != originalMotto) {
    document.getElementById("mottoButton").style.display = "inline-block";
    motto.classList.add("changed");
  }
};
bio.oninput = (evt) => {
  if (bio.value === originalBio) {
    document.getElementById("bioButton").style.display = "none";
    bio.classList.remove("changed");
  }
  if (bio.value != originalBio) {
    document.getElementById("bioButton").style.display = "inline-block";
    bio.classList.add("changed");
  }
};
birthday.oninput = (evt) => {
  if (birthday.value === originalBirthDay) {
    document.getElementById("birthdayButton").style.display = "none";
    birthday.classList.remove("changed");
  }
  if (birthday.value != originalBirthDay) {
    document.getElementById("birthdayButton").style.display = "inline-block";
    birthday.classList.add("changed");
  }
};
confirm_password.oninput = (evt) => {
  document.getElementById("confirmButton").style.display = "inline-block";
  confirm_password.classList.add("changed");
};
