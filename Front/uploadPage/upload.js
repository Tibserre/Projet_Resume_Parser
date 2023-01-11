window.onload = function () {
  JSONResponse = getDataFromAPI();
  console.log(JSONResponse);
};


function getDataFromAPI() {
  return fetch('http://127.0.0.1:2000/resume-parser', {
    method: 'GET',
  })
    .then(function (response) {
      return response.json();
    })
    .then(function (data) {
      var resultat = JSON.stringify(data);
      var resultatJSON = JSON.parse(resultat)
      console.log(JSON.stringify(resultatJSON.reponse));
      ajoutJson(resultatJSON.reponse)
      return resultatJSON;
    })
}


function parsingJSON(JSON) {
  console.log(JSON.Promise);
}





// fonction pour afficher les lists
function displayList(list, title, elementId, maxColumn) {
  let listHtml = "";
  listHtml += "<div class='card'>"
  listHtml += "<div class='card-title'>" + title + "</div>"
  listHtml += "<ul class='card-list'>";
  for (let i = 0; i < list.length; i++) {
    if (i % maxColumn === 0 && i !== 0) {
      listHtml += "</ul><ul class='card-list'>";
    }
    listHtml += "<li>" + list[i] + "</li>";
  }
  listHtml += "</ul>"
  listHtml += "</div>"
  document.getElementById(elementId).innerHTML = listHtml;
}








function ajoutJson(data) {
  //const jsonContainer = document.getElementById('json');

  // ajout du JSON à l'élément
  //jsonContainer.appendChild(displayData(data));

// Récupération des données à partir de la variable "data"
let cvData = data["CV_-_TGU.docx"];
let formation = cvData["formation"]["formation"];
let linkedinSkills = cvData["linkedin_skills"];
let professionnalExperiences = cvData["professionnal_experiences"]["experiences"];
let skills = cvData["skills"];

//appel des fonctions pour l'affichage des listes
displayList(formation, "Formation", "formation", 5);
displayList(linkedinSkills, "Linkedin_skills", "linkedin_skills", 5);
displayList(skills["competences fonctionnelles"], "competences fonctionnelles", "competences-fonctionnelles", 5);
displayList(skills["competences techniques"], "competences techniques", "competences-techniques", 5);
displayList(skills["langage"], "langage", "langage", 5);


// bouton pour afficher professionnal experiences
let professionnalExpButton = document.getElementById("professionnal-experiences-button");
professionnalExpButton.addEventListener("click", function () {
  let listHtml = "";
  listHtml += "<ul class='card-list'>";
  for (let i = 0; i < professionnalExperiences.length; i++) {
    listHtml += "<li>" + professionnalExperiences[i] + "</li>";
    console.log(professionnalExperiences[i])
  }
  listHtml += "</ul>";
  document.getElementById("professionnal-experiences-list").innerHTML = listHtml;
  let professionnalExpList = document.getElementById("professionnal-experiences-list");
  professionnalExpList.classList.remove("hidden");
});
}
