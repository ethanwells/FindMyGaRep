// get references to HTML elements
const searchButton = document.querySelector("#searchButton");
const streetInput = document.getElementById("street-address");
const zipInput = document.getElementById("zipcode");
const resultDiv = document.getElementById("results");





// initialize geocodio client with API key

searchButton.addEventListener("click", function() {
  console.log("hello");
  // get user input values
  const street = streetInput.value;
  const zip = zipInput.value;

  // format address for API request
  const address = `${street} ${zip}`;

  // make GET request to server
  fetch(`https://obscure-beyond-79368.herokuapp.com/get_rep_info?streetAddress=${street}&zipcode=${zip}`)
    .then(response => response.json())
    .then(data => {
      // update resultDiv with representative information
      console.log(data)
      displayData(data.name, data.party, data.email, data.district);
    })
    .catch(error => {
      console.error(error);
      resultDiv.innerHTML = "<p>Error getting representative information. Please try again later.</p>";
    });
});


// add rep info to html
function displayData(repname, party, email, district) {
  const div = document.createElement("div");
  div.className = "info-box"; 
  div.classList.add("person");
  const repname_object = document.createElement("p");
  repname_object.innerText = "Name: " + repname;
  div.appendChild(repname_object);

  const repemail = document.createElement("p");
  repemail.innerText = "Legislative Email: " + email;
  div.appendChild(repemail);

  const button = document.createElement("button");
  button.innerText = "Send Email";
  button.addEventListener("click", function() {
    const username = "myusername";
    const emailSubject = "subject"
    var emailBody = `
            Hi Representative ${repname} 
            \n\n
            My name is ${username}, and I am your constituent in district ${district}. I am writing to you to express my support for Beyond the Box and my hope for you to support this bill HB 427.
            \n\n
            Beyond the Box is an initiative to include system-impacted people (SIPs) in higher education. 
            \n\n
            Reducing barriers for system-impacted people has been shown to:
            \n\n
            - Reduce recidivism: Initial studies report a recidivism rate of 5.6% for SIPs with a Bachelor’s degree. Georgia’s current recidivism rate hovers between 29-50%. Education can make a huge impact on reducing the change of future offenses, therefore increasing public safety!
            \n\n
            - Create a campus that includes everyone: Applicants with a criminal history are 2.5x more likely to get denied. Over 60% do not finish college applications when they encounter the question because they believe they will be rejected. Something as simple as removing the question will remove unnecessary obstacles for positive reentry and reintegration into society.
            \n\n
            HB 427 is important to me and our community. Please vote YES to reducing barriers to higher education so that we can have an education system in Georgia that gives everyone a chance at being a productive citizen of Georgia!
      `;

    const emailCommand = "mailto:" + email + "?subject=" + emailSubject + "&body=" + emailBody;
    window.location.href = emailCommand;
  });
  div.appendChild(button);


  results.appendChild(div);
}





