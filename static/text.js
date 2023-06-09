const testing = async () => {
  let reqPar = document.getElementById("reqPar");
  let topic = reqPar.dataset.topic;
  let count = reqPar.dataset.count;
  let response = await fetch(`/extractandanalyse/${topic}/${count}`);
  let data = await response.json();
  data = JSON.parse(data);
  document.getElementById("loading").innerHTML = "<div><div>";

  console.log(response);
  console.log(data);
  console.log(data.length);
  console.log(typeof data);

  // Create a table element
  const table = document.createElement("table");

  // Create thead element
  const thead = document.createElement("thead");
  table.appendChild(thead);

  // Create tr element for thead
  const tr = document.createElement("tr");
  thead.appendChild(tr);

  // Create th elements for thead
  const th1 = document.createElement("th");
  th1.textContent = "Title";
  tr.appendChild(th1);

  const th2 = document.createElement("th");
  th2.textContent = "PostText";
  tr.appendChild(th2);

  const th3 = document.createElement("th");
  th3.textContent = "Comments";
  tr.appendChild(th3);

  // Create tbody element
  const tbody = document.createElement("tbody");
  table.appendChild(tbody);

  // Append the table to the DOM
  document.getElementById("table").appendChild(table);
  // data.map((item, index) => {
  //   let row = tableBody.insertRow(index);
  //   let idCell = row.insertCell(0);
  //   let nameCell = row.insertCell(1);
  //   let emailCell = row.insertCell(2);
  //   idCell.innerHTML = item.Title;
  //   nameCell.innerHTML = item.PostText;
  //   emailCell.innerHTML = item.Comments;
  // });

  for (let i = 0; i < data.length; i++) {
    let row = tbody.insertRow(i);
    let idCell = row.insertCell(0);
    let nameCell = row.insertCell(1);
    let emailCell = row.insertCell(2);

    idCell.innerHTML = data[i].Title;
    nameCell.innerHTML = data[i].PostText;
    emailCell.innerHTML = data[i].Comments;
  }
};
testing();
