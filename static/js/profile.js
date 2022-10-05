// Convert string in ISO8601 format to date object
// e.g. 2013-02-08T02:40:00Z
//      2022-10-05 03:17:35.375637
function isoToObj(s) {
  var b = s.split(/[- .:]/i);

  return new Date(Date.UTC(b[0], --b[1], b[2], b[3], b[4], b[5]));
}

function timeToGo(s) {
  // Utility to add leading zero
  function z(n) {
    return (n < 10 ? "0" : "") + n;
  }

  // Convert string to date object
  var d = isoToObj(s);
  var diff = d - new Date();

  // Allow for previous times
  var sign = diff < 0 ? "-" : "";
  diff = Math.abs(diff);

  // Get time components
  var hours = (diff / 3.6e6) | 0;
  var mins = ((diff % 3.6e6) / 6e4) | 0;
  var secs = Math.round((diff % 6e4) / 1e3);

  // Return formatted string
  return sign + z(hours) + ":" + z(mins) + ":" + z(secs);
}

function main() {
  const collection = document.getElementsByClassName("task-timer");

  for (var i = 0; i < collection.length; i++) {
    var elem = collection[i];
    var start_time = elem.getAttribute("start-time");
    var end_time = elem.getAttribute("end-time");
    var timeLeft = timeToGo(end_time);

    if (!timeToGo(start_time).includes("-")) {
      elem.innerHTML = "Starts In: " + timeToGo(start_time);
    } else {
      elem.innerHTML = "Ends In: " + timeLeft;
    }

    if (timeLeft.includes("-")) {
      elem.innerHTML = "Ended: " + timeLeft.replace("-", "") + " Ago";
    }
  }
}

var interval = setInterval(main, 1000); // 1000 ms = 1 second

const Modal = document.getElementById("Modal");
Modal.addEventListener("show.bs.modal", (event) => {
  // Button that triggered the modal
  const button = event.relatedTarget;

  const id = button.getAttribute("task-id");
  const name = button.getAttribute("name");
  const minValue = button.getAttribute("min-value");
  const maxValue = button.getAttribute("max-value");
  const value = button.getAttribute("value");
  const repeat = button.getAttribute("repeat");
  const startDate = button.getAttribute("start-date");
  const endDate = button.getAttribute("end-date");
  const public = button.getAttribute("public");

  const idField = Modal.querySelector("#taskIDPassthrough");
  const nameField = Modal.querySelector("#name");
  const minValueField = Modal.querySelector("#min_value");
  const maxValueField = Modal.querySelector("#max_value");
  const valueField = Modal.querySelector("#value");
  const repeat0Field = Modal.querySelector("#repeat-0");
  const repeat1Field = Modal.querySelector("#repeat-1");
  const startDateField = Modal.querySelector("#start_date");
  const endDateField = Modal.querySelector("#end_date");
  const public0Field = Modal.querySelector("#public-0");
  const public1Field = Modal.querySelector("#public-1");

  idField.value = id;
  nameField.value = name;
  minValueField.value = minValue;
  maxValueField.value = maxValue;
  valueField.value = value;

  if (repeat === "true") {
    repeat0Field.checked = true;
    repeat1Field.checked = false;
  } else {
    repeat1Field.checked = true;
    repeat0Field.checked = false;
  }

  startDateField.value = startDate.split(".")[0];
  endDateField.value = endDate.split(".")[0];

  if (public === "true") {
    public0Field.checked = true;
    public1Field.checked = false;
  } else {
    public1Field.checked = true;
    public0Field.checked = false;
  }
});
