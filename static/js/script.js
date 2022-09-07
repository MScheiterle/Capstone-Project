$(document).ready(function () {
  var clicked = Cookies.get("active");

  if (clicked == "true" && $("#sidebar").hasClass("active") == false) {
    $("#sidebar").toggleClass("active");
  }

  $("#sidebarCollapse").on("click", function () {
    $("#sidebar").toggleClass("active");
    Cookies.set("active", $("#sidebar").hasClass("active"));
  });
});
$(document).ready(function () {
  $("#gamertagSubmit").on("click", function () {
    var search = $("#userSearchTermSideBar").val();
    if ($.trim(search) != "") {
      window.location.href = "/search/@/" + search;
    }
  });
});
$(document).ready(function () {
  $("#gamertagSubmitNav").on("click", function () {
    var searchMethod = $("#userSearchMethod").val();
    var search = $("#userSearchTerm").val();
    if ($.trim(search) != "") {
      window.location.href = "/search/" + searchMethod + "/" + search;
    }
  });
});
$(document).ready(function () {
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
});
$(document).ready(function () {
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
});
