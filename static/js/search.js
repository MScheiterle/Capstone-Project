document
  .getElementById("gamertagSubmitMain")
  .addEventListener("click", function () {
    var search = $("#userSearchTermSearchPage").val();
    if ($.trim(search) != "") {
      window.location.href = "/search/" + search;
    } else {
      window.location.href = "/search";
    }
  });

var input = document.getElementById("userSearchTermSearchPage");
input.addEventListener("keypress", function (event) {
  var search = $("#userSearchTermSearchPage").val();
  if ($.trim(search) != "") {
    if (event.key === "Enter") {
      event.preventDefault();
      document.getElementById("gamertagSubmitMain").click();
    }
  }
});
