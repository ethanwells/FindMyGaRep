const searchButton = document.querySelector("#searchButton");
const searchInput = document.querySelector("#searchInput");
const results = document.querySelector("#results");

searchButton.addEventListener("click", function() {
  const zip = searchInput.value;
  getData(zip);
});

searchInput.addEventListener("keyup", function(event) {
  if (event.key === "Enter") {
    const zip = searchInput.value;
    getData(zip);
  }
});

function getData(zip) {
  Papa.parse("database.csv", {
    download: true,
    header: true,
    complete: function(results) {
      displayData(results.data, zip);
    }
  });
}

function displayData(data, zip) {
  results.innerHTML = "";

  const filteredData = data.filter(function(person) {
    if (searchInput.value.length != 0) {
      console.log("input length:");
      console.log(searchInput.value.length);
      return person.zip === zip;
    }
  });


  if (filteredData.length == 0 && (searchInput.value.length) != 0) {
    const div = document.createElement("div");
    
    const firstName = document.createElement("p");
    firstName.innerText = "no results found for " + searchInput.value;
    div.appendChild(firstName);
    console.log("none!");
    results.appendChild(div);
  }

  filteredData.forEach(function(person) {
    const div = document.createElement("div");
    div.className = "info-box"; 
    div.classList.add("person");
    console.log("here!")
    const firstName = document.createElement("p");
    firstName.innerText = "First Name: " + person.first;
    div.appendChild(firstName);

    const lastName = document.createElement("p");
    lastName.innerText = "Last Name: " + person.last;
    div.appendChild(lastName);

    const email = document.createElement("p");
    email.innerText = "Legislative Email: " + person.email;
    div.appendChild(email);

    const button = document.createElement("button");
    button.innerText = "Send Email";
    button.addEventListener("click", function() {
      window.location.href = "mailto:" + person.email;
    });
    div.appendChild(button);


    results.appendChild(div);
  });
}
