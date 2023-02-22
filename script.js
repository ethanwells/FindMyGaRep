// get references to HTML elements
const searchButton = document.querySelector("#searchButton");
const streetInput = document.getElementById("street-address");
const zipInput = document.getElementById("zipcode");
const usernameInput = document.getElementById("name");
const resultDiv = document.getElementById("results");





// initialize geocodio client with API key

searchButton.addEventListener("click", async function() {
  resultDiv.innerHTML = '';
  // get user input values
  const street = streetInput.value;
  const zip = zipInput.value;

  // format address for API request
  const address = `${street} ${zip}`;

  console.log(usernameInput.value)
  if (usernameInput.value == null || usernameInput.value.replace(/ /g,'').length == 0) {
    resultDiv.innerHTML = "<p>please enter your full name</p>";
    throw new Error('username not entered');
  } 
  if (street == null || street.replace(/ /g,'').length == 0) {
    resultDiv.innerHTML = "<p>please enter your street address</p>";
    throw new Error('street address not entered');
  } 
  if (zip == null || zip.replace(/ /g,'').length == 0) {
    resultDiv.innerHTML = "<p>please enter your zipcode</p>";
    throw new Error('zipcode not entered');
  } 

  // make GET request to server
  try {
    // make GET request to server
    const response = await fetch(`https://obscure-beyond-79368.herokuapp.com/get_rep_info?streetAddress=${street}&zipcode=${zip}`);
    const data = await response.json();

    // update resultDiv with representative information
    console.log("data: !!!");
    console.log(data);

    // updateDB
    console.log("calling updateDB")
    updateDB(data.name, data.party, data.email, data.district, usernameInput.value, data.address);

    await displayData(data.name, data.party, data.email, data.district);
  } catch (error) {
    console.error(error);
    resultDiv.innerHTML = "<p>Error getting representative information. Please enter valid address, or try again later.</p>";
  }
});

async function getEmailBody() {
  try {
    const response = await fetch('./resources/emailbody_template.txt');
    const data = await response.text();
    console.log(data)
    return data;
  } catch (error) {
    console.error(error);
  }
}

// add rep info to html
async function displayData(repname, party, email, district) {
  const div = document.createElement("div");
  div.className = "info-box"; 
  div.classList.add("person");


  const yourrep = document.createElement("h2");
  yourrep.id = "yourrep";
  yourrep.innerText = "Your Rep:";
  div.appendChild(yourrep);

  const repname_object = document.createElement("h3");
  repname_object.innerText = repname;
  div.appendChild(repname_object);

  const button = document.createElement("button");
  button.id = "emailButton";
  button.innerText = "Send Email";

  // when send email button clicked
  button.addEventListener("click", async function() {
    const repLastName = repname.split(' ')[repname.split(' ').length - 1];
    const username = usernameInput.value;
    const emailSubject = "Support HB 427, Beyond the Box!";
    const emailBodyTemplate = (await getEmailBody());
    const emailBody = emailBodyTemplate
      .replace('${replastname}', repLastName)
      .replace('${username}', username)
      .replace('${district}', district)
      .replace(/\n/g, '%0D%0A');
    console.log(emailBody);
    const emailCommand = `mailto:${email}?subject=${emailSubject}&body=${emailBody}`;
    window.location.href = emailCommand;
  });
  div.appendChild(button);

  results.appendChild(div);

  results.scrollIntoView()
}

function updateDB(repname, repparty, repemail, district, username, useraddress) {

  // Create the request body
  let requestBody = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
  };

  // Send the request to the remote server
  fetch(`https://obscure-beyond-79368.herokuapp.com/update_database?repname=${repname}&repparty=${repparty}&repemail=${repemail}&repdistrict=${district}&username=${username}&useraddress=${useraddress}`, requestBody)
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));
}





