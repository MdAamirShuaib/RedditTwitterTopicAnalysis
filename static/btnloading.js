btn_ = document.querySelector(".btn");
btn_.onclick = function () {
  let selected = document.getElementById("topicName").value;
  if (selected != "") {
    this.classList.toggle("btn_load");
    this.innerHTML = "analyzing&nbsp;";
  }
};
