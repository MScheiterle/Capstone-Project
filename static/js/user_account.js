picture.oninput = (evt) => {
  const [file] = picture.files;
  if (file) {
    document.getElementById("pictureButton").click();
  }
};
var originalUsername = originalusername.value;
var originalEmail = originalemail.value;
var originalSecondaryEmail = originalsecondary_email.value;
var originalMotto = originalmotto.value;
var originalBio = originalbio.value;
var originalBirthDay = originalbirthday.value;
var originalTelephoneNumber = originaltelephone_number.value;
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
secondary_email.oninput = (evt) => {
  if (secondary_email.value === originalSecondaryEmail) {
    document.getElementById("secondary_emailButton").style.display = "none";
    secondary_email.classList.remove("changed");
  }
  if (secondary_email.value != originalSecondaryEmail) {
    document.getElementById("secondary_emailButton").style.display =
      "inline-block";
    secondary_email.classList.add("changed");
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
telephone_number.oninput = (evt) => {
  if (telephone_number.value === originalTelephoneNumber) {
    document.getElementById("telephone_numberButton").style.display = "none";
    telephone_number.classList.remove("changed");
  }
  if (telephone_number.value != originalTelephoneNumber) {
    document.getElementById("telephone_numberButton").style.display =
      "inline-block";
    telephone_number.classList.add("changed");
  }
};
confirm_password.oninput = (evt) => {
  document.getElementById("confirmButton").style.display = "inline-block";
  confirm_password.classList.add("changed");
};
