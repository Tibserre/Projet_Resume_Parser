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


function displayIfExistAndCreateHTMLForLinkedInSkills(data, fieldName, displayName, listId, maxItems) {
  if (data[fieldName]) {
    let list = data[fieldName];

    let skillsHTML = "";
    skillsHTML += "<div class='card'>"
    skillsHTML += "<div class='card-title'>" + displayName + "</div>"
    skillsHTML += "<ul class='card-list'>";

    for (let i = 0; i < list.length; i++) {
      if (i % maxItems === 0 && i !== 0) {
        skillsHTML += "</ul><ul class='card-list'>";
      }
      skillsHTML += "<li>" + list[i] + "</li>";
    }
    skillsHTML += "</ul>"
    skillsHTML += "</div>"
    document.getElementById(listId).innerHTML = skillsHTML;
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
  
  let skills = cvData["skills"];

  //appel des fonctions pour l'affichage des listes

  displayIfExist(cvData["formation"], "formation", "Formation", "formation", 5);
  displayIfExist(cvData["skills"], "Skills_applicatives", "Applicatives", "skills-applicatives", 5);
  displayIfExist(cvData["skills"], "Skills_methodo", "Méthodologie", "skills-methodo", 5);
  displayIfExist(cvData["skills"], "Skills_metiers", "Métier", "skills-metiers", 5);
  displayIfExist(cvData["skills"], "Skills_outils", "Outils", "skills-outils", 5);
  displayIfExist(cvData["skills"], "Skills_techniques", "Techniques", "skills-techniques", 5);
  displayIfExist(cvData["skills"], "competences fonctionnelles", "Fonctionnelles", "competences-fonctionnelles", 5);
  displayIfExist(cvData["skills"], "competences techniques", "Techniques", "competences-techniques", 5); ``
  displayIfExist(cvData["skills"], "langage", "Langages", "langage", 5);
  displayIfExistAndCreateHTMLForLinkedInSkills(cvData, "linkedin_skills", "Compétences LinkedIn", "linkedin_skills", 5);

  CreateList(cvData)

  // bouton pour afficher professionnal experiences
  let professionnalExpButton = document.getElementById("professionnal-experiences-button");
  professionnalExpButton.addEventListener("click", function () {

    let professionnalExpList = document.getElementById("professionnal-experiences-list");
    if (professionnalExpList.style.display === "none") {
      console.log("montrer");
      professionnalExpList.style.display = "flex";
    } else {
      console.log("cacher");
      professionnalExpList.style.display = "none";
    }

  });
}

function CreateList(data) {
  let professionnalExpList = document.getElementById("professionnal-experiences-list");
  professionnalExpList.innerHTML = ""; // On vide le contenu de la liste avant de l'afficher


  let professionnalExperiences = data["professionnal_experiences"]["experiences"];
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
}
