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

function displayIfExist(data, fieldName, displayName, listId, maxItems) {
  if (data[fieldName]) {
    let list = data[fieldName];
    displayList(list, displayName, listId, maxItems);
  }
}






function ajoutJson(data) {
  function getCVName(data) {
    let cvName = Object.keys(data)[0]; // Récupère la première clé du JSON (ici "CV_-_TGU.docx")
    return cvName; // Retourne la partie avant le point (ici "CV_-_TGU")
  }

// Récupération des données à partir de la variable "data"
let cvData = data[getCVName(data)];
let formation = cvData["formation"]["formation"];
let linkedinSkills = cvData["linkedin_skills"];
let professionnalExperiences = cvData["professionnal_experiences"]["experiences"];
let skills = cvData["skills"];

//appel des fonctions pour l'affichage des listes

displayIfExist(cvData["formation"], "formation", "Formation", "formation", 5);
displayIfExist(cvData["skills"], "Skills_applicatives", "Skills applicatives", "skills-applicatives", 5);
displayIfExist(cvData["skills"], "Skills_methodo", "Skills méthodo", "skills-methodo", 5);
displayIfExist(cvData["skills"], "Skills_metiers", "Skills métier", "skills-metiers", 5);
displayIfExist(cvData["skills"], "Skills_outils", "Skills outils", "skills-outils", 5);
displayIfExist(cvData["skills"], "Skills_techniques", "Skills techniques", "skills-techniques", 5);

/*
displayList(formation, "Formation", "formation", 5);
displayList(linkedinSkills, "Linkedin_skills", "linkedin_skills", 5);
displayList(skills["competences fonctionnelles"], "competences fonctionnelles", "competences-fonctionnelles", 5);
displayList(skills["competences techniques"], "competences techniques", "competences-techniques", 5);
displayList(skills["langage"], "langage", "langage", 5);
   */



 

// bouton pour afficher professionnal experiences
let professionnalExpButton = document.getElementById("professionnal-experiences-button");
professionnalExpButton.addEventListener("click", function () {
  let professionnalExpList = document.getElementById("professionnal-experiences-list");
  professionnalExpList.innerHTML = ""; // On vide le contenu de la liste avant de l'afficher

  for (let i = 0; i < professionnalExperiences.length; i++) {
    let experience = professionnalExperiences[i];

    let experienceContainer = document.createElement("div"); //Crée un élément div pour chaque expérience
    experienceContainer.classList.add("experience-container");
    professionnalExpList.appendChild(experienceContainer);
    


    let experienceTitle = document.createElement("h3"); // Crée un élément h3 pour le titre de l'expérience
    experienceTitle.classList.add("experience-title");
    experienceTitle.innerHTML = experience;
    experienceContainer.appendChild(experienceTitle);
/*
    let experienceDetail = document.createElement("div"); // Crée un élément div pour les détails de l'expérience
    experienceDetail.classList.add("experience-detail");
    experienceDetail.innerHTML = experience;
    experienceContainer.appendChild(experienceDetail);
    */
  }
  professionnalExpList.classList.remove("hidden");
});
}
